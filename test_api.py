"""
Script de prueba para validar que los modelos Pydantic funcionan correctamente
"""

import json
from app.models import Form1Request, Form2Request, Form3Request, Form4Request

def test_form1_model():
    """Prueba el modelo del formulario 1"""
    with open('examples/form1_example.json', 'r') as f:
        data = json.load(f)

    form1 = Form1Request(**data)
    print("✓ Modelo Form1 validado correctamente")
    print(f"  - Institución: {form1.institucion}")
    print(f"  - Proyecto: {form1.proyecto}")
    print(f"  - Recomendación: {form1.recomendacion}/10")
    return form1

def test_form2_model():
    """Prueba el modelo del formulario 2"""
    with open('examples/form2_example.json', 'r') as f:
        data = json.load(f)

    form2 = Form2Request(**data)
    print("✓ Modelo Form2 validado correctamente")
    print(f"  - Lugar: {form2.lugar}")
    print(f"  - Proyecto: {form2.nombre_proyecto}")
    print(f"  - Recomendación: {form2.recomendacion}/10")
    return form2

def test_form3_model():
    """Prueba el modelo del formulario 3"""
    with open('examples/form3_example.json', 'r') as f:
        data = json.load(f)

    form3 = Form3Request(**data)
    print("✓ Modelo Form3 validado correctamente")
    print(f"  - Lugar: {form3.lugar}")
    print(f"  - Proyecto: {form3.nombre_proyecto}")
    print(f"  - Unidad: {form3.unidad}")
    print(f"  - Recomendación: {form3.recomendacion}/10")
    return form3

def test_form4_model():
    """Prueba el modelo del formulario 4"""
    with open('examples/form4_example.json', 'r') as f:
        data = json.load(f)

    form4 = Form4Request(**data)
    print("✓ Modelo Form4 validado correctamente")
    print(f"  - Lugar: {form4.lugar}")
    print(f"  - Proyecto: {form4.nombre_proyecto}")
    print(f"  - Recomendación: {form4.recomendacion}/10")
    return form4

if __name__ == "__main__":
    print("\n" + "="*60)
    print("VALIDACIÓN DE MODELOS PYDANTIC")
    print("="*60 + "\n")

    try:
        test_form1_model()
        print()
        test_form2_model()
        print()
        test_form3_model()
        print()
        test_form4_model()

        print("\n" + "="*60)
        print("✓ TODOS LOS MODELOS VALIDADOS EXITOSAMENTE")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n✗ Error en la validación: {e}")
        import traceback
        traceback.print_exc()
