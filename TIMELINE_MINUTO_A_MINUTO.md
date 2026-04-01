# TIMELINE MINUTO A MINUTO - Para seguir durante la presentacion

## PUEDES IMPRIMIR ESTO O TENER EN OTRA PANTALLA

---

```
⏱️  MIN 0-1
═══════════════════════════════════════════════════════════
ACCION:  Mostrar diagrama PNG
DECIR:   "Este es el diagrama que tuve que implementar..."
DURACION: 1 minuto
✓ Diagrama visible en pantalla
```

---

```
⏱️  MIN 1-5
═══════════════════════════════════════════════════════════
ACCION:  Introduccion y contexto
DECIR:   "Buenos dias, me llamo Carolina.
         Objetivo fue transformar diagrama en codigo ejecutable...
         Hoy muestro: arquitectura, tecnologias, flujo, demo, decisiones"
DURACION: 4 minutos
✓ Presentacion personal clara
✓ Objetivo claro
```

---

```
⏱️  MIN 5-11
═══════════════════════════════════════════════════════════
ACCION:  Abrir VS Code, mostrar estructura
DECIR:   "La arquitectura esta dividida en 7 capas...
         [Apuntar a cada carpeta mientras hablas]
         
         1. INPUT LAYER - recibe datos
         2. INGESTION - divide en chunks
         3. ROUTER - decide fast/deep
         4. STRATEGY - elige agente
         5. ORCHESTRATION - coordina todo
         6. OUTPUT/API - expone REST
         7. STORAGE - guarda estado"
         
DURACION: 6 minutos
✓ Carpetas visibles en explorer
✓ 7 capas explicadas
```

---

```
⏱️  MIN 11-15
═══════════════════════════════════════════════════════════
ACCION:  Mostrar requirements.txt y docker-compose.yml
DECIR:   "Stack: Python 3.11, FastAPI, Pydantic
         Por que Python? Dominante en IA.
         Por que FastAPI? Moderno, docs automaticas.
         
         Infraestructura:
         - Redis para colas
         - Postgres para persistencia
         - Qdrant para vectores"
         
DURACION: 4 minutos
✓ requirements.txt abierto
✓ docker-compose.yml abierto
```

---

```
⏱️  MIN 15-22
═══════════════════════════════════════════════════════════
ACCION:  Mostrar flujo de datos en codigo
DECIR:   "[Abrir engine.py]
         Cuando llega un request, orquestador hace 6 pasos:
         
         1. collect() - traer contenido
         2. ingest_text() - partir en chunks
         3. route_chunks() - decidir fast/deep
         4. decide_strategy() - elegir agente
         5. save state - publicar, persistir
         6. return response - salida tipada
         
         Cada paso esta en una capa diferente.
         Todo esta tipado con Pydantic."
         
         [Mostrar archivos rapido:
          - collector.py (breve)
          - ingestor.py (breve)
          - agents.py (breve)
          - pipeline.py (esquemas)]
         
DURACION: 7 minutos
✓ engine.py abierto
✓ Otros archivos mostrados brevemente
✓ Flujo entendido
```

---

```
⏱️  MIN 22 [MOMENTO CRITICO]
═══════════════════════════════════════════════════════════
ACCION:  INICIAR API EN TERMINAL
COMANDO: uvicorn src.main:app --reload
         
DECIR:   "Ahora levanto la API en vivo..."
         
ESPERAR: A que diga "Uvicorn running on http://127.0.0.1:8000"
         Esto puede tomar 5-10 segundos
         
DURACION: ~30 segundos para levantarla
✓ Terminal en segundo plano mostrando "Uvicorn running"
```

---

```
⏱️  MIN 22-24
═══════════════════════════════════════════════════════════
ACCION:  En PARALELO mientras API levanta:
         - Abrir navegador
         - Ir a http://127.0.0.1:8000/docs
         
DECIR:   "FastAPI genera documentacion interactiva automaticamente.
         Aqui vemos los 2 endpoints disponibles:
         - GET /health
         - POST /pipeline/process"
         
DURACION: 2 minutos
✓ Swagger abierto
✓ 2 endpoints visibles
```

---

```
⏱️  MIN 24-32
═══════════════════════════════════════════════════════════
ACCION:  DEMO EN VIVO - REQUESTS

REQUEST 1 [MIN 24-27]:
  Clic en POST /pipeline/process → Try it out
  
  Reemplazar payload con:
  {
    "source_type": "text",
    "source_value": "Necesito un resumen ejecutivo sobre la arquitectura de sistemas de IA. El proyecto que presente divide la responsabilidad en capas especializadas. Cada capa tiene un proposito bien definido.",
    "metadata": {"author": "carolina"}
  }
  
  Execute
  
DECIR:   "[Mientras carga]
         Este request va a:
         1. Detectar que pide 'resumen'
         2. Ver que el contenido es largo
         3. Seleccionar summarizer_agent
         4. Guardar estado
         5. Devolver respuesta"
         
         [Cuando respuesta llega]
         "Ven? request_id unico, 4 chunks generados,
          route=deep_processing, strategy=summarizer_agent
          Todo en < 100ms"
         
REQUEST 2 [MIN 27-29]:
  Try it out de nuevo
  
  Cambiar a source_type = "url":
  {
    "source_type": "url",
    "source_value": "https://example.com/arquitectura-ia",
    "metadata": {"author": "carolina"}
  }
  
DECIR:   "Si cambio a URL, sistema simula descarga.
         En produccion, aqui iria scraper real."

REQUEST 3 [MIN 29-31] (OPCIONAL):
  Si hay tiempo, mostrar algo que falle para explicar validacion.
  
  {
    "source_type": "INVALID",
    "source_value": "..."
  }
  
DECIR:   "Pydantic rechaza tipos invalidos. Esto evita bugs silenciosos."

DURACION: 8 minutos
✓ 2-3 requests exitosos
✓ Respuestas analizadas
✓ Demostracion de routing y strategy
```

---

```
⏱️  MIN 32-36
═══════════════════════════════════════════════════════════
ACCION:  Volver a VS Code
         Mostrar 5 decisiones de diseño
         
DECIR:   "Decisiones que tome:
         
         1. MODULARIDAD antes que complejidad
            → 7 capas aunque requiera mas trabajo inicial
         
         2. PYDANTIC para tipado fuerte
            → Contratos claros entre componentes
         
         3. ABSTRACCIONES en storage
            → Hoy en memoria, mañana Postgres/Qdrant
         
         4. API desde inicio
            → No scripts, servicios reales
         
         5. DOCKER COMPOSE ya preparado
            → Piensa en produccion"
         
DURACION: 4 minutos
✓ 5 decisiones claras
```

---

```
⏱️  MIN 36-39
═══════════════════════════════════════════════════════════
ACCION:  Limitaciones y proximos pasos
         
DECIR:   "Limitaciones HONESTAS:
         - No hay LLM real (OpenAI, etc)
         - Storage en memoria (no Postgres)
         - URLs scraped simuladamente
         
         PERO:
         - La arquitectura YA lo permite
         - No necesito rehacer nada
         
         Proximos pasos:
         1. LLM real (OpenAI o Ollama)
         2. Qdrant real para embeddings
         3. Postgres para persistencia
         4. Redis para colas
         5. Seguridad + observabilidad"
         
DURACION: 3 minutos
✓ Limitaciones claras
✓ Honestidad
✓ Vision a futuro
```

---

```
⏱️  MIN 39-40
═══════════════════════════════════════════════════════════
ACCION:  CIERRE
         
DECIR:   "En conclusion, transforme un diagrama conceptual
         en un pipeline ejecutable, modular y escalable.
         
         No es un producto final, es UNA BASE DE INGENIERIA
         sobre la cual se puede crecer.
         
         Mi aporte principal fue materializar la arquitectura
         con criterio tecnico.
         
         Cualquier pregunta?"
         
DURACION: 1 minuto
✓ Cierre fuerte
✓ Puerta abierta para preguntas
```

---

## CHECKPOINTS CRITICOS

Si en algun punto perdiste el timing, aqui estan los checkpoints:

```
✓ MIN 5:  Deberia estar mostrando la estructura de capas
✓ MIN 15: Deberia estar en el stack tecnologico
✓ MIN 22: DEMO debe iniciar aqui (API levantada)
✓ MIN 32: Deberia terminar DEMO, volver a decisiones
✓ MIN 39: Cierre inmediato
✓ MIN 40: FIN
```

Si en el MIN 22 aun no levantaste API:
- → Salta a mostrar codigo / screenshots
- → Cierre demo rapido, continua normalmente

Si en el MIN 32 aun estas en DEMO:
- → No importa, continua hasta terminarla
- → Reduce Decisiones a 2 minutos
- → Limitaciones a 1 minuto

Si todo va rápido:
- → Expande DEMO a 12 minutos
- → Profundiza en explicacion de archivos
- → Has preguntas retoricas para mantener engagement

---

## PARA NO ENTRAR EN PANICO

Si algo falla:
1. Respira
2. Mantén el timing
3. Salta al siguiente segmento
4. Dile al jurado: "La arquitectura es solida, este fue un problema ambiental"

El dibujo de la arquitectura y el codigo son lo mas importante.
La demo es cool pero no es el 100% del proyecto.
