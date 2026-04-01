# Script de Inicializacion Rapida - Ejecutar 10 minutos antes de presentar

## PARA WINDOWS (PowerShell)

Abre PowerShell en la carpeta del proyecto y copia/pega esto:

```powershell
# 1. Activar venv
.\.venv\Scripts\Activate.ps1

# 2. Verificar que pip install funciono
pip list | findstr fastapi

# 3. Abrir VS Code con todas las pestanas
code .

# 4. Mensaje de exito
Write-Host "✅ Ambiente listo. Ya puedes presentar." -ForegroundColor Green
```

---

## PARA MAC/LINUX (Bash)

```bash
# 1. Activar venv
source .venv/bin/activate

# 2. Verificar que pip install funciono
pip list | grep fastapi

# 3. Abrir VS Code
code .

# 4. Mensaje
echo "✅ Ambiente listo. Ya puedes presentar."
```

---

## PASOS PREVIOS (hacer 30 min antes)

### Paso 1: Instalar dependencias (si no ya hiciste)
```bash
cd "c:\Users\Carolina\Documents\IA Henry Proyecto"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Paso 2: Preparar Terminal para API (no ejecutar aún)
Abre una terminal adicional y ten lista para copiar/pegar:
```bash
uvicorn src.main:app --reload
```

### Paso 3: Abrir navegador en tab sin cargar
- Chrome/Firefox
- URL lista: http://127.0.0.1:8000/docs
- NO CARGAR todavía (solo tenerla lista)

### Paso 4: Abrir VS Code
```bash
code .
```

---

## DENTRO DE VS CODE - TABS A PREPARAR (en orden de uso)

```
TAB 1: README.md
TAB 2: DIAGRAMA_VISUAL_FLUJO.md (para referencia)
TAB 3: src/main.py
TAB 4: src/api/routes/pipeline.py
TAB 5: src/api/routes/health.py
TAB 6: src/schemas/pipeline.py
TAB 7: src/layers/orchestration_layer/engine.py
TAB 8: src/layers/input_layer/collector.py
TAB 9: src/layers/ingestion_layer/ingestor.py
TAB 10: src/layers/ai_strategy_layer/agents.py
TAB 11: src/layers/processing_router_layer/router.py
TAB 12: src/storage/queue.py
TAB 13: src/storage/repositories.py
TAB 14: requirements.txt
TAB 15: docker-compose.yml
TAB 16: Dockerfile
```

O mas simple: Abre solo estos archivos principales:
```
- src/main.py
- src/schemas/pipeline.py
- src/layers/orchestration_layer/engine.py
- src/layers/input_layer/collector.py
- src/layers/ingestion_layer/ingestor.py
- src/layers/ai_strategy_layer/agents.py
- docker-compose.yml
- requirements.txt
```

---

## DURANTE LA PRESENTACION - SECUENCIA RECOMENDADA

```
TIMING  | ACCION                        | ARCHIVO / COMANDO
────────┼───────────────────────────────┼─────────────────────────────────
0-1 min | Mostrar diagrama              | Diagrama Arquitectura Proyecto.PNG
        |                               |
1-5 min | Intro, contexto               | (Hablado)
        |                               |
5-7 min | Mostrar carpetas y .gitignore | VS Code: File Explorer
        |                               |
7-11 min| Explicar 7 capas              | VS Code: carpetas en explorador
        |                               |
11-13   | Mostrar requirements.txt      | VS Code: requirements.txt
        |                               |
13-14   | Mostrar docker-compose.yml    | VS Code: docker-compose.yml
        |                               |
14-15   | Explicar por qué cada tech    | (Hablado)
        |                               |
15-22   | Mostrar flujo de datos:       | 
        |  - engine.py paso a paso      | VS Code: engine.py
        |  - collector.py                | VS Code: collector.py
        |  - ingestor.py                | VS Code: ingestor.py
        |  - agents.py                  | VS Code: agents.py
        |  - schemas                    | VS Code: pipeline.py
        |                               |
22 min  | INICIAR API EN TERMINAL       | Terminal: uvicorn src.main:app --reload
        | (mientras trabajas)           |
        |                               |
24 min  | Abrir navegador               | http://127.0.0.1:8000/docs
        |                               |
24-32   | DEMO EN VIVO:                 | Browser: Swagger
        |  - Request 1 (Resumen)        | Payload: ver PAYLOADS en CHECKLIST
        |  - Request 2 (URL)            | 
        |  - Request 3 (Q&A)            |
        |                               |
32-36   | Volver a VS Code              | VS Code: explicar 5 decisiones
        | Explicar decisiones           |
        |                               |
36-39   | Explicar limitaciones         | (Hablado)
        |                               |
39-40   | Cierre                        | (Hablado)
```

---

## ARQUIVOS IMPORTANTES EN ORDEN

### Si te piden mostrar el código rapido, en este orden:

1. **engine.py** (5 min)
   - Es el corazón, muestra el flujo completo
   - Path: `src/layers/orchestration_layer/engine.py`

2. **pipeline.py** (2 min)
   - Esquemas Pydantic, validacion
   - Path: `src/schemas/pipeline.py`

3. **collector.py** (1 min)
   - Simpe, entrada
   - Path: `src/layers/input_layer/collector.py`

4. **ingestor.py** (1 min)
   - Chunking basico
   - Path: `src/layers/ingestion_layer/ingestor.py`

5. **agents.py** (1 min)
   - Estrategia simple
   - Path: `src/layers/ai_strategy_layer/agents.py`

6. **main.py** (1 min)
   - FastAPI setup
   - Path: `src/main.py`

---

## QUICK LAUNCH CHECKLIST (ULTIMO MINUTO)

```
⬜ Terminal 1: `cd proyecto && .venv\Scripts\activate`
⬜ Terminal 1: `uvicorn src.main:app --reload` (INICIAR)
⬜ Esperar: "Uvicorn running on http://127.0.0.1:8000"
⬜ VS Code: abierto con archivos lista
⬜ Browser: pestaña http://127.0.0.1:8000/docs lista (sin cargar)
⬜ PNG del diagrama visible o a 1 clic
⬜ Este archivo (QUICK_LAUNCH) abierto como referencia
✅ LISTO PARA PRESENTAR
```

---

## SI ALGO FALLA EN EL ULTIMO MINUTO

### API no levanta:
```bash
# Verifica que venv este activado
pip list | findstr fastapi

# Si falta, instala:
pip install fastapi uvicorn

# Intenta de nuevo:
uvicorn src.main:app --reload
```

### No puedo ver http://127.0.0.1:8000/docs:
```bash
# El servidor puede estar en otro puerto, mira en terminal:
# "Uvicorn running on http://0.0.0.0:8000"
# Intenta: http://localhost:8000/docs
```

### Un archivo no abre en VS Code:
```bash
# Desde terminal:
code <archivo_path>
# Ejemplo: code src/main.py
```

### Necesito reset urgente:
```bash
# Borra venv y recrea:
rmdir /s .venv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
# Espera 3-5 min
```

---

## NOTAS FINALES

- Si la demo falla, muestras el código. La arquitectura sigue siendo valida.
- Si no recuerdas que decir, mira CHEAT_SHEET_PUNTOS_CLAVE.md
- Si pierdes el hilo, vuelve a "el sistema tiene 7 capas"
- Timing es flexible: demo puede ser 8-12 min, el resto se ajusta
- ¡Buena suerte!
