# Presentacion de Defensa - IA Henry Proyecto

## Slide 1 - Portada

**Titulo:** Arquitectura Base para un Pipeline de Ingenieria en IA

**Subtitulo:** Proyecto academico inspirado en una arquitectura por capas para procesamiento inteligente

**Presenta:** Carolina

**Contexto:** Defensa de proyecto para curso de Ingenieria en IA

**Que decir:**

Buenos dias. En esta presentacion voy a defender el proyecto que construí a partir de un diagrama de arquitectura de IA. El objetivo fue transformar una idea arquitectonica en un sistema ejecutable, entendible y escalable, aunque manteniendo un nivel acorde a una implementacion amateur con buenas practicas de ingenieria.

---

## Slide 2 - Problema que resuelve

**Idea principal:**

Muchas soluciones con IA empiezan con una buena idea, pero fallan cuando hay que organizar el flujo completo: entrada, procesamiento, seleccion de estrategia, persistencia y salida.

**Problema concreto:**

- Recibir informacion desde distintas fuentes.
- Procesarla de forma ordenada.
- Decidir que estrategia usar segun el tipo de contenido.
- Devolver una salida estructurada para una API o una aplicacion cliente.

**Que decir:**

No quise hacer solo un script suelto. Quise plantear una base de sistema. El valor del proyecto no esta solo en usar IA, sino en organizar correctamente las responsabilidades para que despues sea facil integrar modelos, bases de datos vectoriales y colas reales.

---

## Slide 3 - Objetivo del proyecto

**Objetivo general:**

Diseñar e implementar una arquitectura modular para un pipeline de IA que pueda recibir datos, transformarlos, enrutar el procesamiento y preparar la ejecucion de agentes inteligentes.

**Objetivos especificos:**

- Separar el sistema por capas.
- Exponer el flujo mediante una API.
- Dejar una base extensible para produccion.
- Simular componentes de infraestructura como colas y almacenamiento.

**Que decir:**

Mi meta fue convertir el diagrama en un proyecto real que se pudiera correr localmente, probar y explicar. No me enfoque en entrenar un modelo, sino en la ingenieria necesaria para que un sistema con IA pueda funcionar de forma ordenada.

---

## Slide 4 - Vision general de la arquitectura

**Capas implementadas:**

- Input Layer
- Ingestion Layer
- Processing Router Layer
- AI Strategy Layer
- Orchestration Layer
- Output/API Layer
- Storage Layer

**Que decir:**

La arquitectura esta dividida por responsabilidades. Cada capa hace una sola cosa importante. Esto reduce acoplamiento, mejora mantenibilidad y facilita reemplazar componentes. Por ejemplo, hoy uso almacenamiento en memoria, pero la estructura ya permite migrar a Postgres, Redis o Qdrant sin rehacer toda la aplicacion.

---

## Slide 5 - Input Layer

**Funcion:**

Recibir y normalizar entradas desde distintas fuentes.

**Implementacion:**

- Texto directo
- URL simulada
- Archivo local

**Archivo clave:** `src/layers/input_layer/collector.py`

**Que decir:**

La capa de entrada abstrae el origen de los datos. Esto es importante porque en IA no siempre trabajamos solo con texto pegado manualmente. Muchas veces la informacion llega desde archivos, formularios, paginas o APIs externas. Mi diseño contempla eso desde el inicio.

---

## Slide 6 - Ingestion Layer

**Funcion:**

Transformar el contenido bruto en unidades manejables.

**Implementacion:**

- Limpieza basica del texto
- Generacion de chunks
- Estructuracion para pasos posteriores

**Archivo clave:** `src/layers/ingestion_layer/ingestor.py`

**Que decir:**

En sistemas de IA, dividir el contenido en fragmentos es una practica muy comun. Esto mejora la eficiencia y prepara el sistema para futuros embeddings, recuperacion semantica o razonamiento por bloques.

---

## Slide 7 - Processing Router Layer

**Funcion:**

Decidir la via de procesamiento segun las caracteristicas del contenido.

**Rutas actuales:**

- `fast_processing`
- `deep_processing`

**Archivo clave:** `src/layers/processing_router_layer/router.py`

**Que decir:**

No todo contenido necesita el mismo costo computacional. Por eso agregue una capa de router. Si el texto parece simple, puede ir por una ruta rapida. Si es mas largo o complejo, puede derivarse a un procesamiento mas profundo. Esta idea es muy util cuando se trabaja con modelos caros o con latencia alta.

---

## Slide 8 - AI Strategy Layer

**Funcion:**

Seleccionar el tipo de agente o estrategia mas adecuada.

**Estrategias actuales:**

- `summarizer_agent`
- `research_agent`
- `qa_agent`

**Archivo clave:** `src/layers/ai_strategy_layer/agents.py`

**Que decir:**

Esta capa representa la logica de decision inteligente. En vez de acoplar toda la logica en un solo punto, la estrategia se decide aparte. Eso permite que en una siguiente version pueda conectar un LLM real, un clasificador, o incluso un sistema multiagente.

---

## Slide 9 - Orchestration Layer

**Funcion:**

Coordinar el flujo completo del pipeline.

**Responsabilidades:**

- Crear identificador de request
- Ejecutar las capas en orden
- Publicar eventos
- Guardar datos
- Construir respuesta final

**Archivo clave:** `src/layers/orchestration_layer/engine.py`

**Que decir:**

Esta es la capa central del sistema. El orquestador no reemplaza la logica de otras capas, sino que las coordina. En terminos de ingenieria, este diseño mejora legibilidad, control del flujo y escalabilidad.

---

## Slide 10 - Output/API Layer

**Funcion:**

Exponer el sistema hacia el exterior mediante una API.

**Endpoints implementados:**

- `GET /health`
- `POST /pipeline/process`

**Archivos clave:**

- `src/main.py`
- `src/api/routes/health.py`
- `src/api/routes/pipeline.py`

**Que decir:**

Decidi usar FastAPI porque es una tecnologia moderna, simple y muy usada en proyectos de IA. Permite documentacion automatica con Swagger, validacion de datos y una integracion muy limpia con Python.

---

## Slide 11 - Almacenamiento e infraestructura

**Componentes actuales:**

- Cola en memoria
- Repositorio documental en memoria
- Vector store simulado

**Infraestructura preparada con Docker Compose:**

- API
- Redis
- Postgres
- Qdrant

**Archivos clave:**

- `src/storage/queue.py`
- `src/storage/repositories.py`
- `docker-compose.yml`

**Que decir:**

Aunque la implementacion base usa memoria para simplificar el desarrollo, el proyecto ya esta pensado para dar el salto a infraestructura real. Esto demuestra criterio de ingenieria: empezar simple, pero sin cerrar el camino a una evolucion profesional.

---

## Slide 12 - Flujo completo del sistema

**Secuencia funcional:**

1. La API recibe una solicitud.
2. Input Layer obtiene el contenido.
3. Ingestion Layer lo divide en chunks.
4. Router define la via de procesamiento.
5. Strategy Layer selecciona el agente.
6. Orchestration Layer registra y coordina todo.
7. Se devuelve una respuesta estructurada.

**Que decir:**

El sistema transforma una entrada cruda en una salida interpretable y lista para ser consumida por un cliente o por un sistema posterior. Esta separacion ayuda a mantener trazabilidad y orden en el ciclo de vida del dato.

---

## Slide 13 - Tecnologias usadas

**Stack principal:**

- Python 3.11
- FastAPI
- Pydantic
- Pytest
- Docker
- Docker Compose

**Que decir:**

Elegi tecnologias que hoy son muy relevantes en el ecosistema de IA aplicada. Python es el lenguaje dominante. FastAPI facilita exponer servicios. Pydantic mejora la validacion de contratos. Pytest permite asegurar calidad minima. Docker ayuda a estandarizar el entorno.

---

## Slide 14 - Ejemplo de uso

**Request de ejemplo:**

```json
{
  "source_type": "text",
  "source_value": "Necesito un resumen ejecutivo de este texto sobre arquitectura de IA.",
  "metadata": {
    "author": "carolina"
  }
}
```

**Respuesta esperada:**

- `request_id`
- `chunk_count`
- `route`
- `strategy`
- `output`

**Que decir:**

Con un request muy simple, el sistema ya puede inferir que la intencion del usuario esta orientada a un resumen y seleccionar el agente correspondiente. Esto demuestra que el pipeline no solo transporta datos, sino que aplica logica de negocio orientada a IA.

---

## Slide 15 - Decisiones de diseño

**Decisiones importantes:**

- Priorizar modularidad sobre complejidad prematura.
- Simular infraestructura para validar arquitectura primero.
- Dejar contratos tipados entre capas.
- Diseñar pensando en evolucion hacia produccion.

**Que decir:**

Como desarrolladora en etapa amateur, preferi construir una base clara y defendible antes que una solucion demasiado compleja o inestable. Creo que una buena arquitectura vale mas que integrar muchas herramientas sin control.

---

## Slide 16 - Limitaciones actuales

**Limitaciones reales:**

- No hay LLM real integrado todavia.
- No hay embeddings reales.
- El scraping de URLs es simulado.
- La persistencia aun es en memoria.
- Falta autenticacion y observabilidad.

**Que decir:**

Es importante marcar las limitaciones con honestidad. Este proyecto no pretende ser un producto final, sino una base de ingenieria sobre la cual se puede crecer. Precisamente por eso la arquitectura fue pensada para soportar esas mejoras sin romper el sistema.

---

## Slide 17 - Valor academico del proyecto

**Aprendizajes demostrados:**

- Pensamiento arquitectonico.
- Separacion de responsabilidades.
- Modelado de flujos de IA.
- Exposicion de servicios backend.
- Preparacion para infraestructura real.

**Que decir:**

Desde el punto de vista academico, este proyecto demuestra que entiendo que un sistema de IA no es solo un modelo. Tambien requiere API, almacenamiento, orquestacion, estrategias de procesamiento y diseño modular.

---

## Slide 18 - Mejoras futuras

**Proximos pasos:**

- Integrar un LLM real por API.
- Conectar Qdrant o pgvector para busqueda semantica.
- Usar Redis como broker real.
- Persistir resultados en Postgres.
- Agregar monitoreo, logs y seguridad.
- Incorporar evaluacion de respuestas.

**Que decir:**

La siguiente evolucion natural del proyecto es pasar de prototipo estructural a sistema funcional de IA aplicada. La base ya esta preparada para eso.

---

## Slide 19 - Cierre

**Mensaje final:**

El proyecto demuestra la conversion de un diagrama de arquitectura en una implementacion modular, ejecutable y escalable para un pipeline de IA.

**Que decir:**

En conclusion, mi aporte principal fue materializar una arquitectura de ingenieria en IA en un sistema real y explicable. Aunque la implementacion todavia es inicial, ya refleja criterios de diseño, escalabilidad y organizacion que son fundamentales en proyectos profesionales.

---

## Slide 20 - Preguntas posibles del jurado y respuestas cortas

**Pregunta:** ¿Donde esta la inteligencia artificial si todavia no conectaste un modelo real?

**Respuesta sugerida:**
La inteligencia del proyecto esta planteada en la arquitectura y en la estrategia de decision. Hoy esta simulada para validar el diseño, pero la estructura ya permite integrar un modelo real sin rehacer el sistema.

**Pregunta:** ¿Por que usaste FastAPI?

**Respuesta sugerida:**
Porque es una herramienta moderna, muy usada en backend para IA, con validacion, documentacion automatica y una curva de desarrollo muy adecuada para prototipos serios.

**Pregunta:** ¿Cual es el aporte principal del proyecto?

**Respuesta sugerida:**
Transformar un diagrama conceptual en un pipeline ejecutable, modular y preparado para crecer hacia un entorno de produccion.

**Pregunta:** ¿Que mejorarias primero?

**Respuesta sugerida:**
Integraria un LLM real, embeddings y persistencia en una base vectorial, porque eso convertiria la arquitectura en una solucion de IA aplicada mucho mas completa.

**Pregunta:** ¿Que aprendiste con este trabajo?

**Respuesta sugerida:**
Aprendi que en IA no alcanza con usar modelos. Tambien hay que diseñar bien la arquitectura, el flujo de datos y la integracion entre componentes.

---

## Recomendacion para exponer

- Habla entre 5 y 8 minutos.
- No intentes explicar todo el codigo.
- Enfatiza problema, arquitectura, flujo y escalabilidad.
- Reconoce limitaciones, pero muestra criterio tecnico.
- Si te preguntan por que algo esta simulado, responde que fue una decision de alcance para priorizar una base bien diseñada.

## Mini guion final de 30 segundos

Este proyecto toma una arquitectura de referencia para IA y la convierte en una solucion ejecutable, modular y escalable. Mi foco no fue solo hacer que funcione, sino diseñarlo con criterio de ingenieria. Por eso separé el sistema en capas, preparé la integracion con infraestructura real y dejé una base clara para evolucionar hacia un sistema de IA productivo.
