"""
Script de inspección para identificar campos del formulario de Qualtrics
Este script te ayuda a descubrir los IDs y atributos de los campos
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json

FORM_URL = "https://colsubsidio.az1.qualtrics.com/jfe/form/SV_dhz8RuGCTqJm1Ui"


def inspect_form():
    """Inspecciona el formulario y lista todos los campos encontrados"""

    # Configurar Chrome
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        print(f"\n{'='*80}")
        print(f"INSPECCIÓN DEL FORMULARIO DE QUALTRICS")
        print(f"{'='*80}\n")

        # Navegar al formulario
        print(f"Navegando a: {FORM_URL}\n")
        driver.get(FORM_URL)
        time.sleep(3)

        page_num = 1

        while True:
            print(f"\n{'='*80}")
            print(f"PÁGINA {page_num}")
            print(f"{'='*80}\n")

            # Inspeccionar campos de texto
            print("\n--- CAMPOS DE TEXTO ---")
            text_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='email'], input[type='tel'], textarea")
            if text_inputs:
                for idx, input_field in enumerate(text_inputs, 1):
                    field_id = input_field.get_attribute('id')
                    field_name = input_field.get_attribute('name')
                    field_placeholder = input_field.get_attribute('placeholder')
                    field_class = input_field.get_attribute('class')

                    print(f"{idx}. Campo de texto:")
                    if field_id:
                        print(f"   ID: {field_id}")
                    if field_name:
                        print(f"   Name: {field_name}")
                    if field_placeholder:
                        print(f"   Placeholder: {field_placeholder}")
                    if field_class:
                        print(f"   Class: {field_class}")
                    print()
            else:
                print("No se encontraron campos de texto\n")

            # Inspeccionar radio buttons
            print("\n--- RADIO BUTTONS ---")
            radio_groups = {}
            radios = driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")

            if radios:
                for radio in radios:
                    name = radio.get_attribute('name')
                    value = radio.get_attribute('value')
                    radio_id = radio.get_attribute('id')

                    # Intentar encontrar el label asociado
                    label_text = ""
                    try:
                        if radio_id:
                            label = driver.find_element(By.CSS_SELECTOR, f"label[for='{radio_id}']")
                            label_text = label.text.strip()
                    except:
                        # Intentar encontrar el label padre
                        try:
                            parent = radio.find_element(By.XPATH, "..")
                            if parent.tag_name == 'label':
                                label_text = parent.text.strip()
                        except:
                            pass

                    if name not in radio_groups:
                        radio_groups[name] = []

                    radio_groups[name].append({
                        'id': radio_id,
                        'value': value,
                        'label': label_text
                    })

                for idx, (name, options) in enumerate(radio_groups.items(), 1):
                    print(f"{idx}. Grupo de radio buttons:")
                    print(f"   Name: {name}")
                    print(f"   Opciones:")
                    for opt in options:
                        print(f"      - Value: {opt['value']}")
                        if opt['label']:
                            print(f"        Label: {opt['label']}")
                        if opt['id']:
                            print(f"        ID: {opt['id']}")
                    print()
            else:
                print("No se encontraron radio buttons\n")

            # Inspeccionar checkboxes
            print("\n--- CHECKBOXES ---")
            checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
            if checkboxes:
                for idx, checkbox in enumerate(checkboxes, 1):
                    checkbox_id = checkbox.get_attribute('id')
                    checkbox_name = checkbox.get_attribute('name')
                    checkbox_value = checkbox.get_attribute('value')

                    # Intentar encontrar el label
                    label_text = ""
                    try:
                        if checkbox_id:
                            label = driver.find_element(By.CSS_SELECTOR, f"label[for='{checkbox_id}']")
                            label_text = label.text.strip()
                    except:
                        pass

                    print(f"{idx}. Checkbox:")
                    if checkbox_id:
                        print(f"   ID: {checkbox_id}")
                    if checkbox_name:
                        print(f"   Name: {checkbox_name}")
                    if checkbox_value:
                        print(f"   Value: {checkbox_value}")
                    if label_text:
                        print(f"   Label: {label_text}")
                    print()
            else:
                print("No se encontraron checkboxes\n")

            # Inspeccionar dropdowns/select
            print("\n--- DROPDOWNS/SELECT ---")
            selects = driver.find_elements(By.TAG_NAME, "select")
            if selects:
                for idx, select in enumerate(selects, 1):
                    select_id = select.get_attribute('id')
                    select_name = select.get_attribute('name')

                    options = select.find_elements(By.TAG_NAME, "option")
                    option_texts = [opt.text.strip() for opt in options if opt.text.strip()]

                    print(f"{idx}. Dropdown:")
                    if select_id:
                        print(f"   ID: {select_id}")
                    if select_name:
                        print(f"   Name: {select_name}")
                    if option_texts:
                        print(f"   Opciones: {', '.join(option_texts)}")
                    print()
            else:
                print("No se encontraron dropdowns\n")

            # Inspeccionar botones
            print("\n--- BOTONES ---")
            buttons = driver.find_elements(By.TAG_NAME, "button")
            buttons.extend(driver.find_elements(By.CSS_SELECTOR, "input[type='submit'], input[type='button']"))

            if buttons:
                for idx, button in enumerate(buttons, 1):
                    button_text = button.text.strip()
                    button_id = button.get_attribute('id')
                    button_class = button.get_attribute('class')
                    button_type = button.get_attribute('type')
                    button_value = button.get_attribute('value')

                    if button.is_displayed():
                        print(f"{idx}. Botón visible:")
                        if button_text:
                            print(f"   Texto: {button_text}")
                        if button_value:
                            print(f"   Value: {button_value}")
                        if button_id:
                            print(f"   ID: {button_id}")
                        if button_type:
                            print(f"   Type: {button_type}")
                        if button_class:
                            print(f"   Class: {button_class}")
                        print()

            # Preguntar si continuar a la siguiente página
            print(f"\n{'='*80}")
            print("¿Deseas inspeccionar la siguiente página?")
            print("Presiona ENTER para continuar o escribe 'q' para salir:")

            # Esperar input del usuario
            user_input = input().strip().lower()

            if user_input == 'q':
                print("\nFinalizando inspección...")
                break

            # Intentar hacer clic en el botón siguiente
            next_clicked = False
            for button in buttons:
                if button.is_displayed() and any(text in button.text.lower()
                   for text in ['siguiente', 'next', 'continuar']):
                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    time.sleep(0.5)
                    button.click()
                    print("\nNavegando a la siguiente página...\n")
                    time.sleep(3)
                    next_clicked = True
                    page_num += 1
                    break

            if not next_clicked:
                print("\nNo se encontró botón 'Siguiente'. Finalizando inspección...")
                break

    except Exception as e:
        print(f"\nError durante la inspección: {e}")

    finally:
        print("\n\nManteniendo el navegador abierto para inspección manual...")
        print("Presiona ENTER para cerrar el navegador...")
        input()
        driver.quit()


if __name__ == "__main__":
    inspect_form()
