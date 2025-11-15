"""
Modelos Pydantic para el Formulario 1 - Evaluación Preescolar Integrales v1
Basado en el diccionario de ejemplo de form1.py
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class Pagina2Form1(BaseModel):
    """Datos de la página 2 del formulario 1"""
    atencion: List[int] = Field(..., description="7 valores de 1-10 para la sección de atención del programa")
    talento_humano: List[int] = Field(..., description="9 valores de 1-10 para habilidades del talento humano")
    psicosocial: List[int] = Field(..., description="7 valores de 1-10 para profesional psicosocial")
    dinamizadores: List[int] = Field(..., description="7 valores de 1-10 para dinamizadores pedagógicos")
    contacto_dinamizador: str = Field(..., description="'Si' o 'No' para contacto con dinamizador")
    aspectos_dinamizador: Optional[List[int]] = Field(None, description="7 valores de 1-10 para aspectos de dinamizador (condicional)")
    contacto_coordinador: str = Field(..., description="'Si' o 'No' para contacto con coordinador")
    aspectos_satisfaccion: Optional[List[int]] = Field(None, description="5 valores de 1-10 para aspectos de satisfacción (condicional)")
    pqrs_medios: List[str] = Field(..., description="Medios para manifestar PQRS: ['Pagina web', 'Correo electronico', 'Telefonicamente', 'Codigo QR', 'Call center', 'Verbalmente', 'Ninguna']")
    ha_reclamado: str = Field(..., description="'Si' o 'No' para si ha hecho reclamo")
    desarrollo_propuesta: List[int] = Field(..., description="7 valores de 1-10 para desarrollo de la propuesta")
    sugerencias: str = Field(..., description="Texto de sugerencias")

    class Config:
        json_schema_extra = {
            "example": {
                "atencion": [10, 10, 10, 10, 10, 10, 10],
                "talento_humano": [10, 10, 10, 10, 10, 10, 10, 10, 10],
                "psicosocial": [10, 10, 10, 10, 10, 10, 10],
                "dinamizadores": [10, 10, 10, 10, 10, 10, 10],
                "contacto_dinamizador": "Si",
                "aspectos_dinamizador": [10, 10, 10, 10, 10, 10, 10],
                "contacto_coordinador": "Si",
                "aspectos_satisfaccion": [10, 10, 10, 10, 10],
                "pqrs_medios": ["Pagina web", "Correo electronico", "Telefonicamente", "Codigo QR"],
                "ha_reclamado": "No",
                "desarrollo_propuesta": [10, 10, 10, 10, 10, 10, 10],
                "sugerencias": "Excelente programa. Continuamos comprometidos con la calidad educativa."
            }
        }


class Form1Request(BaseModel):
    """Modelo completo para el formulario 1"""
    institucion: str = Field(..., description="Nombre de la institución educativa")
    proyecto: str = Field(..., description="Denominación del proyecto")
    recomendacion: int = Field(..., ge=0, le=10, description="Escala 0-10 para recomendación")
    recomendacion_text: Optional[str] = Field(None, description="Texto de justificación (requerido si recomendacion < 9)")
    satisfaccion: int = Field(..., ge=1, le=10, description="Escala 1-10 para satisfacción")
    satisfaccion_text: Optional[str] = Field(None, description="Texto adicional (requerido si satisfaccion <= 6)")
    pagina_2: Pagina2Form1 = Field(..., description="Datos de la página 2 del formulario")

    class Config:
        json_schema_extra = {
            "example": {
                "institucion": "Colegio San José",
                "proyecto": "Preescolar Integral 2025",
                "recomendacion": 10,
                "recomendacion_text": "hola esta recomendacion",
                "satisfaccion": 10,
                "satisfaccion_text": "sasti text dd",
                "pagina_2": {
                    "atencion": [10, 10, 10, 10, 10, 10, 10],
                    "talento_humano": [10, 10, 10, 10, 10, 10, 10, 10, 10],
                    "psicosocial": [10, 10, 10, 10, 10, 10, 10],
                    "dinamizadores": [10, 10, 10, 10, 10, 10, 10],
                    "contacto_dinamizador": "Si",
                    "aspectos_dinamizador": [10, 10, 10, 10, 10, 10, 10],
                    "contacto_coordinador": "Si",
                    "aspectos_satisfaccion": [10, 10, 10, 10, 10],
                    "pqrs_medios": ["Pagina web", "Correo electronico", "Telefonicamente", "Codigo QR"],
                    "ha_reclamado": "No",
                    "desarrollo_propuesta": [10, 10, 10, 10, 10, 10, 10],
                    "sugerencias": "Excelente programa. Continuamos comprometidos con la calidad educativa."
                }
            }
        }


class FormResponse(BaseModel):
    """Respuesta estándar para todos los formularios"""
    success: bool
    message: str
    form_type: str
