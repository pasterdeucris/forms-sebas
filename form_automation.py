"""
Script de automatización para formulario de Preescolar Integrales
usando Selenium WebDriver
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QualtricsFormFiller:
    """Clase para automatizar el llenado del formulario de Qualtrics"""

    def __init__(self, headless=False):
        """
        Inicializa el driver de Selenium

        Args:
            headless (bool): Si True, ejecuta en modo headless (sin interfaz gráfica)
        """
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def navigate_to_form(self, url):
        """Navega al formulario"""
        logger.info(f"Navegando a: {url}")
        self.driver.get(url)
        time.sleep(2)  # Esperar a que cargue completamente

    def wait_for_element(self, by, value, timeout=10):
        """Espera a que un elemento esté presente"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.warning(f"Timeout esperando elemento: {value}")
            return None

    def wait_for_clickable(self, by, value, timeout=10):
        """Espera a que un elemento sea clickeable"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            logger.warning(f"Timeout esperando elemento clickeable: {value}")
            return None

    def fill_text_field(self, field_id, value):
        """Llena un campo de texto"""
        try:
            field = self.wait_for_element(By.ID, field_id)
            if field:
                field.clear()
                field.send_keys(value)
                logger.info(f"Campo {field_id} llenado con: {value}")
                return True
        except Exception as e:
            logger.error(f"Error llenando campo {field_id}: {e}")
        return False

    def select_radio_by_label(self, label_text):
        """Selecciona un radio button por el texto de su label"""
        try:
            # Buscar el label que contiene el texto
            labels = self.driver.find_elements(By.TAG_NAME, "label")
            for label in labels:
                if label_text.lower() in label.text.lower():
                    # Hacer clic en el label
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", label)
                    time.sleep(0.3)
                    label.click()
                    logger.info(f"Radio button seleccionado: {label_text}")
                    time.sleep(0.5)  # Esperar a que se procese la selección
                    return True
        except Exception as e:
            logger.error(f"Error seleccionando radio button '{label_text}': {e}")
        return False

    def select_radio_by_value(self, name, value):
        """Selecciona un radio button por su name y value"""
        try:
            radio = self.wait_for_clickable(By.CSS_SELECTOR, f"input[name='{name}'][value='{value}']")
            if radio:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", radio)
                time.sleep(0.3)
                self.driver.execute_script("arguments[0].click();", radio)
                logger.info(f"Radio button seleccionado: {name}={value}")
                time.sleep(0.5)
                return True
        except Exception as e:
            logger.error(f"Error seleccionando radio button {name}={value}: {e}")
        return False

    def select_checkbox(self, checkbox_id, check=True):
        """Marca o desmarca un checkbox"""
        try:
            checkbox = self.wait_for_clickable(By.ID, checkbox_id)
            if checkbox:
                is_checked = checkbox.is_selected()
                if (check and not is_checked) or (not check and is_checked):
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                    time.sleep(0.3)
                    checkbox.click()
                    logger.info(f"Checkbox {checkbox_id} {'marcado' if check else 'desmarcado'}")
                    time.sleep(0.5)
                    return True
        except Exception as e:
            logger.error(f"Error con checkbox {checkbox_id}: {e}")
        return False

    def select_dropdown(self, select_id, option_text):
        """Selecciona una opción de un dropdown"""
        try:
            # Hacer clic en el dropdown para abrirlo
            dropdown = self.wait_for_clickable(By.ID, select_id)
            if dropdown:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
                time.sleep(0.3)
                dropdown.click()
                time.sleep(0.5)

                # Buscar y hacer clic en la opción
                options = self.driver.find_elements(By.TAG_NAME, "option")
                for option in options:
                    if option_text.lower() in option.text.lower():
                        option.click()
                        logger.info(f"Opción seleccionada en {select_id}: {option_text}")
                        time.sleep(0.5)
                        return True
        except Exception as e:
            logger.error(f"Error seleccionando dropdown {select_id}: {e}")
        return False

    def handle_conditional_modal(self, trigger_response, modal_data=None):
        """
        Maneja modales que aparecen condicionalmente

        Args:
            trigger_response: La respuesta que dispara el modal (ej: "SI", "NO")
            modal_data: Datos para llenar el modal si aparece
        """
        try:
            # Esperar un momento para que aparezca el modal
            time.sleep(1)

            # Intentar detectar si hay un modal abierto
            modals = self.driver.find_elements(By.CSS_SELECTOR, ".modal, .modal-content, [role='dialog']")

            if modals:
                logger.info("Modal detectado, procesando...")

                if modal_data:
                    # Llenar campos del modal según la configuración
                    for field_type, field_info in modal_data.items():
                        if field_type == 'text_fields':
                            for field_id, value in field_info.items():
                                self.fill_text_field(field_id, value)
                        elif field_type == 'radio_buttons':
                            for name, value in field_info.items():
                                self.select_radio_by_value(name, value)
                        elif field_type == 'checkboxes':
                            for checkbox_id, check in field_info.items():
                                self.select_checkbox(checkbox_id, check)

                # Buscar y hacer clic en el botón de cerrar/continuar del modal
                modal_buttons = self.driver.find_elements(By.CSS_SELECTOR,
                    ".modal button, [role='dialog'] button, .modal-footer button")

                for button in modal_buttons:
                    if any(text in button.text.lower() for text in ['continuar', 'aceptar', 'ok', 'siguiente']):
                        button.click()
                        logger.info("Modal cerrado exitosamente")
                        time.sleep(1)
                        break

                return True
            else:
                logger.info("No se detectó modal condicional")
                return False

        except Exception as e:
            logger.error(f"Error manejando modal condicional: {e}")
            return False

    def click_next_button(self):
        """Hace clic en el botón 'Siguiente' o similar para avanzar"""
        try:
            # Intentar diferentes selectores comunes para botones de siguiente
            next_button_selectors = [
                "button[type='submit']",
                "input[type='submit']",
                "button.NextButton",
                "input.NextButton",
                "#NextButton",
                "button:contains('Siguiente')",
                "input[value='Siguiente']",
                "button[title='Next']"
            ]

            for selector in next_button_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in buttons:
                        if button.is_displayed() and button.is_enabled():
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                            time.sleep(0.5)
                            button.click()
                            logger.info("Botón 'Siguiente' clickeado")
                            time.sleep(2)  # Esperar a que cargue la siguiente página
                            return True
                except:
                    continue

            # Si no encuentra el botón por CSS, buscar por texto
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            buttons.extend(self.driver.find_elements(By.TAG_NAME, "input"))

            for button in buttons:
                if any(text in button.text.lower() for text in ['siguiente', 'next', 'continuar']) or \
                   (button.get_attribute('value') and any(text in button.get_attribute('value').lower()
                    for text in ['siguiente', 'next', 'continuar'])):
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    time.sleep(0.5)
                    button.click()
                    logger.info("Botón 'Siguiente' clickeado")
                    time.sleep(2)
                    return True

        except Exception as e:
            logger.error(f"Error haciendo clic en botón siguiente: {e}")
        return False

    def fill_form_page(self, page_data):
        """
        Llena una página del formulario con los datos proporcionados

        Args:
            page_data (dict): Diccionario con la estructura:
                {
                    'text_fields': {field_id: value},
                    'radio_buttons': [label_text1, label_text2, ...],
                    'radio_by_value': {name: value},
                    'checkboxes': {checkbox_id: True/False},
                    'dropdowns': {select_id: option_text},
                    'conditional_modals': {
                        'trigger': 'SI',  # La respuesta que dispara el modal
                        'modal_data': {...}  # Datos para llenar el modal
                    }
                }
        """
        logger.info("Llenando página del formulario...")

        # Llenar campos de texto
        if 'text_fields' in page_data:
            for field_id, value in page_data['text_fields'].items():
                self.fill_text_field(field_id, value)
                time.sleep(0.3)

        # Seleccionar radio buttons por label
        if 'radio_buttons' in page_data:
            for label_text in page_data['radio_buttons']:
                self.select_radio_by_label(label_text)
                time.sleep(0.3)

                # Verificar si esta selección dispara un modal
                if 'conditional_modals' in page_data:
                    for modal_config in page_data['conditional_modals']:
                        if modal_config.get('trigger', '').lower() in label_text.lower():
                            self.handle_conditional_modal(
                                modal_config['trigger'],
                                modal_config.get('modal_data')
                            )

        # Seleccionar radio buttons por value
        if 'radio_by_value' in page_data:
            for name, value in page_data['radio_by_value'].items():
                self.select_radio_by_value(name, value)
                time.sleep(0.3)

        # Marcar checkboxes
        if 'checkboxes' in page_data:
            for checkbox_id, check in page_data['checkboxes'].items():
                self.select_checkbox(checkbox_id, check)
                time.sleep(0.3)

        # Seleccionar dropdowns
        if 'dropdowns' in page_data:
            for select_id, option_text in page_data['dropdowns'].items():
                self.select_dropdown(select_id, option_text)
                time.sleep(0.3)

        logger.info("Página llenada exitosamente")

    def close(self):
        """Cierra el navegador"""
        logger.info("Cerrando navegador...")
        self.driver.quit()


def main():
    """Función principal de ejemplo"""

    # URL del formulario
    FORM_URL = "https://colsubsidio.az1.qualtrics.com/jfe/form/SV_dhz8RuGCTqJm1Ui"

    # CONFIGURACIÓN DE DATOS DEL FORMULARIO
    # Ajusta estos datos según tus necesidades

    # Datos para la primera página
    page_1_data = {
        'text_fields': {
            # 'QR~QID1': 'Nombre completo',
            # 'QR~QID2': 'correo@ejemplo.com',
            # Agrega los IDs de campos de texto y sus valores
        },
        'radio_buttons': [
            # 'Opción 1',
            # 'Sí',  # Esta opción podría disparar un modal
            # Agrega las opciones de radio buttons que quieres seleccionar
        ],
        'conditional_modals': [
            {
                'trigger': 'SI',  # Si seleccionas una opción con "SI"
                'modal_data': {
                    'text_fields': {
                        # 'modal_field_id': 'valor del campo en el modal'
                    },
                    'radio_buttons': {
                        # 'modal_radio_name': 'valor'
                    }
                }
            }
        ]
    }

    # Datos para la segunda página
    page_2_data = {
        'text_fields': {
            # Campos de la segunda página
        },
        'radio_buttons': [
            # Opciones de la segunda página
        ],
    }

    # Inicializar el automatizador
    form_filler = QualtricsFormFiller(headless=False)

    try:
        # Navegar al formulario
        form_filler.navigate_to_form(FORM_URL)

        # Llenar primera página
        logger.info("=== PÁGINA 1 ===")
        form_filler.fill_form_page(page_1_data)

        # Hacer clic en siguiente
        form_filler.click_next_button()

        # Llenar segunda página
        logger.info("=== PÁGINA 2 ===")
        form_filler.fill_form_page(page_2_data)

        # Hacer clic en siguiente o enviar
        form_filler.click_next_button()

        logger.info("Formulario completado exitosamente!")

        # Esperar para ver el resultado
        time.sleep(5)

    except Exception as e:
        logger.error(f"Error durante la ejecución: {e}")

    finally:
        # Cerrar el navegador
        form_filler.close()


if __name__ == "__main__":
    main()
