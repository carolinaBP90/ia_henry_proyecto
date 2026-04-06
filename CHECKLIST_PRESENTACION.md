# CHECKLIST ANTES DE PRESENTAR - 40 MINUTOS

## PREPARACION DE AMBIENTE (30 minutos antes)

### 1. Instalacion y Dependencias
```bash
cd "c:\Users\Carolina\Documents\IA Henry Proyecto"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
- [ ] Instalar completado sin errores
- [ ] Venv activado

### 2. Terminal Preparada
```bash
# En una terminal lista (pero no ejecutado todavia):
uvicorn src.main:app --reload
```
- [ ] Terminal abierta y lista

### 3. VS Code Abierto con Tab Preparadas
```
code .
```
Tener estas pestanas abiertas:
- [ ] README.md
- [ ] src/layers/orchestration_layer/engine.py
- [ ] src/schemas/pipeline.py
- [ ] src/layers/input_layer/collector.py
- [ ] src/layers/ingestion_layer/ingestor.py
- [ ] src/layers/ai_strategy_layer/agents.py
- [ ] requirements.txt
- [ ] docker-compose.yml

### 4. Navegador Preparado
- [ ] Chrome/Firefox abierto
- [ ] Pestaña lista para http://127.0.0.1:8000/docs
- [ ] Pestaña lista para Swagger

### 5. Diagrama Visible
- [ ] PNG del diagrama listo en una carpeta o open en un visor

---

## DURANTE LA PRESENTACION - CHECKLIST TEMPORAL

### SEGMENTO 1 (0-5 min): Intro
- [ ] Mostrar diagrama PNG
- [ ] Presentarse: "Me llamo Carolina..."
- [ ] Contexto: "Objetivo fue transformar diagrama en codigo"

### SEGMENTO 2 (5-11 min): Arquitectura
- [ ] Abrir VS Code
- [ ] Mostrar estructura de carpetas
- [ ] Apuntar a cada carpeta mientras explicas las 7 capas
- [ ] Temporizado: 6 minutos

### SEGMENTO 3 (11-15 min): Stack Tecnologico
- [ ] Mostrar requirements.txt
- [ ] Explicar FastAPI, Pydantic, Python
- [ ] Mostrar docker-compose.yml
- [ ] Explicar Redis, Postgres, Qdrant
- [ ] Temporizado: 4 minutos

### SEGMENTO 4 (15-22 min): Flujo de Datos
- [ ] Abrir engine.py
- [ ] Seguir run_pipeline paso a paso (6 pasos)
- [ ] Abrir collector.py (breve)
- [ ] Abrir ingestor.py (breve)
- [ ] Abrir agents.py (breve)
- [ ] Mostrar pipeline.py - esquemas Pydantic
- [ ] Temporizado: 7 minutos

### SEGMENTO 5 (22-32 min): DEMO EN VIVO (MAS IMPORTANTE)
- [ ] En terminal: `uvicorn src.main:app --reload`
- [ ] Esperar a que API este lista
- [ ] Abrir navegador: http://127.0.0.1:8000/docs
- [ ] Primer request: texto con "resumen" - analizar respuesta
- [ ] Segundo request: `POST /pipeline/process-image` con imagen escaneada
- [ ] Mostrar que OCR + pipeline devuelven `request_id`, `route`, `strategy`, `output`
- [ ] OPCIONAL: pytest -v (si sobra tiempo)
- [ ] Temporizado: 10 minutos

### SEGMENTO 6 (32-36 min): Decisiones de Diseño
- [ ] Mostrar estructura nuevamente
- [ ] Explicar 5 decisiones clave
- [ ] Enfatizar "modularidad" y "escalabilidad"
- [ ] Temporizado: 4 minutos

### SEGMENTO 7 (36-39 min): Limitaciones y Proximos Pasos
- [ ] Ser honesto: "No hay LLM real, almacenamiento en memoria"
- [ ] Explicar: "Pero la arquitectura ya lo permite"
- [ ] Proximos pasos: LLM, Qdrant, Postgres, Redis, observabilidad
- [ ] Temporizado: 3 minutos

### SEGMENTO 8 (39-40 min): Cierre
- [ ] Resumen rapido: "Arquitectura modular, tipada, escalable"
- [ ] Cierre: "Cualquier pregunta?"
- [ ] Temporizado: 1 minuto

---

## PAYLOADS PARA COPIAR/PEGAR EN DEMO

### Payload 1: Texto Normal con "Resumen"
```json
{
  "source_type": "text",
  "source_value": "Necesito un resumen ejecutivo sobre la arquitectura de sistemas de IA. El proyecto que presente divide la responsabilidad en capas especializadas. Cada capa tiene un proposito bien definido. Esto evita acoplamiento y facilita el testing y la escalabilidad del sistema.",
  "metadata": {
    "author": "carolina",
    "timestamp": "2026-03-31"
  }
}
```

**Esperado:** route="deep_processing", strategy="summarizer_agent"

### Payload 2: URL
```json
{
  "source_type": "url",
  "source_value": "https://example.com/arquitectura-ia",
  "metadata": {
    "author": "carolina"
  }
}
```

**Esperado:** El sistema simula descarga de URL

### Request 3: Imagen escaneada (Swagger)

Usar endpoint `POST /pipeline/process-image`:

- `file`: selecciona una imagen JPG/PNG escaneada
- `metadata`: `{"author":"carolina","tipo":"ocr_demo"}`

**Esperado:** El sistema extrae texto OCR y ejecuta el pipeline normal.

### Payload 3: Texto Corto (Q&A)
```json
{
  "source_type": "text",
  "source_value": "Como funciona el router?",
  "metadata": {}
}
```

**Esperado:** route="fast_processing", strategy="qa_agent"

---

## COMANDOS IMPORTANTE MEMORIZADOS

### Iniciar API
```bash
uvicorn src.main:app --reload
```

### Ejecutar Tests
```bash
pytest -v
```

### Ver Carpeta del Proyecto
```bash
code .
```

### Ver requirements.txt rapido
```bash
cat requirements.txt
```

### Ver docker-compose.yml rapido
```bash
cat docker-compose.yml
```

---

## TIPS PARA NO OLVIDAR

1. **DEMO ES LO MAS IMPORTANTE**: Si falla algo, muestra el codigo en pantalla, pero la demo es lo que demuestra que funciona.

2. **NO TE APRURES**: Tienes 40 minutos. No es poco. Habla claro, pausa cuando cambias de tema.

3. **SI TE PIERDES**: Vuelvé a "el sistema tiene 7 capas, cada una hace una cosa". Es tu punto de anclaje.

4. **SI FALLA LA API**: No paniquez. Explica el codigo en VS Code. La arquitectura sigue siendo valida. Puedes hacer un screenshot de una ejecucion anterior si la tienes.

5. **PREGUNTAS DURANTE**: Si alguien pregunta, responde brevemente. Si es una pregunta grande, responde "Buena pregunta, volvemos a eso al final".

6. **CIERRE FUERTE**: Termina con "Este proyecto muestra que entiendo la ingenieria necesaria para IA aplicada: arquitectura modular, tipada, escalable y preparada para produccion."

---

## TIMING RAPIDO REFERENCE

| Segmento | Tiempo | Minutos |
|----------|--------|---------|
| Intro    | 00:00 - 05:00 | 5 |
| Arquitectura | 05:00 - 11:00 | 6 |
| Stack | 11:00 - 15:00 | 4 |
| Flujo | 15:00 - 22:00 | 7 |
| **DEMO** | **22:00 - 32:00** | **10** |
| Decisiones | 32:00 - 36:00 | 4 |
| Limitaciones | 36:00 - 39:00 | 3 |
| Cierre | 39:00 - 40:00 | 1 |
| **TOTAL** | | **40** |

---

## SEÑALES DE CONTROL MENTALES

- **Intro bien**: "Transforme diagrama en codigo" queda claro
- **Arqui bien**: El audience entiende 7 capas
- **Stack bien**: Saben por qué cada tech
- **Flujo bien**: Entienden el paso a paso
- **DEMO bien**: La API responde, muestra los campos esperados
- **Decisiones bien**: Hacen sentido la modularidad y escalabilidad
- **Limitaciones bien**: Aceptan que no hay LLM pero entienden por qué
- **Cierre bien**: Saben que aprendiste arquitectura, no solo coding

---

## DESPUES DE LA PRESENTACION

- [ ] Desactivar venv
- [ ] Cerrar procesor de API si aun corre
- [ ] Guardar screenshoots de la demo si fue exitosa
- [ ] Tomar notas de preguntas para mejorar futuras presentaciones
