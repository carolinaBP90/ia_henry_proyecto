from src.schemas.pipeline import StrategyDecision


def decide_strategy(route: str, original_text: str) -> StrategyDecision:
    lowered = original_text.lower()

    if "resumen" in lowered or "summary" in lowered:
        return StrategyDecision(
            strategy_name="summarizer_agent",
            confidence=0.92,
            reasoning="Se detecto intencion de resumen en el texto.",
        )

    if route == "deep_processing":
        return StrategyDecision(
            strategy_name="research_agent",
            confidence=0.84,
            reasoning="El contenido es largo y requiere analisis extendido.",
        )

    return StrategyDecision(
        strategy_name="qa_agent",
        confidence=0.78,
        reasoning="Se aplica flujo estandar de preguntas/respuestas.",
    )
