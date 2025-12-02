"""
Configuración de Celery para la aplicación de formularios

Este módulo configura Celery con Redis como broker y backend de resultados.
"""

from celery import Celery
import os

# Configurar la URL de Redis desde variable de entorno o usar localhost por defecto
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Crear la instancia de Celery
celery_app = Celery(
    'formularios_colsubsidio',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['app.tasks']
)

# Configuración de Celery
celery_app.conf.update(
    # Serialización
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
    # Timezone
    timezone='America/Bogota',
    enable_utc=True,
    
    # Configuración de tareas
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutos máximo por tarea
    task_soft_time_limit=25 * 60,  # 25 minutos soft limit
    
    # Resultados
    result_expires=3600,  # Los resultados expiran después de 1 hora
    result_extended=True,
    
    # Reintentos
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    
    # Worker
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
)

if __name__ == '__main__':
    celery_app.start()
