# API Formularios Colsubsidio

API REST para automatizar el llenado de formularios de evaluación de Preescolar Integrales de Colsubsidio Bogotá y Cundinamarca usando FastAPI y Selenium.

## Descripción

Este proyecto convierte los scripts de automatización de formularios Python en una API REST que permite llenar los formularios mediante peticiones HTTP con JSON.

## Formularios Disponibles

| Formulario | Endpoint | URL Qualtrics |
|------------|----------|---------------|
| Form 1 | `/api/forms/form1` | https://colsubsidio.az1.qualtrics.com/jfe/form/SV_dhz8RuGCTqJm1Ui |
| Form 2 | `/api/forms/form2` | https://colsubsidio.az1.qualtrics.com/jfe/form/SV_6VaaNLR3jmRV4pw |
| Form 3 | `/api/forms/form3` | https://colsubsidio.az1.qualtrics.com/jfe/form/SV_cZQUXOINZrCcUx8 |
| Form 4 | `/api/forms/form4` | https://colsubsidio.az1.qualtrics.com/jfe/form/SV_39rtVbeLsFoU9Bc |

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd forms-sebas
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Asegurarse de tener ChromeDriver instalado y en el PATH del sistema.

## Uso

### Iniciar el servidor

Opción 1: Usando el script de inicio
```bash
python run_server.py
```

Opción 2: Usando uvicorn directamente
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: `http://localhost:8000`

### Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

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

## Endpoints de la API

### `POST /api/forms/form1`
Llena el formulario 1 con los datos proporcionados en JSON.

### `POST /api/forms/form2`
Llena el formulario 2 con los datos proporcionados en JSON.

### `POST /api/forms/form3`
Llena el formulario 3 con los datos proporcionados en JSON.

### `POST /api/forms/form4`
Llena el formulario 4 con los datos proporcionados en JSON.

### `GET /api/forms/health`
Verifica el estado de la API.

### `GET /`
Información general de la API.

## Respuestas de la API

Todas las respuestas exitosas siguen el formato:

```json
{
  "success": true,
  "message": "Formulario X en proceso de llenado. Se ejecutará en segundo plano.",
  "form_type": "formX"
}
```

En caso de error:

```json
{
  "detail": "Descripción del error"
}
```

## Notas Importantes

- Los formularios se ejecutan en **segundo plano** (background tasks) para no bloquear la API
- Se requiere **ChromeDriver** instalado en el sistema
- Los formularios interactúan con sitios web externos (Qualtrics)
- Asegúrate de tener una conexión a internet estable
- Los valores de las escalas deben estar en el rango correcto (1-10 o 0-10 según corresponda)

## Desarrollo

Para ejecutar el servidor en modo de desarrollo con recarga automática:

```bash
uvicorn app.main:app --reload
```

## Licencia

MIT
