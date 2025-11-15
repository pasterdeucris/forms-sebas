"""
Endpoints de la API para llenar los formularios automatizados
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models import (
    Form1Request,
    Form2Request,
    Form3Request,
    Form4Request,
    FormResponse
)
import sys
import os

# Agregar el directorio raíz al path para importar los scripts de formularios
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Importar las clases de los formularios
from form1 import ColsubsidioFormFiller as Form1Filler
from form2 import ColsubsidioFormFiller as Form2Filler
from form3 import ColsubsidioFormFiller as Form3Filler
from form4 import ColsubsidioFormFiller as Form4Filler

router = APIRouter(
    prefix="/api/forms",
    tags=["Formularios"]
)


def execute_form_filler(form_filler_class, data: dict):
    """
    Ejecuta el llenado de un formulario en el background

    Args:
        form_filler_class: Clase del formulario a ejecutar
        data: Datos del formulario
    """
    try:
        filler = form_filler_class()
        filler.ejecutar(data)
    except Exception as e:
        print(f"Error ejecutando formulario: {e}")
        raise


@router.post("/form1", response_model=FormResponse)
async def llenar_formulario_1(request: Form1Request, background_tasks: BackgroundTasks):
    """
    Llena el Formulario 1 - Evaluación Preescolar Integrales v1

    **Descripción**: Este endpoint recibe los datos del formulario 1 y ejecuta
    el proceso de llenado automático usando Selenium.

    **URL del formulario**: https://colsubsidio.az1.qualtrics.com/jfe/form/SV_dhz8RuGCTqJm1Ui
    """
    try:
        # Convertir el modelo Pydantic a diccionario
        datos = request.model_dump()

        # Ejecutar el formulario en background
        background_tasks.add_task(execute_form_filler, Form1Filler, datos)

        return FormResponse(
            success=True,
            message="Formulario 1 en proceso de llenado. Se ejecutará en segundo plano.",
            form_type="form1"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando formulario: {str(e)}")


@router.post("/form2", response_model=FormResponse)
async def llenar_formulario_2(request: Form2Request, background_tasks: BackgroundTasks):
    """
    Llena el Formulario 2 - Evaluación Preescolar Integrales v2

    **Descripción**: Este endpoint recibe los datos del formulario 2 y ejecuta
    el proceso de llenado automático usando Selenium.

    **URL del formulario**: https://colsubsidio.az1.qualtrics.com/jfe/form/SV_6VaaNLR3jmRV4pw
    """
    try:
        # Convertir el modelo Pydantic a diccionario
        datos = request.model_dump()

        # Ejecutar el formulario en background
        background_tasks.add_task(execute_form_filler, Form2Filler, datos)

        return FormResponse(
            success=True,
            message="Formulario 2 en proceso de llenado. Se ejecutará en segundo plano.",
            form_type="form2"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando formulario: {str(e)}")


@router.post("/form3", response_model=FormResponse)
async def llenar_formulario_3(request: Form3Request, background_tasks: BackgroundTasks):
    """
    Llena el Formulario 3 - Evaluación Preescolar Integrales v3

    **Descripción**: Este endpoint recibe los datos del formulario 3 y ejecuta
    el proceso de llenado automático usando Selenium.

    **URL del formulario**: https://colsubsidio.az1.qualtrics.com/jfe/form/SV_cZQUXOINZrCcUx8
    """
    try:
        # Convertir el modelo Pydantic a diccionario
        datos = request.model_dump()

        # Ejecutar el formulario en background
        background_tasks.add_task(execute_form_filler, Form3Filler, datos)

        return FormResponse(
            success=True,
            message="Formulario 3 en proceso de llenado. Se ejecutará en segundo plano.",
            form_type="form3"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando formulario: {str(e)}")


@router.post("/form4", response_model=FormResponse)
async def llenar_formulario_4(request: Form4Request, background_tasks: BackgroundTasks):
    """
    Llena el Formulario 4 - Evaluación Preescolar Integrales v4

    **Descripción**: Este endpoint recibe los datos del formulario 4 y ejecuta
    el proceso de llenado automático usando Selenium.

    **URL del formulario**: https://colsubsidio.az1.qualtrics.com/jfe/form/SV_39rtVbeLsFoU9Bc
    """
    try:
        # Convertir el modelo Pydantic a diccionario
        datos = request.model_dump()

        # Ejecutar el formulario en background
        background_tasks.add_task(execute_form_filler, Form4Filler, datos)

        return FormResponse(
            success=True,
            message="Formulario 4 en proceso de llenado. Se ejecutará en segundo plano.",
            form_type="form4"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando formulario: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Verifica el estado de la API
    """
    return {
        "status": "healthy",
        "message": "API de formularios funcionando correctamente",
        "endpoints_disponibles": [
            "/api/forms/form1",
            "/api/forms/form2",
            "/api/forms/form3",
            "/api/forms/form4"
        ]
    }
