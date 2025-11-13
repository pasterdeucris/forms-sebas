"""
Ejemplo específico para el formulario de Preescolar Integrales de Colsubsidio

Este script muestra cómo configurar los datos específicos para este formulario.
Primero ejecuta form_inspector.py para identificar los campos reales.
"""
from form_automation import QualtricsFormFiller
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def fill_colsubsidio_form():
    """
    Ejemplo de llenado del formulario de Preescolar Integrales

    IMPORTANTE: Primero ejecuta form_inspector.py para identificar
    los IDs reales de los campos del formulario.
    """

    # URL del formulario
    FORM_URL = "https://colsubsidio.az1.qualtrics.com/jfe/form/SV_dhz8RuGCTqJm1Ui"

    # Datos de ejemplo - DEBES REEMPLAZAR ESTOS VALORES
    datos_personales = {
        'nombre': 'Juan Pérez García',
        'email': 'juan.perez@ejemplo.com',
        'telefono': '3001234567',
        'ciudad': 'Bogotá'
    }

    # Inicializar el bot
    bot = QualtricsFormFiller(headless=False)

    try:
        # Navegar al formulario
        bot.navigate_to_form(FORM_URL)

        # ===== PÁGINA 1 =====
        logger.info("\n" + "="*60)
        logger.info("LLENANDO PÁGINA 1")
        logger.info("="*60)

        # IMPORTANTE: Estos son IDs de ejemplo
        # Usa form_inspector.py para obtener los IDs reales
        page_1_data = {
            'text_fields': {
                # Reemplaza estos IDs con los reales del formulario
                # 'QR~QID1': datos_personales['nombre'],
                # 'QR~QID2': datos_personales['email'],
                # 'QR~QID3': datos_personales['telefono'],
            },
            'radio_buttons': [
                # Ejemplo: Si hay una pregunta "¿Está interesado?"
                # 'Sí',  # Esto podría disparar un modal
            ],
            'dropdowns': {
                # 'ciudad_select': datos_personales['ciudad'],
            },
            'conditional_modals': [
                {
                    'trigger': 'SI',  # Si seleccionas "Sí" se abre un modal
                    'modal_data': {
                        'text_fields': {
                            # Campos que aparecen en el modal
                            # 'motivo_field': '¿Por qué está interesado?'
                        },
                        'radio_by_value': {
                            # Radio buttons en el modal
                            # 'frecuencia': '1'
                        }
                    }
                }
            ]
        }

        # Llenar página 1
        bot.fill_form_page(page_1_data)

        # Avanzar a página 2
        logger.info("\nAvanzando a la página 2...")
        bot.click_next_button()

        # ===== PÁGINA 2 =====
        logger.info("\n" + "="*60)
        logger.info("LLENANDO PÁGINA 2")
        logger.info("="*60)

        page_2_data = {
            'radio_buttons': [
                # Respuestas para preguntas de la segunda página
                # 'Opción A',
            ],
            'checkboxes': {
                # Si hay checkboxes de términos y condiciones
                # 'acepto_terminos': True,
            },
            'text_fields': {
                # Campos adicionales en página 2
                # 'comentarios': 'Comentarios adicionales aquí'
            },
            'conditional_modals': [
                {
                    'trigger': 'NO',  # Ejemplo: si respondes "No" a algo
                    'modal_data': {
                        'text_fields': {
                            # 'razon': 'Razón por la que respondí no'
                        }
                    }
                }
            ]
        }

        # Llenar página 2
        bot.fill_form_page(page_2_data)

        # Enviar formulario
        logger.info("\nEnviando formulario...")
        bot.click_next_button()

        logger.info("\n" + "="*60)
        logger.info("✅ FORMULARIO COMPLETADO EXITOSAMENTE")
        logger.info("="*60)

        # Esperar para ver el resultado
        import time
        time.sleep(5)

    except Exception as e:
        logger.error(f"❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Cerrar navegador
        bot.close()


def fill_multiple_forms():
    """
    Ejemplo de cómo llenar múltiples formularios con diferentes datos
    Útil si necesitas enviar varios formularios con información diferente
    """

    # Lista de datos de diferentes personas
    personas = [
        {
            'nombre': 'Ana García',
            'email': 'ana@ejemplo.com',
            'telefono': '3001111111',
            'ciudad': 'Bogotá'
        },
        {
            'nombre': 'Carlos López',
            'email': 'carlos@ejemplo.com',
            'telefono': '3002222222',
            'ciudad': 'Medellín'
        }
    ]

    for i, persona in enumerate(personas, 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"PROCESANDO FORMULARIO {i} de {len(personas)}")
        logger.info(f"Persona: {persona['nombre']}")
        logger.info(f"{'='*60}\n")

        # Crear nueva instancia para cada formulario
        bot = QualtricsFormFiller(headless=False)

        try:
            # Aquí iría la lógica de llenado usando los datos de 'persona'
            # Similar al ejemplo anterior pero usando persona['nombre'], etc.
            pass

        except Exception as e:
            logger.error(f"Error procesando formulario de {persona['nombre']}: {e}")

        finally:
            bot.close()

        # Esperar entre formularios para no saturar el servidor
        import time
        if i < len(personas):
            logger.info("Esperando antes del siguiente formulario...")
            time.sleep(10)


if __name__ == "__main__":
    import sys

    print("\n" + "="*60)
    print("AUTOMATIZACIÓN FORMULARIO PREESCOLAR INTEGRALES - COLSUBSIDIO")
    print("="*60)
    print("\n⚠️  IMPORTANTE: Antes de ejecutar este script:")
    print("1. Ejecuta 'python form_inspector.py' para identificar los campos")
    print("2. Actualiza los IDs en este archivo con los valores reales")
    print("3. Verifica que los datos en 'datos_personales' sean correctos")
    print("\n¿Deseas continuar? (s/n): ", end='')

    respuesta = input().strip().lower()

    if respuesta == 's':
        # Ejecutar el llenado único
        fill_colsubsidio_form()

        # Si quieres llenar múltiples formularios, descomenta la siguiente línea:
        # fill_multiple_forms()
    else:
        print("\nOperación cancelada. Ejecuta 'form_inspector.py' primero.")
        sys.exit(0)
