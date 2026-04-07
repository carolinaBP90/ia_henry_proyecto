# Script de Inicializacion Rapida - Ejecutar 10 minutos antes de presentar

## PARA WINDOWS (PowerShell)

Abre PowerShell en la carpeta del proyecto y copia/pega esto:

```powershell
# 1. Activar venv
.\.venv\Scripts\Activate.ps1

# 2. Verificar que pip install funciono
pip list | findstr fastapi

# 2.1 Variables necesarias para demo principal
$env:OPENAI_API_KEY = "tu_openai_key"
$env:LANGFUSE_ENABLED = "true"
$env:LANGFUSE_PUBLIC_KEY = "tu_public_key"
$env:LANGFUSE_SECRET_KEY = "tu_secret_key"

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

# 2.1 Variables necesarias para demo principal
export OPENAI_API_KEY="tu_openai_key"
export LANGFUSE_ENABLED="true"
export LANGFUSE_PUBLIC_KEY="tu_public_key"
export LANGFUSE_SECRET_KEY="tu_secret_key"

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

### Paso 2.1: Preparar comando principal (CLI)
```bash
python -m src.main "C:/ruta/contrato_original.png" "C:/ruta/adenda.png" --output-file resultado.json
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
TAB 4: src/image_parser.py
TAB 5: src/agents/contextualization_agent.py
TAB 6: src/agents/extraction_agent.py
TAB 7: src/models.py
TAB 8: src/services/tracing.py
TAB 9: src/api/routes/pipeline.py
TAB 10: src/api/routes/health.py
TAB 14: requirements.txt
TAB 15: docker-compose.yml
TAB 16: Dockerfile
```

O mas simple: Abre solo estos archivos principales:
```
- src/main.py
- src/image_parser.py
- src/agents/contextualization_agent.py
- src/agents/extraction_agent.py
- src/models.py
- src/services/tracing.py
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
        |  - main.py paso a paso        | VS Code: main.py
        |  - image_parser.py            | VS Code: image_parser.py
        |  - contextualization_agent.py | VS Code: agents/contextualization_agent.py
        |  - extraction_agent.py        | VS Code: agents/extraction_agent.py
        |  - models.py                  | VS Code: models.py
        |                               |
22 min  | DEMO CLI PRINCIPAL            | Terminal: python -m src.main <img1> <img2>
        | (mientras trabajas)           |
        |                               |
24 min  | Abrir resultado JSON          | resultado.json
        |                               |
24-32   | DEMO EN VIVO:                 | Browser: Swagger
        |  - Mostrar spans Langfuse     | Dashboard Langfuse
        |  - API opcional (si hay tiempo)| POST /pipeline/process-image
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

1. **main.py** (5 min)
        - Es el corazón, muestra el flujo completo contractual
        - Path: `src/main.py`

2. **image_parser.py** (2 min)
        - OCR multimodal + validaciones de imagen
        - Path: `src/image_parser.py`

3. **contextualization_agent.py** (2 min)
        - Agente 1, mapa contextual
        - Path: `src/agents/contextualization_agent.py`

4. **extraction_agent.py** (2 min)
        - Agente 2, JSON de cambios
        - Path: `src/agents/extraction_agent.py`

5. **models.py** (1 min)
        - Validacion ContractChangeOutput
        - Path: `src/models.py`

6. **tracing.py** (1 min)
        - Trazabilidad Langfuse por spans
        - Path: `src/services/tracing.py`

---

## QUICK LAUNCH CHECKLIST (ULTIMO MINUTO)

```
⬜ Terminal 1: `cd proyecto && .venv\Scripts\activate`
⬜ Terminal 1: `python -m src.main <img_original> <img_adenda> --output-file resultado.json`
⬜ Esperar: "Uvicorn running on http://127.0.0.1:8000"
⬜ VS Code: abierto con archivos lista
⬜ Browser: dashboard Langfuse abierto
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
pip install -r requirements.txt

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
