"""
Tareas de Celery para ejecutar los formularios RPA

Este módulo define las tareas de Celery que ejecutan el llenado
automático de los formularios de Colsubsidio.
"""

from app.celery_app import celery_app
import sys
import os

# Agregar el directorio raíz al path para importar los scripts de formularios
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Importar las clases de los formularios
from form1 import ColsubsidioFormFiller as Form1Filler
from form2 import ColsubsidioFormFiller as Form2Filler
from form3 import ColsubsidioFormFiller as Form3Filler
from form4 import ColsubsidioFormFiller as Form4Filler


# Mapeo de tipos de formulario a sus clases
FORM_FILLERS = {
    'form1': Form1Filler,
    'form2': Form2Filler,
    'form3': Form3Filler,
    'form4': Form4Filler,
}


@celery_app.task(bind=True, name='app.tasks.execute_form_task', max_retries=3)
def execute_form_task(self, form_type: str, data: dict):
    """
    Tarea de Celery para ejecutar el llenado de un formulario
    
    Args:
        self: Referencia a la tarea (bind=True)
        form_type: Tipo de formulario ('form1', 'form2', 'form3', 'form4')
        data: Datos del formulario en formato diccionario
        
    Returns:
        dict: Resultado de la ejecución con status y mensaje
        
    Raises:
        Exception: Si ocurre un error durante la ejecución
    """
    try:
        # Actualizar estado de la tarea
        self.update_state(
            state='STARTED',
            meta={'status': f'Iniciando llenado de {form_type}...'}
        )
        
        # Obtener la clase del formulario
        form_filler_class = FORM_FILLERS.get(form_type)
        if not form_filler_class:
            raise ValueError(f"Tipo de formulario inválido: {form_type}")
        
        # Ejecutar el llenado del formulario
        self.update_state(
            state='PROGRESS',
            meta={'status': f'Ejecutando {form_type}...'}
        )
        
        filler = form_filler_class()
        filler.ejecutar(data)
        
        # Retornar resultado exitoso
        return {
            'status': 'completed',
            'message': f'Formulario {form_type} completado exitosamente',
            'form_type': form_type
        }
        
    except Exception as e:
        # Registrar el error
        error_message = f"Error ejecutando {form_type}: {str(e)}"
        print(error_message)
        
        # Reintentar la tarea si no se ha alcanzado el máximo de reintentos
        try:
            raise self.retry(exc=e, countdown=60)  # Reintentar después de 60 segundos
        except self.MaxRetriesExceededError:
            # Si se excedieron los reintentos, retornar error
            return {
                'status': 'failed',
                'message': error_message,
                'form_type': form_type,
                'error': str(e)
            }
