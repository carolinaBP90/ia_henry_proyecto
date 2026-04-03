# IA Henry Proyecto

Proyecto base generado desde el diagrama de arquitectura (capas: Input, Ingestion, Processing+Router, AI Strategy, Orchestration y Output/API).

## Arquitectura implementada

- Input Layer: `src/layers/input_layer/collector.py`
- Ingestion Layer: `src/layers/ingestion_layer/ingestor.py`
- Processing Router Layer: `src/layers/processing_router_layer/router.py`
- AI Strategy Layer: `src/layers/ai_strategy_layer/agents.py`
- Orchestration Layer: `src/layers/orchestration_layer/engine.py`
- Output/API Layer: `src/main.py`, `src/api/routes/pipeline.py`
- Storage abstractions: `src/storage/queue.py`, `src/storage/repositories.py`

## Flujo de extremo a extremo

1. API recibe request en `POST /pipeline/process`.
2. Orquestador recolecta entrada (texto/url/archivo).
3. Ingesta parte el contenido en chunks.
4. Router decide via de procesamiento (`fast_processing` o `deep_processing`).
5. Capa de estrategia selecciona el agente.
6. Se persisten eventos y documentos en stores en memoria (listos para cambiar a Redis/DB/Vector DB).
7. API devuelve salida estructurada para capa cliente.

## Ejecutar local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Swagger:

- http://127.0.0.1:8000/docs
- Frontend simple: http://127.0.0.1:8000/

## Ejecutar con Docker Compose

```bash
docker compose up --build
```

Servicios disponibles:

- API: http://127.0.0.1:8000/docs
- Redis: localhost:6379
- Postgres: localhost:5432
- Qdrant: http://127.0.0.1:6333

## Ejecutar tests

```bash
pytest -q
```

## Siguientes pasos para pasar a produccion

- Conectar `QueueBroker` con Redis/RabbitMQ de forma real (ya incluido en Docker Compose).
- Reemplazar stores en memoria por Postgres + Vector DB (Qdrant/pgvector, ya incluidos en Docker Compose).
- Integrar modelos LLM y embeddings reales.
- Agregar autenticacion, rate limiting y observabilidad.
