"""
Servidor FastAPI para automatización de formularios de Colsubsidio

Este servidor proporciona endpoints REST para llenar automáticamente
los formularios de evaluación de Preescolar Integrales usando Selenium.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import forms_router

# Crear la aplicación FastAPI
app = FastAPI(
    title="API Formularios Colsubsidio",
    description="""
    API REST para automatizar el llenado de formularios de evaluación
    de Preescolar Integrales de Colsubsidio Bogotá y Cundinamarca.

    ## Formularios disponibles:

    * **Form 1**: Evaluación Preescolar Integrales v1
    * **Form 2**: Evaluación Preescolar Integrales v2
    * **Form 3**: Evaluación Preescolar Integrales v3
    * **Form 4**: Evaluación Preescolar Integrales v4

    ## Uso:

    Cada endpoint recibe un JSON con la estructura específica del formulario
    y ejecuta el llenado automático usando Selenium WebDriver.

    Los formularios se ejecutan en segundo plano (background tasks) para
    no bloquear la respuesta de la API.
    """,
    version="1.0.0",
    contact={
        "name": "Soporte",
        "email": "soporte@example.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(forms_router)


@app.get("/")
async def root():
    """
    Endpoint raíz de la API
    """
    return {
        "message": "API de Formularios Colsubsidio",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "form1": "/api/forms/form1",
            "form2": "/api/forms/form2",
            "form3": "/api/forms/form3",
            "form4": "/api/forms/form4",
            "health": "/api/forms/health"
        }
    }


@app.get("/health")
async def health():
    """
    Verificar el estado de la API
    """
    return {
        "status": "healthy",
        "message": "API funcionando correctamente"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
