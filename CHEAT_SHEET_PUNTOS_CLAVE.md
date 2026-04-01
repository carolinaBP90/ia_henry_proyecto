# QUICK REFERENCE - HOJA DE PUNTOS CLAVE
## Para usar DURANTE la presentacion (mantenerla visible)

---

## 🟢 SEGMENTO 1 (0-5 MIN): INTRO
```
📍 Mostrar diagrama PNG
📍 "Transform diagrama en codigo ejecutable"
📍 "Hoy muestro: arquitectura, por qué cada tech, demo, decisiones"
```

---

## 🟢 SEGMENTO 2 (5-11 MIN): ARQUITECTURA
```
📍 Abrir VS Code - Mostrar carpetas

7 CAPAS:
  1️⃣  INPUT LAYER        → Recibe texto/URL/archivo
  2️⃣  INGESTION LAYER    → Parte en chunks
  3️⃣  ROUTER LAYER       → Decide fast/deep processing
  4️⃣  STRATEGY LAYER     → Selecciona agente (resumen/research/QA)
  5️⃣  ORCHESTRATION      → Coordina TODO
  6️⃣  OUTPUT/API LAYER   → Expone REST API
  7️⃣  STORAGE LAYER      → Guardar eventos, docs, vectores

💡 VALOR: Separadas = Modular, Testeable, Escalable
```

---

## 🟢 SEGMENTO 3 (11-15 MIN): STACK TECNOLOGICO
```
📍 Mostrar requirements.txt

WHY PYTHON?
  → Dominante en IA/ML
  → Mejor ecosistema

WHY FASTAPI?
  → Moderno, rapido
  → Docs automaticas (Swagger)
  → Validacion Pydantic

WHY DOCKER COMPOSE?
  → Redis   = colas
  → Postgres = persistencia relacional
  → Qdrant = vector DB para embeddings
  → Demuestra pensamiento en escalabilidad
```

---

## 🟢 SEGMENTO 4 (15-22 MIN): FLUJO DE DATOS
```
📍 Abrir engine.py - funcion run_pipeline()

6 PASOS:
  1. collect() → traer contenido
  2. ingest_text() → partir en chunks
  3. route_chunks() → definir fast/deep
  4. decide_strategy() → elegir agente
  5. save state → publciar eventos, persistir docs/vectores
  6. return ProcessResponse → salida estructurada

💡 CADA PASO ES UNA RESPONSABILIDAD CLARA
💡 TODO ESTA TIPADO CON PYDANTIC (contrato firmado)
```

---

## 🟢 SEGMENTO 5 (22-32 MIN): DEMO EN VIVO ⭐⭐⭐
```
📍 Terminal: uvicorn src.main:app --reload
📍 Esperar: "Uvicorn running on http://127.0.0.1:8000"
📍 Browser: http://127.0.0.1:8000/docs

REQUEST 1 - Texto con "resumen":
  ↓ RESPONSE
  request_id: UUID
  chunk_count: 4
  route: "deep_processing" ✓
  strategy: "summarizer_agent" ✓
  
REQUEST 2 - URL:
  ↓ Muestra que sistema carga diferente fuente

💡 LA DEMO VALE MAS QUE 1000 PALABRAS
```

---

## 🟢 SEGMENTO 6 (32-36 MIN): DECISIONES DE DISEÑO
```
5 DECISIONES CLAVE:

1. MODULARIDAD > COMPLEJIDAD
   → Separar capas aunque sea "mas trabajo" al inicio
   
2. PYDANTIC PARA TIPADO FUERTE
   → Contratos entre componentes
   
3. ABSTRACCIONES EN STORAGE
   → Hoy en memoria, mañana Postgres/Redis/Qdrant
   
4. API DESDE INICIO
   → No scripts, servicios reales
   
5. DOCKER COMPOSE
   → Piensa en produccion antes
```

---

## 🟢 SEGMENTO 7 (36-39 MIN): LIMITACIONES + NEXT STEPS
```
LIMITACIONES (HONESTAS):
  ❌ No hay LLM real (OpenAI, etc)
  ❌ Storage en memoria (no Postgres)
  ❌ URLs scrapeadas simuladamente
  
PERO:
  ✅ La arquitectura YA lo permite
  ✅ No necesito rehacer nada para agregar

PROXIMOS PASOS:
  1️⃣  LLM real (OpenAI API o Ollama)
  2️⃣  Qdrant real para vectores
  3️⃣  Postgres para persistencia
  4️⃣  Redis para colas reales
  5️⃣  Security, rate limiting, logs
```

---

## 🟢 SEGMENTO 8 (39-40 MIN): CIERRE
```
"Este proyecto demuestra que entiendo 
la INGENIERIA de IA aplicada:

  ✅ Arquitectura modular
  ✅ Tipado fuerte
  ✅ Escalable horizontalmente
  ✅ Preparado para produccion

Cualquier pregunta?"
```

---

## 🚨 RESPUESTAS RAPIDAS PARA PREGUNTAS

**P: Por que Python?**
R: Dominante en IA. Punto.

**P: Y si el LLM es lento?**
R: La arquitectura esta separada, puedo mejorar una capa sin romper otras.

**P: Como escalas?**
R: Capas separadas = cada una escala independientemente. API es stateless, puedo replicarla.

**P: Por que Pydantic?**
R: Tipado fuerte = errores temprano, no en produccion.

**P: Que pasa despues de esta arquitectura?**
R: Conectar LLM real, vector DB real, y iterar sobre como manejar complejidad.

---

## ⏱️ TIMING CRÍTICO

```
Intro ........................... 5 min
Arquitectura ................... 6 min
Stack .......................... 4 min
Flujo .......................... 7 min
DEMO .......................... 10 min  ← IMPORTANTÍSIMO
Decisiones ..................... 4 min
Limitaciones ................... 3 min
Cierre ......................... 1 min
─────────────────────────────────────
TOTAL              40 min
```

Si te atrasas en DEMO, puedes saltarte algo de Decisiones.
Si tienes tiempo, expande DEMO.

---

## 📋 ARCHIVO ANTES DE EMPEZAR

- Terminal lista (venv activado)
- VS Code abierto con pestañas preparadas
- Navegador con 127.0.0.1:8000/docs listo (pero sin cargo aur)
- Diagrama PNG a mano

---

## 💡 ULTIMO REMINDER

No importa si algo falla. Si la API no levanta, enseña el código.
Lo importante es que muestres que ENTIENDEN ARQUITECTURA.

Un sistema pequeño pero bien diseñado vale más que un caos "funcional"
