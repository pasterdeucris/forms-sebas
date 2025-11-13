"""
Script ejecutable que usa el archivo de configuración JSON
para automatizar el formulario de Qualtrics
"""
import json
import sys
from form_automation import QualtricsFormFiller
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_file='form_config.json'):
    """Carga la configuración desde un archivo JSON"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info(f"Configuración cargada desde {config_file}")
        return config
    except FileNotFoundError:
        logger.error(f"No se encontró el archivo {config_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Error al parsear el JSON: {e}")
        sys.exit(1)


def run_automation(config_file='form_config.json', headless=False):
    """
    Ejecuta la automatización del formulario usando la configuración

    Args:
        config_file (str): Ruta al archivo de configuración JSON
        headless (bool): Si ejecutar en modo headless
    """
    # Cargar configuración
    config = load_config(config_file)

    # Obtener URL del formulario
    form_url = config.get('form_url')
    if not form_url:
        logger.error("No se encontró 'form_url' en la configuración")
        sys.exit(1)

    # Obtener páginas
    pages = config.get('pages', [])
    if not pages:
        logger.error("No se encontraron páginas en la configuración")
        sys.exit(1)

    # Inicializar el automatizador
    form_filler = QualtricsFormFiller(headless=headless)

    try:
        # Navegar al formulario
        form_filler.navigate_to_form(form_url)

        # Procesar cada página
        for page in pages:
            page_num = page.get('page_number', '?')
            page_name = page.get('name', f'Página {page_num}')

            logger.info(f"\n{'='*60}")
            logger.info(f"PROCESANDO: {page_name}")
            logger.info(f"{'='*60}\n")

            # Obtener campos de la página
            fields = page.get('fields', {})

            # Llenar la página
            form_filler.fill_form_page(fields)

            # Hacer clic en siguiente (excepto si es la última página)
            if page != pages[-1]:
                logger.info("Avanzando a la siguiente página...")
                if not form_filler.click_next_button():
                    logger.warning("No se pudo hacer clic en 'Siguiente'. ¿Es la última página?")

        logger.info("\n" + "="*60)
        logger.info("FORMULARIO COMPLETADO EXITOSAMENTE!")
        logger.info("="*60 + "\n")

        # Esperar para ver el resultado
        import time
        time.sleep(5)

    except Exception as e:
        logger.error(f"Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Cerrar el navegador
        form_filler.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Automatizar formulario de Qualtrics')
    parser.add_argument(
        '--config',
        default='form_config.json',
        help='Ruta al archivo de configuración JSON (default: form_config.json)'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Ejecutar en modo headless (sin interfaz gráfica)'
    )

    args = parser.parse_args()

    run_automation(config_file=args.config, headless=args.headless)
