"""
Modelos Pydantic para el Formulario 2 - Evaluación Preescolar Integrales v2
Basado en el diccionario de ejemplo de form2.py
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class Pagina2Form2(BaseModel):
    """Datos de la página 2 del formulario 2"""
    proceso_aprendizaje: List[int] = Field(..., description="4 valores de 1-10 para proceso de aprendizaje de los niños")
    habilidades_docentes: List[int] = Field(..., description="7 valores de 1-10 para habilidades de los docentes")
    auxiliar_salud_nutricion: List[int] = Field(..., description="4 valores de 1-10 para auxiliar de salud y nutrición")
    personal_administrativo: List[int] = Field(..., description="4 valores de 1-10 para personal administrativo")
    actividades_administrativas: List[int] = Field(..., description="4 valores de 1-10 para actividades administrativas")
    alimentacion: List[int] = Field(..., description="3 valores de 1-10 para alimentación brindada")
    desarrollo_propuesta: List[int] = Field(..., description="4 valores de 1-10 para desarrollo de la propuesta")
    profesionales_psicosocial: Optional[List[int]] = Field(None, description="5 valores de 1-10 para profesionales de apoyo psicosocial (condicional)")
    nutricionista: Optional[List[int]] = Field(None, description="5 valores de 1-10 para habilidades del nutricionista (condicional)")
    evaluacion_aspectos: Optional[List[int]] = Field(None, description="5 valores de 1-10 para evaluación de aspectos (condicional)")
    apoyo_piscosocial: str = Field(..., description="'Si' o 'No' para apoyo psicosocial")
    contacto_nutricionista: str = Field(..., description="'Si' o 'No' para contacto con nutricionista")
    especialista_desarrollo: str = Field(..., description="'Si' o 'No' para especialista en desarrollo")
    pqrs_medios: List[str] = Field(..., description="Medios para manifestar PQRS: ['Pagina web', 'Correo electronico', 'Telefonicamente', etc.]")
    ha_reclamado: str = Field(..., description="'Si' o 'No' para si ha hecho reclamo")
    sugerencias: str = Field(..., description="Texto de sugerencias")

    class Config:
        json_schema_extra = {
            "example": {
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
                "pqrs_medios": ["Pagina web", "Correo electronico"],
                "ha_reclamado": "No",
                "sugerencias": "Excelente programa. Continuamos comprometidos con la calidad educativa."
            }
        }


class Form2Request(BaseModel):
    """Modelo completo para el formulario 2"""
    lugar: str = Field(..., description="Nombre del lugar/institución educativa")
    nombre_proyecto: str = Field(..., description="Nombre del proyecto")
    recomendacion: int = Field(..., ge=0, le=10, description="Escala 0-10 para recomendación")
    recomendacion_text: Optional[str] = Field(None, description="Texto de justificación (requerido si recomendacion < 9)")
    satisfaccion: int = Field(..., ge=1, le=10, description="Escala 1-10 para satisfacción")
    satisfaccion_text: Optional[str] = Field(None, description="Texto adicional (requerido si satisfaccion <= 6)")
    pagina_2: Pagina2Form2 = Field(..., description="Datos de la página 2 del formulario")

    class Config:
        json_schema_extra = {
            "example": {
                "lugar": "Colegio San José",
                "nombre_proyecto": "Preescolar Integral 2025",
                "recomendacion": 4,
                "recomendacion_text": "hola esta recomendacion",
                "satisfaccion": 5,
                "satisfaccion_text": "sasti text dd",
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
                    "pqrs_medios": ["Pagina web", "Correo electronico"],
                    "ha_reclamado": "No",
                    "sugerencias": "Excelente programa. Continuamos comprometidos con la calidad educativa."
                }
            }
        }
