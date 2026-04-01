# DIAGRAMA VISUAL DEL FLUJO - Para apuntar en pantalla durante la presentación

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     PIPELINE DE IA - FLUJO COMPLETO                          │
└──────────────────────────────────────────────────────────────────────────────┘

                                    📱 API GATEWAY
                                         │
                    POST /pipeline/process + ProcessRequest
                                         │
                                         ▼
                        ┌──────────────────────────────┐
                        │  ORCHESTRATION LAYER         │
                        │  (engine.py)                 │
                        │  - Coordina flujo            │
                        │  - Genera request_id         │
                        │  - Orquesta pasos            │
                        └─────────────────────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
              ▼                          ▼                          ▼
    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
    │  INPUT LAYER     │    │INGESTION LAYER   │    │ ROUTER LAYER     │
    │ (collector.py)   │    │(ingestor.py)     │    │ (router.py)      │
    │                  │    │                  │    │                  │
    │ • Texto directo  │    │ • Limpia texto   │    │ avg_size > 180?  │
    │ • URL simulada   │    │ • Parte chunks   │    │ Yes → deep       │
    │ • Archivo local  │    │ • Estructural    │    │ No  → fast       │
    └──────────────────┘    └──────────────────┘    └──────────────────┘
              │                          │                          │
              └──────────────────────────┼──────────────────────────┘
                                         │
                                    raw_text
                                         │
                                         ▼
                        ┌─────────────────────────────┐
                        │  STRATEGY LAYER             │
                        │ (agents.py)                 │
                        │                             │
                        │ ¿"resumen" en texto?        │
                        │  Yes → summarizer_agent     │
                        │  No, deep? → research_agent │
                        │  Else → qa_agent            │
                        └─────────────────────────────┘
                                         │
                                    strategy
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
         ┌──────────────────┐  ┌──────────────────┐ ┌──────────────────┐
         │ STORAGE LAYER    │  │  QUEUE BROKER    │ │VECTOR STORE      │
         │ (repositories)   │  │  (queue.py)      │ │(repositories)    │
         │                  │  │                  │ │                  │
         │ document_store   │  │ Pub evento:      │ │ Embeddings de    │
         │ .save(doc)       │  │ "ingestion"      │ │ cada chunk       │
         │                  │  │                  │ │                  │
         └──────────────────┘  └──────────────────┘ └──────────────────┘
                    │                    │                    │
                    └────────────────────┼────────────────────┘
                                         │
                           ✅ Estado persistido
                                         │
                                         ▼
                        ┌─────────────────────────────┐
                        │  RESPONSE BUILDER           │
                        │                             │
                        │ request_id                  │
                        │ extracted_preview           │
                        │ chunk_count                 │
                        │ route                       │
                        │ strategy                    │
                        │ output (next actions)       │
                        └─────────────────────────────┘
                                         │
                                         ▼
                                  ProcessResponse JSON
                                         │
                                         ▼
                                    🎯 CLIENTE
```

---

## DETALLE POR CAPA - Referencias rapidas

```
┌────────────────────────────────────────────────────────────────────────────┐
│                          INPUT LAYER (collector.py)                        │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  Si source_type == "text"                                                 │
│    ↓ Devolver tal cual                                                    │
│                                                                            │
│  Si source_type == "url"                                                  │
│    ↓ Simular descarga (listo para scraper real)                          │
│                                                                            │
│  Si source_type == "file"                                                 │
│    ↓ Leer archivo del disco                                               │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

```
┌────────────────────────────────────────────────────────────────────────────┐
│                       INGESTION LAYER (ingestor.py)                        │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  raw_text = "Este es un texto largo que..."                              │
│                                                                            │
│  chunk_size = 300 caracteres                                              │
│                                                                            │
│  ↓  Divide en fragmentos de 300 chars                                     │
│                                                                            │
│  chunks = [                                                               │
│    Chunk(id="chunk-1", content="Este es un...", type="plain_text"),     │
│    Chunk(id="chunk-2", content="...texto...", type="plain_text"),       │
│    Chunk(id="chunk-3", content="...largo", type="plain_text"),          │
│  ]                                                                        │
│                                                                            │
│  💡 Importante: permite procesamiento en paralelo, embedding            │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

```
┌────────────────────────────────────────────────────────────────────────────┐
│                      ROUTER LAYER (router.py)                             │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  chunks = [chunk-1, chunk-2, chunk-3, chunk-4]                           │
│                                                                            │
│  avg_size = sum(len(chunks)) / len(chunks)                               │
│           = (50 + 48 + 52 + 49) / 4 = 49.75                              │
│                                                                            │
│  if avg_size > 180:                                                      │
│    return "deep_processing"    ← Mas trabajo, mas analysis              │
│  else:                                                                    │
│    return "fast_processing"    ← Simple, rápido                          │
│                                                                            │
│  💡 Esto permite optimizar costo (LLM caro) vs velocidad                │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

```
┌────────────────────────────────────────────────────────────────────────────┐
│                     STRATEGY LAYER (agents.py)                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  original_text = "Necesito un RESUMEN ejecutivo..."                      │
│                                                                            │
│  if "resumen" in text.lower() or "summary" in text.lower():             │
│    return StrategyDecision(                                               │
│      strategy_name="summarizer_agent",                                    │
│      confidence=0.92,                                                     │
│      reasoning="Se detecto intencion de resumen"                         │
│    )                                                                      │
│                                                                            │
│  elif route == "deep_processing":                                        │
│    return StrategyDecision(                                               │
│      strategy_name="research_agent",                                      │
│      confidence=0.84,                                                     │
│      reasoning="Contenido largo requiere analisis"                       │
│    )                                                                      │
│                                                                            │
│  else:                                                                    │
│    return StrategyDecision(                                               │
│      strategy_name="qa_agent",                                            │
│      confidence=0.78,                                                     │
│      reasoning="Flujo estandar"                                          │
│    )                                                                      │
│                                                                            │
│  💡 Hoy: heurísticas simples                                            │
│  💡 Mañana: LLM de clasificación real                                   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

```
┌────────────────────────────────────────────────────────────────────────────┐
│                       STORAGE LAYER (repositories.py)                      │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  DOCUMENT STORE (en memoria):                                             │
│    records = [                                                            │
│      {                                                                    │
│        request_id: "abc-123-def",                                        │
│        content: "Texto original completo...",                            │
│        metadata: { author: "carolina" }                                  │
│      }                                                                    │
│    ]                                                                      │
│                                                                            │
│  VECTOR STORE (en memoria):                                               │
│    vectors = [                                                            │
│      {                                                                    │
│        request_id: "abc-123-def",                                        │
│        chunk_id: "chunk-1",                                              │
│        embedding: [0.1, 0.2, 0.3, ...],  ← Seria real con LLM         │
│        content: "..."                                                    │
│      }                                                                    │
│    ]                                                                      │
│                                                                            │
│  💡 Hoy: listas en RAM                                                  │
│  💡 Mañana: Postgres + Qdrant                                           │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

```
┌────────────────────────────────────────────────────────────────────────────┐
│                        OUTPUT/API LAYER (main.py)                          │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  @router.post("/pipeline/process")                                        │
│  def process_request(payload: ProcessRequest) -> ProcessResponse:        │
│                                                                            │
│    Acepta:                                                                │
│    {                                                                      │
│      "source_type": "text|url|file",                                     │
│      "source_value": "...",                                              │
│      "metadata": { ... }                                                 │
│    }                                                                      │
│                                                                            │
│    Devuelve:                                                              │
│    {                                                                      │
│      "request_id": "uuid",                                               │
│      "extracted_preview": "...",                                         │
│      "chunk_count": 4,                                                   │
│      "route": "deep_processing",                                         │
│      "strategy": { name, confidence, reasoning },                        │
│      "output": { next_action, agent, queue }                            │
│    }                                                                      │
│                                                                            │
│  💡 FastAPI genera Swagger automático en /docs                          │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## CICLO COMPLETO DE UN REQUEST - Paso a paso

```
REQUEST ENTRA:
{
  "source_type": "text",
  "source_value": "Necesito un resumen de arquitectura de IA",
  "metadata": {"author": "carolina"}
}

        ↓ STEP 1: Input Layer
        collect("text", "Necesito un resumen...")
        → "Necesito un resumen de arquitectura de IA"

        ↓ STEP 2: Ingestion Layer
        ingest_text("Necesito un resumen...")
        → [Chunk-1, Chunk-2, Chunk-3]

        ↓ STEP 3: Router Layer
        route_chunks([...])
        → avg_size = 50 chars
        → "fast_processing"

        ↓ STEP 4: Strategy Layer
        decide_strategy("fast_processing", original_text)
        → "resumen" detected!
        → StrategyDecision(name="summarizer_agent", confidence=0.92)

        ↓ STEP 5: Save State
        broker.publish("ingestion_events", {...})
        document_store.save({...})
        vector_store.upsert({...} × 3 chunks)

        ↓ STEP 6: Build Response
        ProcessResponse(
          request_id="uuid-123",
          extracted_preview="Necesito un resumen de...",
          chunk_count=3,
          route="fast_processing",
          strategy={...},
          output={next_action: "dispatch_agent", agent: "summarizer_agent", ...}
        )

RESPONSE SALE:
{
  "request_id": "uuid-123",
  "extracted_preview": "Necesito un resumen de...",
  "chunk_count": 3,
  "route": "fast_processing",
  "strategy": {
    "strategy_name": "summarizer_agent",
    "confidence": 0.92,
    "reasoning": "Se detecto intencion de resumen en el texto."
  },
  "output": {
    "next_action": "dispatch_agent",
    "agent": "summarizer_agent",
    "queue": "agent_execution_queue"
  }
}
```

---

## ARQUITECTURA VS CODIGO - Mapeo Rapido

```
CAPA ARQUITECTONICA          →  ARCHIVO PYTHON
─────────────────────────────────────────────────────────
Input Layer                  →  src/layers/input_layer/collector.py
Ingestion Layer              →  src/layers/ingestion_layer/ingestor.py
Processing Router Layer      →  src/layers/processing_router_layer/router.py
AI Strategy Layer            →  src/layers/ai_strategy_layer/agents.py
Orchestration Layer          →  src/layers/orchestration_layer/engine.py
Output/API Layer             →  src/main.py, src/api/routes/pipeline.py
Storage Layer                →  src/storage/queue.py, src/storage/repositories.py
Configuration & Logging      →  src/core/config.py, src/core/logging.py
Data Schemas                 →  src/schemas/pipeline.py
Tests                        →  tests/test_pipeline.py
```

---

## DURANTE LA PRESENTACION - USA ESTO PARA APUNTAR

Imprime este archivo o mantén abierto en otra pantalla para:
1. Recordar el flujo visual
2. Apuntar componentes en el diagrama ASCII
3. Mostrar paso a paso como fluyen los datos
4. Mapear archivos a capas rápidamente
