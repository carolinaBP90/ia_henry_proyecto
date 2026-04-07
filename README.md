# IA Henry Proyecto

Aplicacion Python para comparar contrato original vs adenda usando LLM multimodal y dos agentes, con salida JSON validada por Pydantic y trazabilidad en Langfuse.

## Flujo implementado (consigna)

1. Parsing multimodal de imagenes (2 ejecuciones): `src/image_parser.py`
2. Agente 1 de contextualizacion: `src/agents/contextualization_agent.py`
3. Agente 2 de extraccion de cambios: `src/agents/extraction_agent.py`
4. Validacion final con `ContractChangeOutput`: `src/models.py`
5. Trazabilidad con spans Langfuse: `src/services/tracing.py`

Span tree del pipeline principal:

```text
contract-analysis
├── parse_original_contract
├── parse_amendment_contract
├── contextualization_agent
└── extraction_agent
```

## Entry point principal (CLI)

El script principal ahora es `src/main.py` y acepta dos paths de imagen:

```bash
python -m src.main "C:/ruta/contrato_original.png" "C:/ruta/adenda.png"
```

Salida a archivo opcional:

```bash
python -m src.main "C:/ruta/contrato_original.png" "C:/ruta/adenda.png" --output-file "resultado.json"
```

## Variables de entorno requeridas

Minimo para ejecutar:

- `OPENAI_API_KEY`

Para trazabilidad en dashboard de Langfuse:

- `LANGFUSE_ENABLED=true`
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_HOST` (opcional, default cloud)

Ejemplo PowerShell:

```powershell
$env:OPENAI_API_KEY = "tu_openai_key"
$env:LANGFUSE_ENABLED = "true"
$env:LANGFUSE_PUBLIC_KEY = "tu_public_key"
$env:LANGFUSE_SECRET_KEY = "tu_secret_key"
```

## Modelo de salida validado

`ContractChangeOutput` en `src/models.py`:

- `sections_changed: List[str]`
- `topics_touched: List[str]`
- `summary_of_the_change: str`

## Ejecucion local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Levantar API (modo demo alternativa):

```bash
uvicorn src.main:app --reload
```

- Swagger: http://127.0.0.1:8000/docs
- Frontend simple: http://127.0.0.1:8000/

## Tests

```bash
pytest -q
```

## Docker

```bash
docker compose up --build
```

Servicios: API, Redis, Postgres y Qdrant.
