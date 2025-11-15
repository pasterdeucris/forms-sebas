"""
API FastAPI para gestión de formularios de Colsubsidio
Permite ejecutar los 4 formularios de manera programática
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid
from datetime import datetime
import traceback

# Importar los form fillers
from form1 import ColsubsidioFormFiller as FormFiller1
from form2 import ColsubsidioFormFiller as FormFiller2
from form3 import ColsubsidioFormFiller as FormFiller3
from form4 import ColsubsidioFormFiller as FormFiller4


# Crear instancia de FastAPI
app = FastAPI(
    title="API de Formularios Colsubsidio",
    description="API REST para automatizar el llenado de formularios de Colsubsidio",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelos de datos
class FormType(str, Enum):
    """Tipos de formularios disponibles"""
    FORM1 = "form1"
    FORM2 = "form2"
    FORM3 = "form3"
    FORM4 = "form4"


class TaskStatus(str, Enum):
    """Estados de las tareas"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class DatosPagina2Base(BaseModel):
    """Modelo base para datos de página 2 (común a todos los formularios)"""
    pqrs_medios: Optional[List[str]] = Field(default=None, description="Medios de PQRS")
    ha_reclamado: str = Field(default="No", description="¿Ha reclamado? (Si/No)")
    sugerencias: Optional[str] = Field(default=None, description="Sugerencias adicionales")


class DatosPagina2Form1(DatosPagina2Base):
    """Modelo para datos de página 2 del formulario 1"""
    atencion: Optional[List[int]] = Field(default=None, description="7 valores para atención")
    talento_humano: Optional[List[int]] = Field(default=None, description="9 valores para talento humano")
    psicosocial: Optional[List[int]] = Field(default=None, description="7 valores para psicosocial")
    dinamizadores: Optional[List[int]] = Field(default=None, description="7 valores para dinamizadores")
    contacto_dinamizador: str = Field(default="No", description="¿Contacto con dinamizador? (Si/No)")
    aspectos_dinamizador: Optional[List[int]] = Field(default=None, description="7 valores para aspectos dinamizador")
    contacto_coordinador: str = Field(default="Si", description="¿Contacto con coordinador? (Si/No)")
    aspectos_satisfaccion: Optional[List[int]] = Field(default=None, description="5 valores para aspectos satisfacción")
    desarrollo_propuesta: Optional[List[int]] = Field(default=None, description="7 valores para desarrollo propuesta")


class DatosPagina2Form2(DatosPagina2Base):
    """Modelo para datos de página 2 del formulario 2"""
    proceso_aprendizaje: Optional[List[int]] = Field(default=None, description="5 valores")
    habilidades_docentes: Optional[List[int]] = Field(default=None, description="7 valores")
    auxiliar_salud_nutricion: Optional[List[int]] = Field(default=None, description="4 valores")
    personal_administrativo: Optional[List[int]] = Field(default=None, description="4 valores")
    actividades_administrativas: Optional[List[int]] = Field(default=None, description="4 valores")
    alimentacion: Optional[List[int]] = Field(default=None, description="4 valores")
    desarrollo_propuesta: Optional[List[int]] = Field(default=None, description="7 valores")
    profesionales_psicosocial: Optional[List[int]] = Field(default=None, description="5 valores")
    nutricionista: Optional[List[int]] = Field(default=None, description="5 valores")
    evaluacion_aspectos: Optional[List[int]] = Field(default=None, description="5 valores")
    apoyo_piscosocial: str = Field(default="No", description="¿Apoyo psicosocial? (Si/No)")
    contacto_nutricionista: str = Field(default="Si", description="¿Contacto nutricionista? (Si/No)")
    especialista_desarrollo: str = Field(default="Si", description="¿Especialista desarrollo? (Si/No)")


class DatosPagina2Form3(DatosPagina2Form2):
    """Modelo para datos de página 2 del formulario 3 (similar a Form2 + coordinador_zona)"""
    coordinador_zona: Optional[List[int]] = Field(default=None, description="4 valores para coordinador zona")


class DatosPagina2Form4(DatosPagina2Form2):
    """Modelo para datos de página 2 del formulario 4 (similar a Form2 + campos adicionales)"""
    acompanamiento_familia: Optional[List[int]] = Field(default=None, description="5 valores")
    coordinador_pedagogico: Optional[List[int]] = Field(default=None, description="4 valores")


class FormularioRequestBase(BaseModel):
    """Modelo base para solicitud de formulario"""
    institucion: Optional[str] = Field(default=None, alias="lugar", description="Nombre de la institución")
    proyecto: Optional[str] = Field(default=None, alias="nombre_proyecto", description="Nombre del proyecto")
    recomendacion: int = Field(default=10, ge=0, le=10, description="Nivel de recomendación (0-10)")
    recomendacion_text: Optional[str] = Field(default="", description="Texto de recomendación (si < 9)")
    satisfaccion: int = Field(default=10, ge=1, le=10, description="Nivel de satisfacción (1-10)")
    satisfaccion_text: Optional[str] = Field(default="", description="Texto de satisfacción (si <= 6)")

    class Config:
        populate_by_name = True


class FormularioRequest1(FormularioRequestBase):
    """Modelo de solicitud para el formulario 1"""
    pagina_2: DatosPagina2Form1


class FormularioRequest2(FormularioRequestBase):
    """Modelo de solicitud para el formulario 2"""
    lugar: str = Field(..., description="Lugar")
    nombre_proyecto: str = Field(..., description="Nombre del proyecto")
    pagina_2: DatosPagina2Form2


class FormularioRequest3(FormularioRequestBase):
    """Modelo de solicitud para el formulario 3"""
    lugar: str = Field(..., description="Lugar")
    nombre_proyecto: str = Field(..., description="Nombre del proyecto")
    unidad: str = Field(..., description="Unidad educativa")
    pagina_2: DatosPagina2Form3


class FormularioRequest4(FormularioRequestBase):
    """Modelo de solicitud para el formulario 4"""
    lugar: str = Field(..., description="Lugar")
    nombre_proyecto: str = Field(..., description="Nombre del proyecto")
    pagina_2: DatosPagina2Form4


class TaskResponse(BaseModel):
    """Respuesta al crear una tarea"""
    task_id: str
    status: TaskStatus
    message: str
    created_at: datetime


class TaskDetailResponse(BaseModel):
    """Respuesta detallada de una tarea"""
    task_id: str
    status: TaskStatus
    form_type: FormType
    created_at: datetime
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    result: Optional[Dict[str, Any]] = None


# Almacenamiento en memoria de tareas (en producción usar base de datos)
tasks_storage: Dict[str, Dict[str, Any]] = {}


def ejecutar_formulario(task_id: str, form_type: FormType, datos: Dict[str, Any]):
    """
    Ejecuta un formulario en segundo plano
    """
    try:
        # Actualizar estado a running
        tasks_storage[task_id]["status"] = TaskStatus.RUNNING

        # Seleccionar el form filler correcto
        if form_type == FormType.FORM1:
            form_filler = FormFiller1()
        elif form_type == FormType.FORM2:
            form_filler = FormFiller2()
        elif form_type == FormType.FORM3:
            form_filler = FormFiller3()
        elif form_type == FormType.FORM4:
            form_filler = FormFiller4()
        else:
            raise ValueError(f"Tipo de formulario no válido: {form_type}")

        # Ejecutar el formulario
        form_filler.ejecutar(datos)

        # Actualizar estado a completado
        tasks_storage[task_id]["status"] = TaskStatus.COMPLETED
        tasks_storage[task_id]["completed_at"] = datetime.now()
        tasks_storage[task_id]["result"] = {"message": "Formulario completado exitosamente"}

    except Exception as e:
        # Actualizar estado a fallido
        tasks_storage[task_id]["status"] = TaskStatus.FAILED
        tasks_storage[task_id]["completed_at"] = datetime.now()
        tasks_storage[task_id]["error"] = str(e)
        tasks_storage[task_id]["traceback"] = traceback.format_exc()


# Endpoints de la API

@app.get("/", tags=["General"])
async def root():
    """Endpoint raíz de la API"""
    return {
        "message": "API de Formularios Colsubsidio",
        "version": "1.0.0",
        "endpoints": {
            "form1": "/api/v1/form1",
            "form2": "/api/v1/form2",
            "form3": "/api/v1/form3",
            "form4": "/api/v1/form4",
            "tasks": "/api/v1/tasks",
            "docs": "/docs"
        }
    }


@app.get("/health", tags=["General"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}


@app.post("/api/v1/form1", response_model=TaskResponse, tags=["Formularios"])
async def ejecutar_form1(request: FormularioRequest1, background_tasks: BackgroundTasks):
    """
    Ejecuta el formulario 1 en segundo plano
    """
    task_id = str(uuid.uuid4())
    created_at = datetime.now()

    # Crear entrada en storage
    tasks_storage[task_id] = {
        "task_id": task_id,
        "status": TaskStatus.PENDING,
        "form_type": FormType.FORM1,
        "created_at": created_at,
        "datos": request.dict(by_alias=True)
    }

    # Convertir request a diccionario para el form filler
    datos = {
        "institucion": request.institucion or request.proyecto,
        "proyecto": request.proyecto or request.institucion,
        "recomendacion": request.recomendacion,
        "recomendacion_text": request.recomendacion_text,
        "satisfaccion": request.satisfaccion,
        "satisfaccion_text": request.satisfaccion_text,
        "pagina_2": request.pagina_2.dict()
    }

    # Agregar tarea en segundo plano
    background_tasks.add_task(ejecutar_formulario, task_id, FormType.FORM1, datos)

    return TaskResponse(
        task_id=task_id,
        status=TaskStatus.PENDING,
        message="Tarea creada exitosamente. El formulario se está procesando.",
        created_at=created_at
    )


@app.post("/api/v1/form2", response_model=TaskResponse, tags=["Formularios"])
async def ejecutar_form2(request: FormularioRequest2, background_tasks: BackgroundTasks):
    """
    Ejecuta el formulario 2 en segundo plano
    """
    task_id = str(uuid.uuid4())
    created_at = datetime.now()

    tasks_storage[task_id] = {
        "task_id": task_id,
        "status": TaskStatus.PENDING,
        "form_type": FormType.FORM2,
        "created_at": created_at,
        "datos": request.dict()
    }

    datos = {
        "lugar": request.lugar,
        "nombre_proyecto": request.nombre_proyecto,
        "recomendacion": request.recomendacion,
        "recomendacion_text": request.recomendacion_text,
        "satisfaccion": request.satisfaccion,
        "satisfaccion_text": request.satisfaccion_text,
        "pagina_2": request.pagina_2.dict()
    }

    background_tasks.add_task(ejecutar_formulario, task_id, FormType.FORM2, datos)

    return TaskResponse(
        task_id=task_id,
        status=TaskStatus.PENDING,
        message="Tarea creada exitosamente. El formulario se está procesando.",
        created_at=created_at
    )


@app.post("/api/v1/form3", response_model=TaskResponse, tags=["Formularios"])
async def ejecutar_form3(request: FormularioRequest3, background_tasks: BackgroundTasks):
    """
    Ejecuta el formulario 3 en segundo plano
    """
    task_id = str(uuid.uuid4())
    created_at = datetime.now()

    tasks_storage[task_id] = {
        "task_id": task_id,
        "status": TaskStatus.PENDING,
        "form_type": FormType.FORM3,
        "created_at": created_at,
        "datos": request.dict()
    }

    datos = {
        "lugar": request.lugar,
        "nombre_proyecto": request.nombre_proyecto,
        "unidad": request.unidad,
        "recomendacion": request.recomendacion,
        "recomendacion_text": request.recomendacion_text,
        "satisfaccion": request.satisfaccion,
        "satisfaccion_text": request.satisfaccion_text,
        "pagina_2": request.pagina_2.dict()
    }

    background_tasks.add_task(ejecutar_formulario, task_id, FormType.FORM3, datos)

    return TaskResponse(
        task_id=task_id,
        status=TaskStatus.PENDING,
        message="Tarea creada exitosamente. El formulario se está procesando.",
        created_at=created_at
    )


@app.post("/api/v1/form4", response_model=TaskResponse, tags=["Formularios"])
async def ejecutar_form4(request: FormularioRequest4, background_tasks: BackgroundTasks):
    """
    Ejecuta el formulario 4 en segundo plano
    """
    task_id = str(uuid.uuid4())
    created_at = datetime.now()

    tasks_storage[task_id] = {
        "task_id": task_id,
        "status": TaskStatus.PENDING,
        "form_type": FormType.FORM4,
        "created_at": created_at,
        "datos": request.dict()
    }

    datos = {
        "lugar": request.lugar,
        "nombre_proyecto": request.nombre_proyecto,
        "recomendacion": request.recomendacion,
        "recomendacion_text": request.recomendacion_text,
        "satisfaccion": request.satisfaccion,
        "satisfaccion_text": request.satisfaccion_text,
        "pagina_2": request.pagina_2.dict()
    }

    background_tasks.add_task(ejecutar_formulario, task_id, FormType.FORM4, datos)

    return TaskResponse(
        task_id=task_id,
        status=TaskStatus.PENDING,
        message="Tarea creada exitosamente. El formulario se está procesando.",
        created_at=created_at
    )


@app.get("/api/v1/tasks/{task_id}", response_model=TaskDetailResponse, tags=["Tareas"])
async def obtener_tarea(task_id: str):
    """
    Obtiene el estado de una tarea específica
    """
    if task_id not in tasks_storage:
        raise HTTPException(status_code=404, detail=f"Tarea {task_id} no encontrada")

    task = tasks_storage[task_id]

    return TaskDetailResponse(
        task_id=task["task_id"],
        status=task["status"],
        form_type=task["form_type"],
        created_at=task["created_at"],
        completed_at=task.get("completed_at"),
        error=task.get("error"),
        result=task.get("result")
    )


@app.get("/api/v1/tasks", tags=["Tareas"])
async def listar_tareas(
    status: Optional[TaskStatus] = None,
    form_type: Optional[FormType] = None,
    limit: int = 100
):
    """
    Lista todas las tareas con filtros opcionales
    """
    tasks = list(tasks_storage.values())

    # Filtrar por status
    if status:
        tasks = [t for t in tasks if t["status"] == status]

    # Filtrar por form_type
    if form_type:
        tasks = [t for t in tasks if t["form_type"] == form_type]

    # Ordenar por fecha de creación (más reciente primero)
    tasks.sort(key=lambda x: x["created_at"], reverse=True)

    # Limitar resultados
    tasks = tasks[:limit]

    return {
        "total": len(tasks),
        "tasks": [
            {
                "task_id": t["task_id"],
                "status": t["status"],
                "form_type": t["form_type"],
                "created_at": t["created_at"],
                "completed_at": t.get("completed_at")
            }
            for t in tasks
        ]
    }


@app.delete("/api/v1/tasks/{task_id}", tags=["Tareas"])
async def eliminar_tarea(task_id: str):
    """
    Elimina una tarea del almacenamiento
    """
    if task_id not in tasks_storage:
        raise HTTPException(status_code=404, detail=f"Tarea {task_id} no encontrada")

    del tasks_storage[task_id]

    return {"message": f"Tarea {task_id} eliminada exitosamente"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
