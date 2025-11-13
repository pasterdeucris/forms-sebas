"""
API REST con FastAPI para automatizar el formulario de Qualtrics

Opcional: Si quieres exponer la automatización como un servicio web
Ejecuta con: uvicorn app:app --reload
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from form_automation import QualtricsFormFiller
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear app FastAPI
app = FastAPI(
    title="Qualtrics Form Automation API",
    description="API para automatizar el llenado del formulario de Preescolar Integrales",
    version="1.0.0"
)


# Modelos de datos
class FormData(BaseModel):
    """Modelo para los datos del formulario"""
    text_fields: Optional[Dict[str, str]] = {}
    radio_buttons: Optional[List[str]] = []
    radio_by_value: Optional[Dict[str, str]] = {}
    checkboxes: Optional[Dict[str, bool]] = {}
    dropdowns: Optional[Dict[str, str]] = {}
    conditional_modals: Optional[List[Dict[str, Any]]] = []


class PageData(BaseModel):
    """Modelo para una página del formulario"""
    page_number: int
    name: str
    fields: FormData


class FormRequest(BaseModel):
    """Modelo para la petición completa"""
    form_url: str
    pages: List[PageData]
    headless: bool = True


class FormResponse(BaseModel):
    """Modelo para la respuesta"""
    success: bool
    message: str
    errors: Optional[List[str]] = None


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Qualtrics Form Automation API",
        "version": "1.0.0",
        "endpoints": {
            "POST /fill-form": "Llenar el formulario completo",
            "GET /health": "Verificar estado del servicio"
        }
    }


@app.get("/health")
async def health_check():
    """Verificar estado del servicio"""
    return {
        "status": "healthy",
        "service": "Qualtrics Form Automation"
    }


@app.post("/fill-form", response_model=FormResponse)
async def fill_form(request: FormRequest):
    """
    Llenar el formulario de Qualtrics

    Args:
        request: Datos del formulario a llenar

    Returns:
        FormResponse con el resultado de la operación
    """
    logger.info(f"Recibida petición para llenar formulario: {request.form_url}")

    errors = []
    form_filler = None

    try:
        # Inicializar el automatizador
        form_filler = QualtricsFormFiller(headless=request.headless)

        # Navegar al formulario
        form_filler.navigate_to_form(request.form_url)

        # Procesar cada página
        for page in request.pages:
            logger.info(f"Procesando {page.name}")

            # Convertir el modelo Pydantic a diccionario
            fields_dict = page.fields.dict()

            # Llenar la página
            form_filler.fill_form_page(fields_dict)

            # Avanzar a la siguiente página (excepto en la última)
            if page != request.pages[-1]:
                if not form_filler.click_next_button():
                    errors.append(f"No se pudo avanzar después de {page.name}")

        logger.info("Formulario completado exitosamente")

        return FormResponse(
            success=True,
            message="Formulario llenado exitosamente",
            errors=errors if errors else None
        )

    except Exception as e:
        logger.error(f"Error al llenar formulario: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al llenar el formulario: {str(e)}"
        )

    finally:
        if form_filler:
            form_filler.close()


@app.post("/test-connection")
async def test_connection(form_url: str):
    """
    Probar conexión al formulario sin llenarlo

    Args:
        form_url: URL del formulario

    Returns:
        Estado de la conexión
    """
    form_filler = None

    try:
        form_filler = QualtricsFormFiller(headless=True)
        form_filler.navigate_to_form(form_url)

        return {
            "success": True,
            "message": "Conexión exitosa al formulario",
            "url": form_url
        }

    except Exception as e:
        logger.error(f"Error al conectar con el formulario: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al conectar con el formulario: {str(e)}"
        )

    finally:
        if form_filler:
            form_filler.close()


# Ejemplo de cómo usar la API:
"""
# Ejecutar el servidor:
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Hacer una petición POST a /fill-form:
curl -X POST "http://localhost:8000/fill-form" \
  -H "Content-Type: application/json" \
  -d '{
    "form_url": "https://colsubsidio.az1.qualtrics.com/jfe/form/SV_dhz8RuGCTqJm1Ui",
    "headless": true,
    "pages": [
      {
        "page_number": 1,
        "name": "Página 1",
        "fields": {
          "text_fields": {
            "field_id": "valor"
          },
          "radio_buttons": ["Opción 1"]
        }
      }
    ]
  }'

# O usar Python requests:
import requests

data = {
    "form_url": "https://colsubsidio.az1.qualtrics.com/jfe/form/SV_dhz8RuGCTqJm1Ui",
    "headless": True,
    "pages": [
        {
            "page_number": 1,
            "name": "Página 1",
            "fields": {
                "text_fields": {"campo": "valor"},
                "radio_buttons": ["Sí"]
            }
        }
    ]
}

response = requests.post("http://localhost:8000/fill-form", json=data)
print(response.json())
"""


if __name__ == "__main__":
    import uvicorn

    # Ejecutar el servidor
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
