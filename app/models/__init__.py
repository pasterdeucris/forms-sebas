"""
Modelos Pydantic para las APIs de formularios
"""

from .form1_models import Form1Request, Pagina2Form1, FormResponse
from .form2_models import Form2Request, Pagina2Form2
from .form3_models import Form3Request, Pagina2Form3
from .form4_models import Form4Request, Pagina2Form4

__all__ = [
    "Form1Request",
    "Form2Request",
    "Form3Request",
    "Form4Request",
    "Pagina2Form1",
    "Pagina2Form2",
    "Pagina2Form3",
    "Pagina2Form4",
    "FormResponse",
]
