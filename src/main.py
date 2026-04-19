from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
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
	llm_client = get_openai_client()

	original_path = validate_contract_image_path(original_image_path)
	amendment_path = validate_contract_image_path(amendment_image_path)

	trace = tracing.start_root_trace(
		name="contract-analysis",
		metadata={
			"original_image_path": str(original_path),
			"amendment_image_path": str(amendment_path),
			"started_at": datetime.now(UTC).isoformat(),
		},
	)

	original_span_output: dict[str, object] = {}
	with tracing.span(
		trace,
		"parse_original_contract",
		input_data={"path": str(original_path)},
		metadata={"stage": "ocr", "document_role": "original"},
		output_data=original_span_output,
	):
		original_text = parse_contract_image(str(original_path))
		original_span_output.update(
			{
				"status": "ok",
				"output_preview": original_text[:800],
				"output_chars": len(original_text),
				"llm_call": llm_client.get_last_call_metadata(),
			}
		)

	amendment_span_output: dict[str, object] = {}
	with tracing.span(
		trace,
		"parse_amendment_contract",
		input_data={"path": str(amendment_path)},
		metadata={"stage": "ocr", "document_role": "amendment"},
		output_data=amendment_span_output,
	):
		amendment_text = parse_contract_image(str(amendment_path))
		amendment_span_output.update(
			{
				"status": "ok",
				"output_preview": amendment_text[:800],
				"output_chars": len(amendment_text),
				"llm_call": llm_client.get_last_call_metadata(),
			}
		)

	contextualization_agent = ContextualizationAgent(llm_client=llm_client)
	context_span_output: dict[str, object] = {}
	with tracing.span(
		trace,
		"contextualization_agent",
		input_data={
			"original_text_chars": len(original_text),
			"amendment_text_chars": len(amendment_text),
		},
		metadata={"stage": "agent", "agent": "ContextualizationAgent"},
		output_data=context_span_output,
	):
		context_report = contextualization_agent.run(
			original_text=original_text,
			amendment_text=amendment_text,
		)
		context_span_output.update(
			{
				"status": "ok",
				"output_preview": context_report[:800],
				"output_chars": len(context_report),
				"llm_call": llm_client.get_last_call_metadata(),
			}
		)

	extraction_agent = ExtractionAgent(llm_client=llm_client)
	extraction_span_output: dict[str, object] = {}
	with tracing.span(
		trace,
		"extraction_agent",
		input_data={
			"context_report_chars": len(context_report),
			"original_text_chars": len(original_text),
			"amendment_text_chars": len(amendment_text),
		},
		metadata={"stage": "agent", "agent": "ExtractionAgent"},
		output_data=extraction_span_output,
	):
		extraction_payload = extraction_agent.run(
			context_report=context_report,
			original_text=original_text,
			amendment_text=amendment_text,
		)
		extraction_span_output.update(
			{
				"status": "ok",
				"output": extraction_payload,
				"llm_call": llm_client.get_last_call_metadata(),
			}
		)

	try:
		return ContractChangeOutput.model_validate(extraction_payload)
	except ValidationError as exc:
		repaired_payload = extraction_payload
		for _ in range(runtime_settings.json_repair_max_attempts):
			repaired_payload = llm_client.repair_json_payload(
				invalid_payload=json.dumps(repaired_payload, ensure_ascii=False),
				validation_error=str(exc),
			)
			try:
				return ContractChangeOutput.model_validate(repaired_payload)
			except ValidationError as retry_exc:
				exc = retry_exc
		raise


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
