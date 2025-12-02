"""
Script para ejecutar el worker de Celery localmente (sin Docker)

Este script inicia un worker de Celery que procesa las tareas de llenado
de formularios. Usa el pool 'solo' para compatibilidad con Windows.

Uso:
    python run_celery.py
"""

import os
import sys

# Asegurar que el directorio raíz está en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.celery_app import celery_app

if __name__ == '__main__':
    # Configurar argumentos para el worker
    argv = [
        'worker',
        '--loglevel=info',
        '--pool=solo',  # Pool 'solo' para Windows
        '--concurrency=1',
    ]
    
    print("=" * 60)
    print("Iniciando Celery Worker para Formularios Colsubsidio")
    print("=" * 60)
    print(f"Broker: {celery_app.conf.broker_url}")
    print(f"Backend: {celery_app.conf.result_backend}")
    print("=" * 60)
    print("\nPresiona Ctrl+C para detener el worker\n")
    
    # Iniciar el worker
    celery_app.worker_main(argv)
