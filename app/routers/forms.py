"""
Endpoints de la API para llenar los formularios automatizados
"""

from fastapi import APIRouter, HTTPException
from app.models import (
    Form1Request,
    Form2Request,
    Form3Request,
    Form4Request,
    FormResponse,
    TaskStatusResponse
)
from app.tasks import execute_form_task
from app.celery_app import celery_app

router = APIRouter(
    prefix="/api/forms",
    tags=["Formularios"]
)


@router.post("/form1", response_model=FormResponse)
async def llenar_formulario_1(request: Form1Request):
    """
    Llena el Formulario 1 - Evaluación Preescolar Integrales v1

    **Descripción**: Este endpoint recibe los datos del formulario 1 y ejecuta
    el proceso de llenado automático usando Selenium.

    **URL del formulario**: https://colsubsidio.az1.qualtrics.com/jfe/form/SV_dhz8RuGCTqJm1Ui
    
    **Retorna**: Un objeto con el task_id que puede usarse para consultar el estado
    de la tarea en el endpoint /api/forms/task/{task_id}
    """
    try:
        # Convertir el modelo Pydantic a diccionario
        datos = request.model_dump()

        # Ejecutar el formulario en Celery
        task = execute_form_task.delay('form1', datos)

        return FormResponse(
            success=True,
            message="Formulario 1 encolado exitosamente. Use el task_id para consultar el estado.",
            form_type="form1",
            task_id=task.id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando formulario: {str(e)}")


@router.post("/form2", response_model=FormResponse)
async def llenar_formulario_2(request: Form2Request):
    """
    Llena el Formulario 2 - Evaluación Preescolar Integrales v2

    **Descripción**: Este endpoint recibe los datos del formulario 2 y ejecuta
    el proceso de llenado automático usando Selenium.

    **URL del formulario**: https://colsubsidio.az1.qualtrics.com/jfe/form/SV_6VaaNLR3jmRV4pw
    
    **Retorna**: Un objeto con el task_id que puede usarse para consultar el estado
    de la tarea en el endpoint /api/forms/task/{task_id}
    """
    try:
        # Convertir el modelo Pydantic a diccionario
        datos = request.model_dump()

        # Ejecutar el formulario en Celery
        task = execute_form_task.delay('form2', datos)

        return FormResponse(
            success=True,
            message="Formulario 2 encolado exitosamente. Use el task_id para consultar el estado.",
            form_type="form2",
            task_id=task.id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando formulario: {str(e)}")


@router.post("/form3", response_model=FormResponse)
async def llenar_formulario_3(request: Form3Request):
    """
    Llena el Formulario 3 - Evaluación Preescolar Integrales v3

    **Descripción**: Este endpoint recibe los datos del formulario 3 y ejecuta
    el proceso de llenado automático usando Selenium.

    **URL del formulario**: https://colsubsidio.az1.qualtrics.com/jfe/form/SV_cZQUXOINZrCcUx8
    
    **Retorna**: Un objeto con el task_id que puede usarse para consultar el estado
    de la tarea en el endpoint /api/forms/task/{task_id}
    """
    try:
        # Convertir el modelo Pydantic a diccionario
        datos = request.model_dump()

        # Ejecutar el formulario en Celery
        task = execute_form_task.delay('form3', datos)

        return FormResponse(
            success=True,
            message="Formulario 3 encolado exitosamente. Use el task_id para consultar el estado.",
            form_type="form3",
            task_id=task.id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando formulario: {str(e)}")


@router.post("/form4", response_model=FormResponse)
async def llenar_formulario_4(request: Form4Request):
    """
    Llena el Formulario 4 - Evaluación Preescolar Integrales v4

    **Descripción**: Este endpoint recibe los datos del formulario 4 y ejecuta
    el proceso de llenado automático usando Selenium.

    **URL del formulario**: https://colsubsidio.az1.qualtrics.com/jfe/form/SV_39rtVbeLsFoU9Bc
    
    **Retorna**: Un objeto con el task_id que puede usarse para consultar el estado
    de la tarea en el endpoint /api/forms/task/{task_id}
    """
    try:
        # Convertir el modelo Pydantic a diccionario
        datos = request.model_dump()

        # Ejecutar el formulario en Celery
        task = execute_form_task.delay('form4', datos)

        return FormResponse(
            success=True,
            message="Formulario 4 encolado exitosamente. Use el task_id para consultar el estado.",
            form_type="form4",
            task_id=task.id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando formulario: {str(e)}")


@router.get("/task/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """
    Consulta el estado de una tarea de Celery
    
    **Descripción**: Este endpoint permite consultar el estado de una tarea
    previamente encolada usando su task_id.
    
    **Estados posibles**:
    - PENDING: La tarea está esperando ser ejecutada
    - STARTED: La tarea ha comenzado a ejecutarse
    - PROGRESS: La tarea está en progreso
    - SUCCESS: La tarea se completó exitosamente
    - FAILURE: La tarea falló
    - RETRY: La tarea está siendo reintentada
    """
    try:
        task_result = celery_app.AsyncResult(task_id)
        
        response = TaskStatusResponse(
            task_id=task_id,
            status=task_result.status,
            result=task_result.result if task_result.successful() else None,
            error=str(task_result.info) if task_result.failed() else None,
            meta=task_result.info if task_result.state in ['STARTED', 'PROGRESS'] else None
        )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando tarea: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Verifica el estado de la API y la conexión con Celery/Redis
    """
    try:
        # Verificar conexión con Redis/Celery
        inspector = celery_app.control.inspect()
        active_workers = inspector.active()
        
        return {
            "status": "healthy",
            "message": "API de formularios funcionando correctamente",
            "celery_workers": len(active_workers) if active_workers else 0,
            "endpoints_disponibles": [
                "/api/forms/form1",
                "/api/forms/form2",
                "/api/forms/form3",
                "/api/forms/form4",
                "/api/forms/task/{task_id}"
            ]
        }
    except Exception as e:
        return {
            "status": "degraded",
            "message": "API funcionando pero Celery no está disponible",
            "error": str(e),
            "endpoints_disponibles": [
                "/api/forms/form1",
                "/api/forms/form2",
                "/api/forms/form3",
                "/api/forms/form4",
                "/api/forms/task/{task_id}"
            ]
        }

