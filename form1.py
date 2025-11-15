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
    'atencion': {
        'QID': '27',
        'question_id': '1',
        'choice_ids': [3, 61, 62, 63, 64, 65, 66],
        'nombre': 'Atención del programa'
    },
    'talento_humano': {
        'QID': '54',
        'question_id': '1',
        'choice_ids': [61, 63, 64, 65, 66, 67, 68, 69, 70],
        'nombre': 'Habilidades del talento humano'
    },
    'psicosocial': {
        'QID': '72',
        'question_id': '1',
        'choice_ids': [61, 66, 67, 68, 69, 70, 71],
        'nombre': 'Profesional psicosocial'
    },
    'dinamizadores': {
        'QID': '73',
        'question_id': '1',
        'choice_ids': [61, 71, 75, 76, 77, 78, 79],
        'nombre': 'Dinamizadores pedagógicos'
    },
    'desarrollo_propuesta': {
        'QID': '70',
        'question_id': '1',
        'choice_ids': [61, 99, 100, 101, 102, 103, 104],
        'nombre': 'Desarrollo de la propuesta'
    },
    'aspectos_satisfaccion': {  # NUEVA SECCIÓN
        'QID': '63',
        'question_id': '1',
        'choice_ids': [93, 90, 92, 61, 91],  # 5 filas
        'nombre': 'Aspectos de satisfacción'
    },
    'aspectos_dinamizador': {  # Segunda sección condicional - NUEVA
        'QID': '62',
        'question_id': '1',
        'choice_ids': [86, 87, 88, 61, 83, 84, 85],  # 7 filas
        'nombre': 'Aspectos de dinamizador'
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
        self.url = "https://colsubsidio.az1.qualtrics.com/jfe/form/SV_dhz8RuGCTqJm1Ui"
    
    def esperar_carga(self, segundos=1):
        """Espera un tiempo específico"""
        time.sleep(segundos)

    def hacer_clic_boton_siguiente_final(self):
        """
        Hace clic en el botón de siguiente/continuar
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
                print("Método 1 falló, intentando con JavaScript...")
                # Método 2: Click con JavaScript
                self.driver.execute_script("arguments[0].click();", boton)
                print("✓ Clic en botón siguiente exitoso (JavaScript)")
            
            self.esperar_carga(1)
            
        except Exception as e:
            print(f"✗ Error al hacer clic en botón siguiente: {e}")
            raise
    def llenar_pagina_1(self, institucion, proyecto, recomendacion=10, recon_text = "g", satisfaccion=10, sastisf_text = "gg"):
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
        

        radio_id = f"/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[8]/div[3]/div/fieldset/div/table/tbody/tr[2]/td[{recomendacion}]/span/label"
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
        
        radio_id_2 = f"/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[12]/div[3]/div/fieldset/div/table/tbody/tr[2]/td[{satisfaccion +1}]/span/label"
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

    def llenar_pagina_2_seccion_aspectos_satisfaccion(self, valores=None):
        

        self.llenar_seccion('aspectos_satisfaccion', valores)

    def llenar_pagina_2_seccion_atencion(self, valores=None):
        """
        Llena la sección de atención del programa (QID27)
        7 filas con escala 1-10
        
        Args:
            valores (list): Lista de 7 valores (1-10). Si es None, usa 10 para todas
        """
        self.llenar_seccion('atencion', valores)
    
    def llenar_pagina_2_seccion_talento_humano(self, valores=None):
        """
        Llena la sección de habilidades del talento humano (QID54)
        9 filas con escala 1-10
        """
        self.llenar_seccion('talento_humano', valores)
    
    def llenar_pagina_2_seccion_psicosocial(self, valores=None):
        """
        Llena la sección del profesional psicosocial (QID72)
        7 filas con escala 1-10
        """
        self.llenar_seccion('psicosocial', valores)
    
    def llenar_pagina_2_seccion_dinamizadores(self, valores=None):
        """
        Llena la sección de dinamizadores pedagógicos (QID73)
        7 filas con escala 1-10
        """
        self.llenar_seccion('dinamizadores', valores)
    
    def llenar_pagina_2_seccion_desarrollo_propuesta(self, valores=None):
        """
        Llena la sección de desarrollo de la propuesta (QID70)
        7 filas con escala 1-10
        """
        self.llenar_seccion('desarrollo_propuesta', valores)

    def llenar_pagina_2_seccion_desarrollo_aspectos_dinamizador(self, valores=None):
        """
        Llena la sección de desarrollo de la propuesta (QID70)
        7 filas con escala 1-10
        """
        self.llenar_seccion('aspectos_dinamizador', valores)
    
    def responder_pregunta_si_no_demo(self, respuesta="Si"):
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

    def responder_pregunta_si_no_coor(self, respuesta="Si"):
        """
        Responde a una pregunta de Sí/No
        
        Args:
            question_id (str): ID de la pregunta
            respuesta (str): "Si" o "No"
        """
        try:

            if respuesta.lower() == "si":
                label_xpath = '/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[14]/div[3]/div/fieldset/div/table/tbody/tr/td[1]/span/label'    # Construir el selector para el label
            else:
                label_xpath = '/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[14]/div[3]/div/fieldset/div/table/tbody/tr/td[2]/span/label'    # Construir el selector para el label
            label = self.driver.find_element(By.XPATH, label_xpath)
            label.click()
            
            self.esperar_carga(0.3)
        except Exception as e:
            print(f"Error respondiendo pregunta  {e}")

    
    def responder_pregunta_si_no_recla(self, respuesta="Si"):
        """
        Responde a una pregunta de Sí/No
        
        Args:
            question_id (str): ID de la pregunta
            respuesta (str): "Si" o "No"
        """
        try:

            if respuesta.lower() == "si":
                label_xpath = '/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[20]/div[3]/div/fieldset/div/table/tbody/tr/td[1]/span/label'    # Construir el selector para el label
            else:
                label_xpath = '/html/body/div[3]/div/form/div/div[2]/div[1]/div[3]/div[1]/div[20]/div[3]/div/fieldset/div/table/tbody/tr/td[2]/span/label'    # Construir el selector para el label
            label = self.driver.find_element(By.XPATH, label_xpath)
            label.click()
            
            self.esperar_carga(0.3)
        except Exception as e:
            print(f"Error respondiendo pregunta  {e}")
    
    def seleccionar_checkboxes_pqrs(self, opciones):
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
        self.llenar_pagina_2_seccion_atencion(datos_pagina_2.get('atencion'))
        
        # Sección de talento humano
        self.llenar_pagina_2_seccion_talento_humano(datos_pagina_2.get('talento_humano'))
        
        # Sección psicosocial
        self.llenar_pagina_2_seccion_psicosocial(datos_pagina_2.get('psicosocial'))
        
        # Sección dinamizadores
        self.llenar_pagina_2_seccion_dinamizadores(datos_pagina_2.get('dinamizadores'))
        
        # Pregunta sobre contacto con dinamizador de inclusión
        self.responder_pregunta_si_no_demo( datos_pagina_2.get('contacto_dinamizador', 'No'))

        if datos_pagina_2.get('contacto_dinamizador').lower() == 'si':
            self.esperar_carga(0.5)
            self.llenar_pagina_2_seccion_desarrollo_aspectos_dinamizador(datos_pagina_2.get('aspectos_dinamizador'))
        # Pregunta sobre contacto con coordinador de zona
        self.responder_pregunta_si_no_coor(datos_pagina_2.get('contacto_coordinador', 'Si'))

        if datos_pagina_2.get('contacto_coordinador').lower() == 'si':
                self.esperar_carga(0.5)
                self.llenar_pagina_2_seccion_aspectos_satisfaccion(datos_pagina_2.get('aspectos_satisfaccion'))

        
        # Medios para manifestar PQRS
        if 'pqrs_medios' in datos_pagina_2:
            self.seleccionar_checkboxes_pqrs(datos_pagina_2['pqrs_medios'])
        
        # Pregunta sobre solicitud, queja o reclamo
        self.responder_pregunta_si_no_recla( datos_pagina_2.get('ha_reclamado', 'No'))
        if datos_pagina_2.get('ha_reclamado').lower() == 'si':
            pass
        
        # Sección de desarrollo de la propuesta
        self.llenar_pagina_2_seccion_desarrollo_propuesta(datos_pagina_2.get('desarrollo_propuesta'))
        
        # Sugerencias
        
        self.llenar_sugerencias(datos_pagina_2['sugerencias'])

        # #QR\~QID51    
        
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
                institucion=datos['institucion'],
                proyecto=datos['proyecto'],
                recomendacion=datos.get('recomendacion', 10),
                recon_text=datos.get('recomendacion_text', ""),
                satisfaccion=datos.get('satisfaccion', 10),
                sastisf_text=datos.get('satisfaccion_text', "")
            )
            
            # Ir a página 2
            self.hacer_click_siguiente()
            
            # Llenar página 2
            self.llenar_pagina_2(datos['pagina_2'])
            
            self.hacer_clic_boton_siguiente_final()
            self.driver.quit()
            # Aquí puedes agregar más páginas si las hay
            # self.hacer_click_siguiente()
            # self.llenar_pagina_3(...)
            
            
            
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
        'institucion': 'Colegio San José',
        'proyecto': 'Preescolar Integral 2025',
        'recomendacion': 10,
        'recomendacion_text': "hola esta recomendacion",  # Escala 0-10
        'satisfaccion': 10,
        'satisfaccion_text': "sasti text dd",  # Escala 1-10
        'pagina_2': {
            'atencion': [10, 10, 10, 10, 10, 10, 10],  # 7 valores
            'talento_humano': [10, 10, 10, 10, 10, 10, 10, 10, 10],  # 9 valores
            'psicosocial': [10, 10, 10, 10, 10, 10, 10],  # 7 valores
            'dinamizadores': [10, 10, 10, 10, 10, 10, 10],  # 7 valores
            'contacto_dinamizador': 'si',  # "Si" o "No",
            'aspectos_dinamizador': [10, 10, 10, 10, 10, 10, 10],
            'contacto_coordinador': 'Si',
            'aspectos_satisfaccion': [10, 10, 10, 10, 10], # "Si" o "No"
            'pqrs_medios': [
                'Pagina web',           # Se mapeará a choice_id='7'
                'Correo electronico',   # Se mapeará a choice_id='4'
                'Telefonicamente',      # Se mapeará a choice_id='5'
                'Codigo QR' 
            ],
            'ha_reclamado': 'No',  # "Si" o "No"
            'desarrollo_propuesta': [10, 10, 10, 10, 10, 10, 10],  # 7 valores
            'sugerencias': 'Excelente programa. Continuamos comprometidos con la calidad educativa.'
        }
    }
    
    # Crear instancia y ejecutar
    form_filler = ColsubsidioFormFiller()
    form_filler.ejecutar(datos_formulario)


if __name__ == "__main__":
    main()