# API Formularios Colsubsidio

API REST para automatizar el llenado de formularios de evaluación de Preescolar Integrales de Colsubsidio Bogotá y Cundinamarca usando FastAPI, Celery, Redis y Selenium.

## ✨ Características

- **API REST** con FastAPI para endpoints HTTP
- **Procesamiento asíncrono** con Celery y Redis
- **Automatización RPA** con Selenium WebDriver
- **Docker Compose** para fácil despliegue
- **Seguimiento de tareas** en tiempo real

## Descripción

Este proyecto convierte los scripts de automatización de formularios Python en una API REST que permite llenar los formularios mediante peticiones HTTP con JSON.

## Formularios Disponibles

| Formulario | Endpoint | URL Qualtrics |
|------------|----------|---------------|
| Form 1 | `/api/forms/form1` | https://colsubsidio.az1.qualtrics.com/jfe/form/SV_dhz8RuGCTqJm1Ui |
| Form 2 | `/api/forms/form2` | https://colsubsidio.az1.qualtrics.com/jfe/form/SV_6VaaNLR3jmRV4pw |
| Form 3 | `/api/forms/form3` | https://colsubsidio.az1.qualtrics.com/jfe/form/SV_cZQUXOINZrCcUx8 |
| Form 4 | `/api/forms/form4` | https://colsubsidio.az1.qualtrics.com/jfe/form/SV_39rtVbeLsFoU9Bc |

## 🚀 Inicio Rápido con Docker Compose (Recomendado)

### Requisitos Previos
- Docker y Docker Compose instalados
- ChromeDriver (incluido en la imagen Docker)

### Iniciar todos los servicios

```bash
# Iniciar Redis, Celery worker y FastAPI
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

El servidor estará disponible en: `http://localhost:8000`

## 💻 Instalación Local (Desarrollo)

### Requisitos Previos
- Python 3.9+
- Redis instalado y ejecutándose
- ChromeDriver instalado y en el PATH

### Pasos

1. **Clonar el repositorio**:
```bash
git clone <url-del-repositorio>
cd forms-sebas
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Iniciar Redis** (si no está usando Docker):
```bash
# En Windows con WSL2
wsl redis-server

# O con Docker
docker run -d -p 6379:6379 redis:alpine
```

4. **Iniciar el worker de Celery** (en una terminal):
```bash
python run_celery.py
```

5. **Iniciar el servidor FastAPI** (en otra terminal):
```bash
python run_server.py
# O directamente con uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📖 Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔄 Flujo de Trabajo

1. **Enviar formulario**: POST a `/api/forms/form{1-4}` → Recibe `task_id`
2. **Consultar estado**: GET a `/api/forms/task/{task_id}` → Ver progreso
3. **Esperar completación**: Estado cambia de PENDING → STARTED → SUCCESS

### Ejemplos de Uso

#### Formulario 1

```bash
curl -X POST "http://localhost:8000/api/forms/form1" \
  -H "Content-Type: application/json" \
  -d '{
    "institucion": "Colegio San José",
    "proyecto": "Preescolar Integral 2025",
    "recomendacion": 10,
    "recomendacion_text": "Excelente programa",
    "satisfaccion": 10,
    "satisfaccion_text": "Muy satisfecho",
    "pagina_2": {
      "atencion": [10, 10, 10, 10, 10, 10, 10],
      "talento_humano": [10, 10, 10, 10, 10, 10, 10, 10, 10],
      "psicosocial": [10, 10, 10, 10, 10, 10, 10],
      "dinamizadores": [10, 10, 10, 10, 10, 10, 10],
      "contacto_dinamizador": "Si",
      "aspectos_dinamizador": [10, 10, 10, 10, 10, 10, 10],
      "contacto_coordinador": "Si",
      "aspectos_satisfaccion": [10, 10, 10, 10, 10],
      "pqrs_medios": ["Pagina web", "Correo electronico"],
      "ha_reclamado": "No",
      "desarrollo_propuesta": [10, 10, 10, 10, 10, 10, 10],
      "sugerencias": "Excelente programa"
    }
  }'
```

#### Formulario 2

```bash
curl -X POST "http://localhost:8000/api/forms/form2" \
  -H "Content-Type: application/json" \
  -d '{
    "lugar": "Colegio San José",
    "nombre_proyecto": "Preescolar Integral 2025",
    "recomendacion": 9,
    "satisfaccion": 9,
    "pagina_2": {
      "proceso_aprendizaje": [10, 10, 10, 10],
      "habilidades_docentes": [10, 10, 10, 10, 10, 10, 10],
      "auxiliar_salud_nutricion": [10, 10, 10, 10],
      "personal_administrativo": [10, 10, 10, 10],
      "actividades_administrativas": [10, 10, 10, 10],
      "alimentacion": [10, 10, 10],
      "desarrollo_propuesta": [10, 10, 10, 10],
      "profesionales_psicosocial": [10, 10, 10, 10, 10],
      "nutricionista": [10, 10, 10, 10, 10],
      "evaluacion_aspectos": [10, 10, 10, 10, 10],
      "apoyo_piscosocial": "No",
      "contacto_nutricionista": "Si",
      "especialista_desarrollo": "Si",
      "pqrs_medios": ["Pagina web"],
      "ha_reclamado": "No",
      "sugerencias": "Muy buen programa"
    }
  }'
```

#### Formulario 3

```bash
curl -X POST "http://localhost:8000/api/forms/form3" \
  -H "Content-Type: application/json" \
  -d '{
    "lugar": "Colegio San José",
    "nombre_proyecto": "Preescolar Integral 2025",
    "unidad": "Unidad Educativa Bogotá",
    "recomendacion": 9,
    "satisfaccion": 9,
    "pagina_2": {
      "proceso_aprendizaje": [10, 10, 10, 10],
      "habilidades_docentes": [10, 10, 10, 10, 10, 10, 10],
      "auxiliar_salud_nutricion": [10, 10, 10, 10],
      "personal_administrativo": [10, 10, 10, 10],
      "actividades_administrativas": [10, 10, 10, 10],
      "alimentacion": [10, 10, 10],
      "desarrollo_propuesta": [10, 10, 10, 10],
      "profesionales_psicosocial": [10, 10, 10, 10, 10],
      "nutricionista": [10, 10, 10, 10, 10],
      "evaluacion_aspectos": [10, 10, 10, 10, 10],
      "coordinador_zona": [10, 10, 10, 10],
      "apoyo_piscosocial": "No",
      "contacto_nutricionista": "Si",
      "especialista_desarrollo": "Si",
      "pqrs_medios": ["Pagina web"],
      "ha_reclamado": "No",
      "sugerencias": "Muy buen programa"
    }
  }'
```

#### Formulario 4

```bash
curl -X POST "http://localhost:8000/api/forms/form4" \
  -H "Content-Type: application/json" \
  -d '{
    "lugar": "Colegio San José",
    "nombre_proyecto": "Preescolar Integral 2025",
    "recomendacion": 9,
    "satisfaccion": 9,
    "pagina_2": {
      "proceso_aprendizaje": [10, 10, 10, 10],
      "acompanamiento_familia": [10, 10, 10, 10, 10],
      "habilidades_docentes": [10, 10, 10, 10, 10, 10, 10],
      "auxiliar_salud_nutricion": [10, 10, 10, 10],
      "personal_administrativo": [10, 10, 10, 10],
      "actividades_administrativas": [10, 10, 10, 10],
      "coordinador_pedagogico": [10, 10, 10, 10],
      "alimentacion": [10, 10, 10],
      "desarrollo_propuesta": [10, 10, 10, 10],
      "profesionales_psicosocial": [10, 10, 10, 10, 10],
      "nutricionista": [10, 10, 10, 10, 10],
      "evaluacion_aspectos": [10, 10, 10, 10, 10],
      "apoyo_piscosocial": "No",
      "contacto_nutricionista": "Si",
      "especialista_desarrollo": "Si",
      "pqrs_medios": ["Pagina web"],
      "ha_reclamado": "No",
      "sugerencias": "Muy buen programa"
    }
  }'
```

## Estructura del Proyecto

```
forms-sebas/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI principal
│   ├── models/              # Modelos Pydantic (schemas JSON)
│   │   ├── __init__.py
│   │   ├── form1_models.py
│   │   ├── form2_models.py
│   │   ├── form3_models.py
│   │   └── form4_models.py
│   └── routers/             # Endpoints de la API
│       ├── __init__.py
│       └── forms.py
├── form1.py                 # Script original de formulario 1
├── form2.py                 # Script original de formulario 2
├── form3.py                 # Script original de formulario 3
├── form4.py                 # Script original de formulario 4
├── run_server.py            # Script de inicio del servidor
├── requirements.txt         # Dependencias
└── README.md               # Este archivo
```

## 📡 Endpoints de la API

### `POST /api/forms/form{1-4}`
Encola un formulario para ser llenado. Retorna un `task_id` para seguimiento.

**Respuesta**:
```json
{
  "success": true,
  "message": "Formulario encolado exitosamente...",
  "form_type": "form1",
  "task_id": "abc-123-def-456"
}
```

### `GET /api/forms/task/{task_id}`
Consulta el estado de una tarea.

**Respuesta**:
```json
{
  "task_id": "abc-123",
  "status": "SUCCESS",
  "result": {"status": "completed", "message": "..."},
  "error": null,
  "meta": null
}
```

**Estados posibles**: `PENDING`, `STARTED`, `PROGRESS`, `SUCCESS`, `FAILURE`, `RETRY`

### `GET /api/forms/health`
Verifica el estado de la API y workers de Celery.

### `GET /`
Información general de la API.

## 🔍 Ejemplo Completo: Enviar y Monitorear Tarea

```bash
# 1. Enviar formulario
RESPONSE=$(curl -X POST "http://localhost:8000/api/forms/form1" \
  -H "Content-Type: application/json" \
  -d '{"institucion": "Colegio Test", ...}')

echo $RESPONSE
# {"success":true,"message":"...","form_type":"form1","task_id":"abc-123"}

# 2. Extraer task_id
TASK_ID=$(echo $RESPONSE | jq -r '.task_id')

# 3. Consultar estado
curl "http://localhost:8000/api/forms/task/$TASK_ID"
```

## ⚙️ Arquitectura

```
┌─────────────┐      ┌──────────────┐      ┌───────────────┐
│   Cliente   │─────▶│   FastAPI    │─────▶│  Redis Queue  │
└─────────────┘      └──────────────┘      └───────────────┘
                            │                       │
                            │                       ▼
                            │              ┌───────────────┐
                            │              │ Celery Worker │
                            │              └───────────────┘
                            │                       │
                            │                       ▼
                            │              ┌───────────────┐
                            └─────────────▶│   Selenium    │
                                           │   (Browser)   │
                                           └───────────────┘
```

## ⚠️ Notas Importantes

- Los formularios se ejecutan **asíncronamente** con Celery para no bloquear la API
- **Redis** es necesario como broker de mensajes y almacén de resultados
- Se requiere **ChromeDriver** (incluido en Docker, manual en instalación local)
- Los formularios interactúan con sitios web externos (Qualtrics)
- Conexión a internet estable requerida
- Los valores de las escalas deben estar en el rango correcto (1-10 o 0-10)
- Las tareas tienen un timeout de 30 minutos
- Los resultados expiran después de 1 hora

## 🛠️ Comandos Útiles

### Docker Compose
```bash
# Ver logs del worker
docker-compose logs -f celery-worker

# Ver logs de la API
docker-compose logs -f fastapi

# Reiniciar un servicio
docker-compose restart celery-worker

# Ver estado de servicios
docker-compose ps
```

### Desarrollo Local
```bash
# Verificar Redis
redis-cli ping  # Debe responder PONG

# Ver tareas en cola
celery -A app.celery_app inspect active

# Purgar todas las tareas
celery -A app.celery_app purge
```

## 🐛 Troubleshooting

**Error: "No se puede conectar a Redis"**
- Verificar que Redis esté ejecutándose: `docker-compose ps` o `redis-cli ping`
- Verificar variable de entorno `REDIS_URL`

**Error: "No hay workers disponibles"**
- Verificar que el worker de Celery esté ejecutándose
- Ver logs: `docker-compose logs celery-worker`

**Tarea en estado PENDING por mucho tiempo**
- El worker puede estar ocupado con otras tareas
- Verificar logs del worker para errores

## Licencia

MIT
