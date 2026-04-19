from __future__ import annotations

import argparse
import json
from pathlib import Path

from fastapi import FastAPI
from pydantic import ValidationError

from src.api.routes.health import router as health_router
from src.api.routes.pipeline import router as pipeline_router
from src.api.routes.ui import router as ui_router
from src.agents.contextualization_agent import ContextualizationAgent
from src.agents.extraction_agent import ExtractionAgent
from src.config import get_settings as get_runtime_settings
from src.image_parser import (
	parse_contract_image,
	validate_contract_image_path,
)
from src.models import ContractChangeOutput
from src.core.config import get_settings
from src.core.logging import configure_logging
from src.services.openai_client import get_openai_client
from src.services.tracing import TracingService

settings = get_settings()
configure_logging()

app = FastAPI(title=settings.app_name)
app.include_router(ui_router)
app.include_router(health_router)
app.include_router(pipeline_router)


def run_contract_analysis(original_image_path: str, amendment_image_path: str) -> ContractChangeOutput:
	"""Execute full contract comparison pipeline required by the challenge."""
	runtime_settings = get_runtime_settings()
	tracing = TracingService(runtime_settings)

	original_path = validate_contract_image_path(original_image_path)
	amendment_path = validate_contract_image_path(amendment_image_path)

	try:
		with tracing.root_trace(
			name="contract-analysis",
			input={
				"original_image_path": str(original_path),
				"amendment_image_path": str(amendment_path),
			},
		) as root_span:
			# Get a LangChain callback handler scoped to this root trace so all
			# LLM generations (model name, token usage, latency) are captured
			# automatically as nested observations — no manual tracking needed.
			handler = tracing.get_langchain_handler()
			llm_client = get_openai_client(callbacks=[handler] if handler else [])

			with tracing.span("parse_original_contract", metadata={"stage": "ocr", "document_role": "original"}):
				original_text = parse_contract_image(str(original_path), client=llm_client)

			with tracing.span("parse_amendment_contract", metadata={"stage": "ocr", "document_role": "amendment"}):
				amendment_text = parse_contract_image(str(amendment_path), client=llm_client)

			contextualization_agent = ContextualizationAgent(llm_client=llm_client)
			with tracing.span("contextualization_agent", metadata={"stage": "agent", "agent": "ContextualizationAgent"}):
				context_report = contextualization_agent.run(
					original_text=original_text,
					amendment_text=amendment_text,
				)

			extraction_agent = ExtractionAgent(llm_client=llm_client)
			with tracing.span("extraction_agent", metadata={"stage": "agent", "agent": "ExtractionAgent"}):
				extraction_payload = extraction_agent.run(
					context_report=context_report,
					original_text=original_text,
					amendment_text=amendment_text,
				)

			try:
				result = ContractChangeOutput.model_validate(extraction_payload)
			except ValidationError as exc:
				repaired_payload = extraction_payload
				for _ in range(runtime_settings.json_repair_max_attempts):
					repaired_payload = llm_client.repair_json_payload(
						invalid_payload=json.dumps(repaired_payload, ensure_ascii=False),
						validation_error=str(exc),
					)
					try:
						result = ContractChangeOutput.model_validate(repaired_payload)
						break
					except ValidationError as retry_exc:
						exc = retry_exc
				else:
					raise

			if root_span is not None:
				root_span.update(output=result.model_dump())

			return result
	finally:
		# CRITICAL: flush all queued Langfuse events before the process exits.
		# Without this, traces are never delivered from the background queue.
		tracing.shutdown()


def _build_arg_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		description="Run multimodal contract analysis over original contract and amendment images.",
	)
	parser.add_argument("original_image_path", help="Path to original contract image (png/jpeg)")
	parser.add_argument("amendment_image_path", help="Path to amendment/addendum image (png/jpeg)")
	parser.add_argument(
		"--output-file",
		default="",
		help="Optional output JSON file path. If omitted, result is printed to stdout.",
	)
	return parser


def main() -> int:
	parser = _build_arg_parser()
	args = parser.parse_args()

	result = run_contract_analysis(
		original_image_path=args.original_image_path,
		amendment_image_path=args.amendment_image_path,
	)

	rendered = result.model_dump_json(indent=2, ensure_ascii=False)
	if args.output_file:
		output_path = Path(args.output_file)
		output_path.parent.mkdir(parents=True, exist_ok=True)
		output_path.write_text(rendered + "\n", encoding="utf-8")
	else:
		print(rendered)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
