"""
Script para llenar automáticamente el formulario de Preescolar Integrales de Colsubsidio
Bogotá y Cundinamarca usando Selenium
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time



SECCIONES_CONFIG = {
    'proceso_aprendizaje': {
        'QID': '27',
        'question_id': '1',
        'choice_ids': [3, 67, 68, 69,70],
        'nombre': 'Proceso de aprendizaje de los niños'
    },
    'habilidades_docentes': {
        'QID': '54',
        'question_id': '1',
        'choice_ids': [61, 71, 72, 73, 74, 75, 76],
        'nombre': 'Habilidades de los docentes'
    },
    'auxiliar_salud_nutricion': {
        'QID': '73',
        'question_id': '1',
        'choice_ids': [72, 73, 74, 75],
        'nombre': 'Auxiliar de apoyo en salud y nutrición'
    },
    'personal_administrativo': {
        'QID': '74',
        'question_id': '1',
        'choice_ids': [72, 73, 74, 75],
        'nombre': 'Personal administrativo'
    },
    'actividades_administrativas': {
        'QID': '75',
        'question_id': '1',
        'choice_ids': [61, 95, 96, 97],
        'nombre': 'Actividades administrativas'
    },
    'alimentacion': {
        'QID': '76',
        'question_id': '1',
        'choice_ids': [61, 99, 100,101],
        'nombre': 'Alimentación brindada en el jardín'
    },
    'desarrollo_propuesta': {
        'QID': '70',
        'question_id': '1',
        'choice_ids': [61, 105, 106, 107,108,109,110],
        'nombre': 'Desarrollo de la propuesta'
    },
    'profesionales_psicosocial': {
        'QID': '55',
        'question_id': '1',
        'choice_ids': [61, 76, 77, 78, 79],
        'nombre': 'Profesionales de apoyo psicosocial'
    },
    'nutricionista': {
        'QID': '59',
        'question_id': '1',
        'choice_ids': [72, 73, 74, 75, 76],
        'nombre': 'Habilidades del nutricionista'
    },
    'evaluacion_aspectos': {
        'QID': '63',
        'question_id': '1',
        'choice_ids': [61, 90, 91, 92, 93],
        'nombre': 'Evaluación de aspectos'
    },
    'coordinador_zona': {
    'QID': '80',
    'question_id': '1',
    'choice_ids': [72, 77, 74, 75],
    'nombre': 'Habilidades del coordinador de zona'
}
}
class ColsubsidioFormFiller:
    def __init__(self):
        """Inicializa el navegador"""
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Descomentar para modo sin ventana
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://colsubsidio.az1.qualtrics.com/jfe/form/SV_cZQUXOINZrCcUx8"
    
    def esperar_carga(self, segundos=1):
        """Espera un tiempo específico"""
        time.sleep(segundos)


    def hacer_clic_boton_siguiente(self):
        """
        Hace clic en el botón de siguiente/continuar de la página
        """
        print("Haciendo clic en botón siguiente...")
        
        xpath_boton = "/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[2]/input[2]"
        
        try:
            # Esperar a que el botón sea clickeable
            boton = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, xpath_boton))
            )
            
            # Scroll al botón para asegurarnos que esté visible
            self.driver.execute_script("arguments[0].scrollIntoView(true);", boton)
            self.esperar_carga(0.5)
            
            try:
                # Método 1: Click normal
                boton.click()
                print("✓ Clic en botón siguiente exitoso")
                
            except Exception as e1:
                print(f"Método 1 falló, intentando método 2...")
                try:
                    # Método 2: Click con JavaScript
                    self.driver.execute_script("arguments[0].click();", boton)
                    print("✓ Clic en botón siguiente exitoso (método 2)")
                    
                except Exception as e2:
                    print(f"Método 2 falló, intentando método 3...")
                    # Método 3: Click con Actions
                    from selenium.webdriver.common.action_chains import ActionChains
                    actions = ActionChains(self.driver)
                    actions.move_to_element(boton).click().perform()
                    print("✓ Clic en botón siguiente exitoso (método 3)")
            
            self.esperar_carga(1)
            
        except Exception as e:
            print(f"✗ Error al hacer clic en botón siguiente: {e}")
            raise


    def seleccionar_checkboxes_medios_pqrs(self, opciones):
        """
        Selecciona opciones de medios para manifestar PQRS (QID65)
        
        Args:
            opciones (list): Lista de textos de opciones a seleccionar
                            Opciones válidas:
                            - 'Call center'
                            - 'Correo electronico'
                            - 'Telefonicamente'
                            - 'Verbalmente'
                            - 'Pagina web'
                            - 'Codigo QR'
                            - 'Ninguna'
        """
        print("Seleccionando medios de PQRS...")
        
        # Mapeo de textos simplificados a choice IDs
        mapeo_opciones = {
            'call center': '1',
            'correo electronico': '4',
            'telefonicamente': '5',
            'verbalmente': '6',
            'pagina web': '7',
            'codigo qr': '8',
            'ninguna': '3'
        }
        
        try:
            for opcion in opciones:
                # Normalizar el texto de la opción
                opcion_normalizada = opcion.lower().strip()
                
                # Buscar coincidencia parcial en el mapeo
                choice_id = None
                for key, value in mapeo_opciones.items():
                    if key in opcion_normalizada or opcion_normalizada in key:
                        choice_id = value
                        break
                
                if choice_id is None:
                    print(f"⚠ Opción '{opcion}' no reconocida. Saltando...")
                    continue
                
                # Construir el ID del checkbox
                checkbox_id = f"QR~QID65~{choice_id}"
                label_for = f"QR~QID65~{choice_id}"
                
                print(f"  Seleccionando: {opcion} (ID: {choice_id})")
                
                try:
                    # Método 1: Hacer clic en el label
                    label = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, f"label[for='{label_for}']"))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", label)
                    self.esperar_carga(0.3)
                    self.driver.execute_script("arguments[0].click();", label)
                    print(f"  ✓ {opcion} seleccionado")
                    self.esperar_carga(0.3)
                    
                except Exception as e1:
                    print(f"  Método 1 falló, intentando método 2...")
                    try:
                        # Método 2: Hacer clic directamente en el input
                        checkbox = self.driver.find_element(By.ID, checkbox_id)
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                        self.esperar_carga(0.3)
                        self.driver.execute_script("""
                            arguments[0].checked = true;
                            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                            arguments[0].dispatchEvent(new Event('click', { bubbles: true }));
                        """, checkbox)
                        print(f"  ✓ {opcion} seleccionado (método 2)")
                        self.esperar_carga(0.3)
                        
                    except Exception as e2:
                        print(f"  ✗ Error seleccionando '{opcion}': {e2}")
            
            print("✓ Selección de medios PQRS completada\n")
            
        except Exception as e:
            print(f"✗ Error general en selección de PQRS: {e}")

    def seleccionar_escala_matriz(self, QID, question_id, choice_id, value):
        """
        Selecciona un valor en una matriz de preguntas tipo escala
        
        Args:
            QID (str): ID de la pregunta (ej: '27')
            question_id (str): ID de la sub-pregunta (ej: '1')
            choice_id (int): ID del choice/fila (ej: 3, 61, 62, etc.)
            value (int): Valor a seleccionar (1-10)
        """
        try:
            # Construir el ID del radio button
            radio_id = f"QR~QID{QID}#{question_id}~{choice_id}~{value}"
            print(f"Seleccionando: {radio_id}")
            
            # Esperar a que el input exista
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, radio_id))
            )
            
            # Método 1: Hacer clic en el label
            try:
                label = self.driver.find_element(By.CSS_SELECTOR, f"label[for='{radio_id}']")
                self.driver.execute_script("arguments[0].click();", label)
                print(f"✓ Clic en label exitoso")
                time.sleep(0.3)
                return
            except:
                print("Método 1 (label) falló, intentando método 2...")
            
            # Método 2: Marcar el input directamente
            try:
                input_element = self.driver.find_element(By.ID, radio_id)
                self.driver.execute_script("""
                    arguments[0].checked = true;
                    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                    arguments[0].dispatchEvent(new Event('click', { bubbles: true }));
                """, input_element)
                print(f"✓ Método 2 (input) exitoso")
                time.sleep(0.3)
                return
            except:
                print("Método 2 falló, intentando método 3...")
            
            # Método 3: Click normal en input
            input_element = self.driver.find_element(By.ID, radio_id)
            input_element.click()
            print(f"✓ Método 3 (click normal) exitoso")
            time.sleep(0.3)
            
        except Exception as e:
            print(f"✗ Error seleccionando QID{QID} choice {choice_id} valor {value}: {e}")

    def hacer_clic_boton_finalizar(self):
        """
        Hace clic en el botón de siguiente/continuar de la página
        """
        print("Haciendo clic en botón siguiente...")
        
        xpath_boton = "/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[2]/input[2]"
        
        try:
            # Esperar a que el botón sea clickeable
            boton = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, xpath_boton))
            )
            
            # Scroll al botón
            self.driver.execute_script("arguments[0].scrollIntoView(true);", boton)
            self.esperar_carga(0.5)
            
            try:
                # Método 1: Click normal
                boton.click()
                print("✓ Clic en botón siguiente exitoso")
                
            except Exception:
                print("Método 1 falló, intentando método 2...")
                try:
                    # Método 2: Click con JavaScript
                    self.driver.execute_script("arguments[0].click();", boton)
                    print("✓ Clic en botón siguiente exitoso (método 2)")
                    
                except Exception:
                    print("Método 2 falló, intentando método 3...")
                    # Método 3: Click con Actions
                    from selenium.webdriver.common.action_chains import ActionChains
                    actions = ActionChains(self.driver)
                    actions.move_to_element(boton).click().perform()
                    print("✓ Clic en botón siguiente exitoso (método 3)")
            
            self.esperar_carga(1)
            
        except Exception as e:
            print(f"✗ Error al hacer clic en botón siguiente: {e}")
            raise

    def llenar_seccion(self, seccion_nombre, valores=None):
        """
        Llena cualquier sección del formulario de manera genérica
        
        Args:
            seccion_nombre (str): Nombre de la sección ('atencion', 'talento_humano', etc.)
            valores (list): Lista de valores (1-10). Si es None, usa 10 para todas
        """
        if seccion_nombre not in SECCIONES_CONFIG:
            raise ValueError(f"Sección '{seccion_nombre}' no encontrada")
        
        config = SECCIONES_CONFIG[seccion_nombre]
        num_filas = len(config['choice_ids'])
        
        print(f"\n{'='*60}")
        print(f"Llenando sección: {config['nombre']}...")
        print(f"{'='*60}")
        
        if valores is None:
            valores = [10] * num_filas
        
        if len(valores) != num_filas:
            print(f"Advertencia: Se esperaban {num_filas} valores para '{seccion_nombre}', pero se recibieron {len(valores)}")
            # Ajustar valores si es necesario
            if len(valores) > num_filas:
                valores = valores[:num_filas]
            else:
                valores = valores + [10] * (num_filas - len(valores))
        
        QID = config['QID']
        question_id = config['question_id']
        choice_ids = config['choice_ids']
        
        for i, (choice_id, valor) in enumerate(zip(choice_ids, valores), 1):
            print(f"Fila {i}/{num_filas}: choice_id={choice_id}, valor={valor}")
            self.seleccionar_escala_matriz(QID, question_id, choice_id, valor)
        
        self.esperar_carga(0.5)
        print(f"✓ Sección '{config['nombre']}' completada\n")


    
    def llenar_pagina_1(self, institucion, proyecto,unidad, recomendacion=10, recon_text = "g", satisfaccion=10, sastisf_text = "gg"):
        """
        Llena la primera página del formulario
        
        Args:
            institucion (str): Nombre de la institución educativa
            proyecto (str): Denominación del proyecto
            recomendacion (int): Escala 0-10 para recomendación
            satisfaccion (int): Escala 1-10 para satisfacción
        """
        print("Llenando página 1...")
        
        # Llenar campo "Institución educativa"
        institucion_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#QR\~QID57"))
        )
        institucion_field.clear()
        institucion_field.send_keys(institucion)
        
        # Llenar campo "Denominación del proyecto"
        proyecto_field = self.driver.find_element(By.CSS_SELECTOR, "#QR\~QID43")
        proyecto_field.clear()
        proyecto_field.send_keys(proyecto)
       
        # Seleccionar nivel de recomendación (0-10)
        proyecto_field_2 = self.driver.find_element(By.CSS_SELECTOR, "#QR\~QID78")
        proyecto_field_2.clear()
        proyecto_field_2.send_keys(unidad)
       

        radio_id = f"/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[10]/div[3]/div/fieldset/div/table/tbody/tr[2]/td[{recomendacion+1}]/span/label"
        radio_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, radio_id))
        )
        radio_button.click()
        
        if recomendacion not in [9,10]:
            recomtxt = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#QR\~QID13"))
            )
            self.esperar_carga(0.7)
            recomtxt.clear()
            recomtxt.send_keys(recon_text)   

              # Seleccionar nivel de satisfacción (1-10)
        
        radio_id_2 = f"/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[14]/div[3]/div/fieldset/div/table/tbody/tr[2]/td[{satisfaccion+1}]/span/label"
        radio_button_2 = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, radio_id_2))
        )
        radio_button_2.click()
        
        if satisfaccion <=6:
            sastimtxt = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#QR\~QID53"))
            )
            self.esperar_carga(0.7)
            sastimtxt.clear()
            sastimtxt.send_keys(sastisf_text)
        
       
        self.esperar_carga()
        print("Página 1 completada")
        
    
    def hacer_click_siguiente(self):
        """Hace clic en el botón Siguiente"""
        siguiente_btn = self.driver.find_element(By.XPATH, "/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[2]/input")
        siguiente_btn.click()
        self.esperar_carga(2)
    
    
    
    def responder_pregunta_si_no(self, question_id, respuesta="Si"):
        """
        Responde a una pregunta de Sí/No
        
        Args:
            question_id (str): ID de la pregunta
            respuesta (str): "Si" o "No"
        """
        try:
            # Construir el selector para el label
            label_text = respuesta
            label_xpath = f"//fieldset[@id='{question_id}']//label[contains(., '{label_text}')]"
            label = self.driver.find_element(By.XPATH, label_xpath)
            label.click()
            self.esperar_carga(0.3)
        except Exception as e:
            print(f"Error respondiendo pregunta {question_id}: {e}")
    
    def seleccionar_checkboxes_pqrs(self, opciones):
        """
        Selecciona opciones de medios para manifestar PQRS
        
        Args:
            opciones (list): Lista de textos de opciones a seleccionar
        """
        print("Seleccionando medios de PQRS...")
        
        try:
            for opcion in opciones:
                checkbox_xpath = f"//fieldset[@id='QID15']//label[contains(., '{opcion}')]"
                checkbox = self.driver.find_element(By.XPATH, checkbox_xpath)
                checkbox.click()
                self.esperar_carga(0.2)
        except Exception as e:
            print(f"Error seleccionando checkboxes PQRS: {e}")
    

        
        self.esperar_carga(0.5)
    
    def llenar_sugerencias(self, texto):
        """
        Llena el campo de sugerencias
        
        Args:
            texto (str): Texto de sugerencias
        """
        try:
            sugerencias_field = self.driver.find_element(By.CSS_SELECTOR, "#QR\~QID51")
            sugerencias_field.clear()
            sugerencias_field.send_keys(texto)
        except Exception as e:
            print(f"Error llenando sugerencias: {e}")


    def llenar_pagina_2_seccion_coordinador_zona(self, valores=None):
        self.llenar_seccion('coordinador_zona', valores)

    def llenar_pagina_2_seccion_proceso_aprendizaje(self, valores=None):
        self.llenar_seccion('proceso_aprendizaje', valores)

    def llenar_pagina_2_seccion_habilidades_docentes(self, valores=None):
        self.llenar_seccion('habilidades_docentes', valores)

    def llenar_pagina_2_seccion_auxiliar_salud_nutricion(self, valores=None):
        self.llenar_seccion('auxiliar_salud_nutricion', valores)

    def llenar_pagina_2_seccion_personal_administrativo(self, valores=None):
        self.llenar_seccion('personal_administrativo', valores)

    def llenar_pagina_2_seccion_actividades_administrativas(self, valores=None):
        self.llenar_seccion('actividades_administrativas', valores)

    def llenar_pagina_2_seccion_alimentacion(self, valores=None):
        self.llenar_seccion('alimentacion', valores)

    def llenar_pagina_2_seccion_desarrollo_propuesta(self, valores=None):
        self.llenar_seccion('desarrollo_propuesta', valores)

    def llenar_pagina_2_seccion_profesionales_psicosocial(self, valores=None):
        self.llenar_seccion('profesionales_psicosocial', valores)

    def llenar_pagina_2_seccion_nutricionista(self, valores=None):
        self.llenar_seccion('nutricionista', valores)

    def llenar_pagina_2_seccion_evaluacion_aspectos(self, valores=None):
        self.llenar_seccion('evaluacion_aspectos', valores)

    def responder_pregunta_si_no_psicosocail(self, respuesta="Si"):
        """
        Responde a una pregunta de Sí/No
        
        Args:
            question_id (str): ID de la pregunta
            respuesta (str): "Si" o "No"
        """
        try:

            if respuesta.lower() == "si":
                label_xpath = '/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[6]/div[3]/div/fieldset/div/table/tbody/tr/td[1]/span/label'    # Construir el selector para el label
            else:
                label_xpath = '/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[6]/div[3]/div/fieldset/div/table/tbody/tr/td[2]/span/label'    # Construir el selector para el label
            label = self.driver.find_element(By.XPATH, label_xpath)
            label.click()
            
            self.esperar_carga(0.3)
        except Exception as e:
            print(f"Error respondiendo pregunta  {e}")

    def responder_pregunta_si_no_nutricionista(self, respuesta="Si"):
        """
        Responde a una pregunta de Sí/No
        
        Args:
            question_id (str): ID de la pregunta
            respuesta (str): "Si" o "No"
        """
        try:

            if respuesta.lower() == "si":
                label_xpath = '/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[10]/div[3]/div/fieldset/div/table/tbody/tr/td[1]/span/label'    # Construir el selector para el label
            else:
                label_xpath = '/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[10]/div[3]/div/fieldset/div/table/tbody/tr/td[2]/span/label'    # Construir el selector para el label
            label = self.driver.find_element(By.XPATH, label_xpath)
            label.click()
            
            self.esperar_carga(0.3)
        except Exception as e:
            print(f"Error respondiendo pregunta  {e}")

    def responder_pregunta_si_no_spe_desa(self, respuesta="no"):
        """
        Responde a una pregunta de Sí/No
        
        Args:
            question_id (str): ID de la pregunta
            respuesta (str): "Si" o "No"
        """
        try:

            if respuesta.lower() == "si":
                label_xpath = '/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[18]/div[3]/div/fieldset/div/table/tbody/tr/td[1]/span/label'    # Construir el selector para el label
            else:
                label_xpath = '/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[18]/div[3]/div/fieldset/div/table/tbody/tr/td[2]/span/label'    # Construir el selector para el label
            label = self.driver.find_element(By.XPATH, label_xpath)
            label.click()
            
            self.esperar_carga(0.3)
        except Exception as e:
            print(f"Error respondiendo pregunta  {e}")

    
    def responder_pregunta_si_no_recla(self, respuesta="no"):
        """
        Responde a una pregunta de Sí/No
        
        Args:
            question_id (str): ID de la pregunta
            respuesta (str): "Si" o "No"
        """
        try:

            if respuesta.lower() == "si":
                label_xpath = '/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[4]/div[3]/div/fieldset/div/table/tbody/tr/td[1]/span/label'    # Construir el selector para el label
            else:
                label_xpath = '/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[4]/div[3]/div/fieldset/div/table/tbody/tr/td[2]/span/label'    # Construir el selector para el label
            label = self.driver.find_element(By.XPATH, label_xpath)
            label.click()
            
            self.esperar_carga(0.3)
        except Exception as e:
            print(f"Error respondiendo pregunta  {e}")


    def llenar_pagina_2(self, datos_pagina_2):
        """
        Llena toda la página 2
        
        Args:
            datos_pagina_2 (dict): Diccionario con todos los datos de la página 2
        """
        print("\n" + "="*80)
        print("INICIANDO LLENADO DE PÁGINA 2")
        print("="*80 + "\n")
        
        # Sección de atención del programa
        self.llenar_pagina_2_seccion_proceso_aprendizaje(datos_pagina_2.get('proceso_aprendizaje'))


        self.llenar_pagina_2_seccion_habilidades_docentes(datos_pagina_2.get('habilidades_docentes'))

        self.responder_pregunta_si_no_psicosocail( datos_pagina_2.get('apoyo_piscosocial'))
        if datos_pagina_2.get('apoyo_piscosocial').lower() == 'si':
            self.esperar_carga(0.5)
            self.llenar_pagina_2_seccion_profesionales_psicosocial(datos_pagina_2.get('profesionales_psicosocial'))

        #TODO:CHECK
        self.responder_pregunta_si_no_nutricionista( datos_pagina_2.get('contacto_nutricionista'))

        self.esperar_carga(0.5)
        if datos_pagina_2.get('contacto_nutricionista').lower() == 'si':
            self.llenar_pagina_2_seccion_nutricionista(datos_pagina_2.get('nutricionista'))
            self.llenar_pagina_2_seccion_auxiliar_salud_nutricion(datos_pagina_2.get('auxiliar_salud_nutricion')) 
            self.llenar_pagina_2_seccion_personal_administrativo(datos_pagina_2.get('personal_administrativo'))
            self.llenar_pagina_2_seccion_coordinador_zona(datos_pagina_2.get('coordinador_zona'))

        else:
            self.llenar_pagina_2_seccion_auxiliar_salud_nutricion(datos_pagina_2.get('auxiliar_salud_nutricion'))
            self.llenar_pagina_2_seccion_personal_administrativo(datos_pagina_2.get('personal_administrativo'))


        self.responder_pregunta_si_no_spe_desa( datos_pagina_2.get('especialista_desarrollo'))
        if datos_pagina_2.get('especialista_desarrollo').lower() == 'si':
            self.esperar_carga(0.5)
            self.llenar_pagina_2_seccion_evaluacion_aspectos(datos_pagina_2.get('evaluacion_aspectos'))

        self.llenar_pagina_2_seccion_actividades_administrativas(datos_pagina_2.get('actividades_administrativas'))
        
        self.llenar_pagina_2_seccion_alimentacion(datos_pagina_2.get('alimentacion'))
        
    
        self.hacer_clic_boton_siguiente()


    def llenar_pagina_3(self, datos_pagina_2):
         # Medios para manifestar PQRS
        if 'pqrs_medios' in datos_pagina_2:
            self.seleccionar_checkboxes_medios_pqrs(datos_pagina_2['pqrs_medios'])
        
    
        self.responder_pregunta_si_no_recla( datos_pagina_2.get('ha_reclamado'))

        
        # Sección de desarrollo de la propuesta
        self.llenar_pagina_2_seccion_desarrollo_propuesta(datos_pagina_2.get('desarrollo_propuesta'))
        
        # Sugerencias
        if 'sugerencias' in datos_pagina_2:
            self.llenar_sugerencias(datos_pagina_2['sugerencias'])
        
        print("\n" + "="*80)
        print("PÁGINA 2 COMPLETADA")
        print("="*80 + "\n")

    def ejecutar(self, datos):
        """
        Ejecuta el llenado completo del formulario
        
        Args:
            datos (dict): Diccionario con todos los datos del formulario
        """
        try:
            print(f"Navegando a: {self.url}")
            self.driver.get(self.url)
            self.esperar_carga(3)
            
            # Llenar página 1
            self.llenar_pagina_1(
                institucion=datos['lugar'],
                proyecto=datos['nombre_proyecto'],
                unidad=datos.get('unidad'),
                recomendacion=datos.get('recomendacion', 10),
                recon_text=datos.get('recomendacion_text', ""),
                satisfaccion=datos.get('satisfaccion', 10),
                sastisf_text=datos.get('satisfaccion_text', "")
            )
            
            # Ir a página 2
            self.hacer_click_siguiente()
            
            # Llenar página 2
            self.llenar_pagina_2(datos['pagina_2'])

            self.llenar_pagina_3(datos['pagina_2'])       

            self.hacer_clic_boton_finalizar()     
            # Aquí puedes agregar más páginas si las hay
            # self.hacer_click_siguiente()
            # self.llenar_pagina_3(...)
            
            print("\n¡Formulario completado exitosamente!")
            print("NOTA: El formulario NO ha sido enviado. Revisa los datos antes de enviar.")
            
            # Mantener el navegador abierto para revisión
            input("\nPresiona Enter para cerrar el navegador...")
            
        except Exception as e:
            print(f"\nError durante la ejecución: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.driver.quit()


def main():
    """Función principal con datos de ejemplo"""
    
    # Datos de ejemplo para llenar el formulario
    datos_formulario = {
        'lugar': 'Colegio San José',
        'nombre_proyecto': 'Preescolar Integral 2025',
        "unidad": "Unidad Educativa Bogotá",
        'recomendacion': 4,
        'recomendacion_text': "hola esta recomendacion",  # Escala 0-10
        'satisfaccion': 5,
        'satisfaccion_text': "sasti text dd",  # Escala 1-10
        'pagina_2': {
            'proceso_aprendizaje': [10, 10, 10, 10],  # 4 valores
            'habilidades_docentes': [10, 10, 10, 10, 10, 10, 10],  # 7 valores
            'auxiliar_salud_nutricion': [10, 10, 10, 10],  # 4 valores
            'personal_administrativo': [10, 10, 10, 10],  # 4 valores
            'actividades_administrativas': [10, 10, 10, 10],  # 4 valores
            'alimentacion': [10, 10, 10],  # 3 valores
            'desarrollo_propuesta': [10, 10, 10, 10],  # 4 valores
            'profesionales_psicosocial': [10, 10, 10, 10, 10],  # 5 valores
            'nutricionista': [10, 10, 10, 10, 10],  # 5 valores
            'evaluacion_aspectos': [10, 10, 10, 10, 10],
             'coordinador_zona': [10, 10, 10, 10],  # 4 valores # 5 valores
            'apoyo_piscosocial': 'No',  # "Si" o "No"
            'contacto_nutricionista': 'Si',  # "Si" o "No",
            'especialista_desarrollo': 'Si',  # "Si" o "No"
            'pqrs_medios': [
                'Pagina web',
                'Correo electronico'
            ],
            'ha_reclamado': 'No',  # "Si" o "No"
            
            'sugerencias': 'Excelente programa. Continuamos comprometidos con la calidad educativa.'
        }
    }
    
    # Crear instancia y ejecutar
    form_filler = ColsubsidioFormFiller()
    form_filler.ejecutar(datos_formulario)


if __name__ == "__main__":
    main()