# Plan de Presentacion - 40 Minutos
## Proyecto: Arquitectura Base para Pipeline de Ingenieria en IA

---

## TIMING TOTAL: 40 MINUTOS

### Segmento 1: Introduccion y Contexto (5 minutos)
**00:00 - 05:00**

#### Que mostrar en pantalla:
- Diagrama Arquitectura Proyecto.PNG (abierto en pantalla)
- README.md del proyecto

#### Guion a decir:

Buenos dias. Me llamo Carolina y les presento un proyecto que nace del desafio de convertir un diagrama de arquitectura de IA en un sistema ejecutable y modular.

*[Mostrar el diagrama]*

Este diagrama representa un pipeline completo para procesamiento inteligente. Mi objetivo fue no solo entender el diagrama, sino materializarlo en codigo, structures y decisiones de ingenieria que pudiera defender.

Hoy les voy a mostrar:
1. La arquitectura que implemente
2. Donde use cada tecnologia y por que
3. Como fluyen los datos a traves del sistema
4. Una demostracion en vivo del resultado

El valor del proyecto no esta solo en hacer algo que funcione, sino en demostrar que entiendo la ingenieria necesaria para que un sistema con IA sea organizan, escalable y mantenible.

---

### Segmento 2: Vision General de la Arquitectura (6 minutos)
**05:00 - 11:00**

#### Que mostrar en pantalla:
- Abrir en VS Code la carpeta del proyecto
- Mostrar la estructura de carpetas en el explorador

#### Comando para preparar:
```
cd "c:\Users\Carolina\Documents\IA Henry Proyecto"
code .
```

#### Guion a decir:

La arquitectura esta dividida en 7 capas. Cada una tiene una responsabilidad clara, esto es crucial en IA porque el flujo de datos es complejo y necesita trazabilidad.

*[Apuntar en el explorador a cada carpeta mientras hablas]*

**Input Layer** - Aqui recibimos datos desde diferentes fuentes: texto directo, URLs, archivos locales. Es como la puerta de entrada al sistema.

**Ingestion Layer** - Tomamos ese texto bruto y lo procesamos: limpieza, division en chunks. Esto prepara el contenido para pasos posteriores, especialmente importante si despues queremos hacer embeddings o recuperacion semantica.

**Processing Router Layer** - Decidimos la via de procesamiento. No todo contenido vale lo mismo. Si es simple, va por fast_processing. Si es largo o complejo, va por deep_processing. Esto es importante para optimizar costos cuando se usan modelos caros.

**AI Strategy Layer** - Aqui selectamos que tipo de agente o estrategia aplicar. Un texto puede necesitar resumen, investigacion profunda o responder preguntas. La arquitectura lo decide aqui.

**Orchestration Layer** - El corazon del sistema. Coordina todas las capas anteriores, maneja IDs de request, eventos, persistencia. Es donde todo se une.

**Output/API Layer** - Exponemos el pipeline mediante una API REST. Los clientes externos no ven la complejidad interna, solo hacen un request y reciben una respuesta estructurada.

**Storage Layer** - Cualquier dato que genere el sistema (eventos, documentos, vectores) pasa por aqui. Hoy es en memoria para prototipo, pero esta listo para cambiar a Postgres, Redis, Qdrant sin romper nada.

En terminos de ingenieria de IA, esta separacion permite que despues sea facil swapear componentes. Hoy uso placeholder, manana conecto un LLM real, en un mes cambio a una base vectorial. El diseño aguanta eso.

---

### Segmento 3: Stack Tecnologico (4 minutos)
**11:00 - 15:00**

#### Que mostrar en pantalla:
- requirements.txt
- docker-compose.yml
- Dockerfile

#### Comando para abrir:
```
cat requirements.txt
cat docker-compose.yml
```

#### Guion a decir:

Ahora veamos las tecnologias concretas. ¿Por que estas y no otras?

*[Mostrar requirements.txt]*

**FastAPI** - Es una herramienta moderna para construir APIs. Genera documentacion automatica (Swagger), permite validacion de datos con Pydantic y es muy eficiente. En el ecosistema de IA aplicada, es casi un estandar.

**Pydantic** - Define esquemas tipados para todos los datos que fluyen. Esto evita errores silenciosos y hace el sistema mas robusto.

**Python 3.11** - Porque es el lenguaje dominante en ciencia de datos y IA. Ningun otro lenguaje tiene el ecosistema que Python.

*[Mostrar docker-compose.yml]*

A nivel de infraestructura, arme un Docker Compose con 4 servicios:

**API** - El servicio FastAPI que expone el pipeline.

**Redis** - Sistema de colas en memoria alta velocidad. Para cuando el flujo de procesamiento es asincrono.

**Postgres** - Base de datos relacional. Cuando necesitemos persistir metadatos, auditorias, historiales.

**Qdrant** - Esto es especialmente importante para IA. Qdrant es una base de datos vectorial. Aqui guardaremos embeddings y podremos hacer busquedas semanticas.

El hecho de que ya este configurado en Docker Compose muestra que pense en escalabilidad desde el inicio. No es "vamos a agregar Redis despues si hace falta". Es "el sistema ya inteligentemente prepara el lugar para estos componentes".

---

### Segmento 4: Flujo de Datos (7 minutos)
**15:00 - 22:00**

#### Que mostrar en pantalla:
- src/layers/orchestration_layer/engine.py (archivo principal de flujo)
- src/schemas/pipeline.py (esquemas de datos)

#### Comando:
```
code src/layers/orchestration_layer/engine.py
code src/schemas/pipeline.py
```

#### Guion a decir:

Ahora veamos concretamente como fluyen los datos. Esto es el corazon del sistema.

*[Abrir engine.py - la funcion run_pipeline]*

Cuando llega una solicitud, esta funcion orquesta todo. Sigan conmigo paso a paso.

**Paso 1 - Coleccion:**
```python
raw_text = collect(payload.source_type, payload.source_value)
```
Llamamos a la capa de Input. Si es texto, devuelve texto. Si es URL, simula descarga. Si es archivo, lo lee del disco.

*[Mostrar collector.py brevemente]*

**Paso 2 - Ingestion:**
```python
chunks = ingest_text(raw_text)
```
Partimos el texto en fragmentos. Esto es crucial en IA porque un modelo no puede procesar 100 paginas de una vez. El chunking permite procesamiento manejable.

*[Mostrar ingestor.py]*

**Paso 3 - Routing:**
```python
route = route_chunks(chunks)
```
Analizamos el contenido. Si el contenido promedio es largo (>180 caracteres), va a deep_processing. Si es corto, va a fast_processing. Esto es una heuristica basica, pero demuestra la idea: adaptar el flujo al contenido.

**Paso 4 - Estrategia:**
```python
strategy = decide_strategy(route, raw_text)
```
Aqui es donde la IA entra. Analizamos el texto: ¿busca un resumen? ¿necesita investigacion profunda? ¿quiere Q&A? Seleccionamos el agente.

*[Mostrar agents.py]*

Hoy esta basado en palabras clave simples, pero es donde mañana conectamos un clasificador real o un LLM.

**Paso 5 - Persistencia y Eventos:**
```python
broker.publish("ingestion_events", {...})
document_store.save({...})
for chunk in chunks:
    vector_store.upsert({...})
```
Registramos lo que paso. El evento va a la cola, el documento va al repositorio, los chunks van al store vectorial. Esto permite rastreabilidad y auditoria.

**Paso 6 - Respuesta:**
```python
return ProcessResponse(
    request_id=request_id,
    extracted_preview=raw_text[:120],
    chunk_count=len(chunks),
    route=route,
    strategy=strategy,
    output=output,
)
```
Devolvemos una salida estructurada. El cliente sabe exactamente que le devolvemos: ID del request, vista previa del contenido, cuantos chunks se generaron, que ruta se tomo y que agente se selecciono.

*[Mostrar pipeline.py - los esquemas Pydantic]*

Estos esquemas son muy importantes. Definen un "contrato" entre las capas. Si algo viola el contrato (ejemplo: llega un string cuando se espera un numero), Pydantic lo rechaza inmediatamente. Eso evita bugs silenciosos.

---

### Segmento 5: Demostracion en Vivo (10 minutos)
**22:00 - 32:00**

#### Preparacion previa:
Asegúrate de que las dependencias esten instaladas:

```bash
cd "c:\Users\Carolina\Documents\IA Henry Proyecto"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

#### Comando para iniciar la API:
```bash
uvicorn src.main:app --reload
```

La API estara en http://127.0.0.1:8000/docs

#### Guion a decir:

Ahora vamos a ver el sistema en vivo. Levanto la API.

*[Ejecutar el comando de uvicorn, esperar a que este listo]*

Perfecto. El sistema esta escuchando en localhost:8000. FastAPI automaticamente genera documentacion interactiva. Abro el navegador en Swagger.

*[Abrir http://127.0.0.1:8000/docs en el navegador]*

Ven aqui dos endpoints:

**GET /health** - Simple health check. Indica que la API esta viva.

**POST /pipeline/process** - Este es nuestro endpoint principal. Toma un ProcessRequest y devuelve ProcessResponse.

Voy a hacer un request de ejemplo. Pruebo con un texto que pide resumen.

*[Hacer clic en POST /pipeline/process -> Try it out]*

*[Poner este payload]:*
```json
{
  "source_type": "text",
  "source_value": "Necesito un resumen ejecutivo sobre la arquitectura de sistemas de IA. El proyecto que presente divide la responsabilidad en capas especializadas. Cada capa tiene un proposito bien definido. Esto evita acoplamiento y facilita el testing.",
  "metadata": {
    "author": "carolina",
    "timestamp": "2026-03-31"
  }
}
```

*[Ejecutar - Execute]*

*[Esperar la respuesta]*

Perfecto. Veamos que nos devolvio:

*[Analizar la respuesta JSON mientras hablas]*

- **request_id**: Un UUID unico para rastrear este procesamiento.
- **extracted_preview**: Los primeros 120 caracteres. Util para mostrar en una UI.
- **chunk_count**: Los 4 chunks que genero el sistema.
- **route**: Detecto "deep_processing" porque el contenido es largo.
- **strategy**: Selecciono "summarizer_agent" con 92% de confianza porque detecto la palabra "resumen".
- **output**: Indica los proximos pasos: un agente debe ejecutar.

Todo esto ocurrio en milisegundos, coordinadamente, sin que el codigo tuviera que hacer logica manual. Eso es arquitectura.

Ahora voy a probar que pasa si cambio el source_type a URL.

*[Try it out de nuevo con este payload]*
```json
{
  "source_type": "url",
  "source_value": "https://example.com/arquitectura-ia",
  "metadata": {
    "author": "carolina"
  }
}
```

*[Execute]*

Ven que el sistema simulo la descarga. La razon es que en un prototipo, no queremos depender de conexiones reales a internet. Pero la estructura ya soporta implementar scraping real después.

Hagamos un test mas para demostrar la robustez del sistema.

*[Abrir terminal y ejecutar]*
```bash
pytest -v
```

*[O si prefieres hacerlo manualmente, te muestro aqui el test]*

```python
def test_pipeline_process() -> None:
    payload = {
        "source_type": "text",
        "source_value": "Necesito un resumen...",
        "metadata": {"author": "carolina"},
    }
    response = client.post("/pipeline/process", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["route"] in {"fast_processing", "deep_processing"}
    assert body["strategy"]["strategy_name"] == "summarizer_agent"
    assert body["chunk_count"] >= 1
```

Es decir, probamos que:
1. La API responde correctamente.
2. El router toma una decision valida.
3. El strategy selecciono el agente correcto.
4. Se generaron chunks.

Si los tests fallan, sabemos que hay un problema. Si pasan, sabemos que el pipeline funciona como se espera.

---

### Segmento 6: Decisiones de Diseño (4 minutos)
**32:00 - 36:00**

#### Que mostrar en pantalla:
- Volver a VS Code, mostrar la estructura de carpetas

#### Guion a decir:

Quiero explicar las decisiones clave que tome:

**Decision 1: Modularidad antes que complejidad.**
Pude haber hecho un solo archivo con todo. Pero eso seria un desastre. En cambio, separe responsabilidades en capas. Eso hace que el codigo sea legible y testeable.

**Decision 2: Tipado fuerte con Pydantic.**
Podría haber usado diccionarios sueltos. Pero eso es frágil. Pydantic fuerza contratos claros entre componentes. Si algo no es valido, lo sabes inmediatamente.

**Decision 3: Abstracciones para infraestructura.**
Las colas, documentos y vectores hoy estan en memoria. Pero la interfaz permite cambiar a Redis, Postgres, Qdrant sin tocar la logica del pipeline. Eso demuestra pensamiento de scalabilidad.

**Decision 4: API desde el inicio.**
No hice un script. Hice una API. Porque en IA real, raramente trabajas con scripts, trabajas con servicios. Esto tambien permite documentacion automatica y testing.

**Decision 5: Docker Compose.**
Incluir la infraestructura completa (Redis, Postgres, Qdrant) desde el inicio señala que pienso en produccion, no solo en prototipo.

Estas decisiones reflejan que entiendo la diferencia entre "codigo que funciona" y "arquitectura que escala".

---

### Segmento 7: Limitaciones y Proximos Pasos (3 minutos)
**36:00 - 39:00**

#### Guion a decir:

Es importante ser honesto sobre limitaciones.

**Limitacion 1: Ningun LLM real.**
El sistema no conecta OpenAI, Anthropic, Ollama ni ningun modelo real. Los agentes estan simulados. Pero la arquitectura YA PERMITE conectar uno sin rehacer nada.

**Limitacion 2: Almacenamiento en memoria.**
Redis, Postgres, Qdrant estan definidos en Docker pero no conectados al codigo. Mi prioridad fue validar la arquitectura primero.

**Limitacion 3: Scraping simulado.**
URLs se procesan de forma simulada, no real.

Pero no son debilidades fatales. Son decisiones de alcance. Prioriza estructura sobre complejidad.

**Proximos pasos naturales:**

1. Conectar un LLM real (OpenAI API o un modelo local con Ollama).
2. Integrar Qdrant para busqueda vectorial real.
3. Persistir en Postgres.
4. Usar Redis para colas reales.
5. Agregar autenticacion, rate limiting, observabilidad.

Cada uno de estos pasos es posible sin rehacer la arquitectura. Eso es lo importante.

---

### Segmento 8: Cierre (1 minuto)
**39:00 - 40:00**

#### Guion a decir:

En conclusion, lo que present es una arquitectura modular, tipada, escalable y funcional para un pipeline de IA. No es un producto final, pero demuestra que entiendo la ingenieria necesaria.

Mi contribucion principal fue transformar un diagrama en codigo, en decisiones, en un sistema que se puede correr, probar, explicar y evolucionar.

Cualquier pregunta?

---

## NOTAS PRACTICAS PARA LA PRESENTACION

### Antes de empezar:
1. Abre todos los archivos que vas a mostrar en VS Code (pestañas preparadas).
2. Ten la terminal lista.
3. Instala las dependencias antes (si no las tienes).
4. Abre el navegador en http://127.0.0.1:8000/docs (pestaña lista).
5. Ten el diagrama PNG a mano.

### Durante la presentacion:
- Habla claro y no muy rapido. 40 minutos da mucho tiempo.
- Si olvidas algo, no importa. Puedes volver a mencionarlo.
- Si surge una pregunta, responde pero luego retoma.
- La demostracion es lo mas importante. Si funciona, la audiencia lo ve.

### Si algo falla en la demostracion:
- Mantén la calma. Explica que algun componente no esta listo, pero "la arquitectura esta diseñada para esto".
- Muestra el codigo en VS Code en su lugar.

### Timing critico:
- Introduccion: 5 min (flexible, si es muy interesante, 6 está bien).
- Arquitectura: 6 min (mostrar carpetas, explicar capas).
- Stack: 4 min (explicar por qué cada tech).
- Flujo: 7 min (walkthrough del code).
- Demo: 10 min (lo más importante, déjale tiempo).
- Decisiones: 4 min (por qué hiciste asi).
- Limitaciones: 3 min (sé honesto).
- Cierre: 1 min (conclusión y preguntas).

Total: 40 minutos.

---

## PREGUNTAS ESPERADAS Y RESPUESTAS CORTAS

**P:** ¿Por que Python y no otra cosa?

**R:** Porque es el lenguaje dominante en AI y ciencia de datos. Tiene el mejor ecosistema de librerias para estos problemas.

**P:** ¿Cual es la diferencia entre tus routers y los agentes?

**R:** El router decide la via de procesamiento (fast/deep) basado en caracteristicas del contenido. El agente decide QUE HACER (resumen, investigacion, Q&A) basado en la intencion detectada.

**P:** ¿Por que no integraste un LLM real?

**R:** Porque queria validar primero que la arquitectura fuera solida. LLMs son caros y requieren configuracion. Una arquitectura mala con LLM integrado sigue siendo mala. Una buena arquitectura sin LLM se puede escalar facilmente.

**P:** ¿Qdrant sobre pgvector?

**R:** Ambos son validos. Qdrant es especifico para vectores, pgvector es integrado a Postgres. Depende del caso de uso. Aqui use Qdrant porque es mas specialised para search semantico.

**P:** ¿Como manejas escalabilidad?

**R:** Separando responsabilidades. Si alguna capa es cuello de botella, la upgrade sin tocar otras. Por ejemplo, si los embeddings son lentos, cambio Qdrant a una version distribuida. Si el volumen de documentos crece, cambio Postgres a una instancia mas grande. La API ya esta sin estado (stateless), asi que puedo replicarla horizontalmente.

**P:** ¿Que aprendiste con esto?

**R:** Que en IA aplicada, la arquitectura y el diseño importan tanto como los modelos. Un modelo genial en una arquitectura mala va a fracasar. Una arquitectura buena con un modelo simple puede escalar y mejorar continuamente.
