from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_pipeline_process() -> None:
    payload = {
        "source_type": "text",
        "source_value": "Necesito un resumen ejecutivo de este texto sobre arquitectura de IA.",
        "metadata": {"author": "carolina"},
    }
    response = client.post("/pipeline/process", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["route"] in {"fast_processing", "deep_processing"}
    assert body["strategy"]["strategy_name"] == "summarizer_agent"
    assert body["chunk_count"] >= 1
