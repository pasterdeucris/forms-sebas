"""
Tests unitarios para el formulario de Preescolar Integrales de Colsubsidio - Form1
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from form1 import ColsubsidioFormFiller, SECCIONES_CONFIG


class TestColsubsidioFormFillerForm1:
    """Tests para la clase ColsubsidioFormFiller del formulario 1"""

    @pytest.fixture
    def form_filler(self):
        """Fixture que crea una instancia del form filler con driver mockeado"""
        with patch('form1.webdriver.Chrome'):
            filler = ColsubsidioFormFiller()
            filler.driver = Mock()
            filler.wait = Mock()
            return filler

    def test_inicializacion(self, form_filler):
        """Test que verifica la inicialización correcta del form filler"""
        assert form_filler.url == "https://colsubsidio.az1.qualtrics.com/jfe/form/SV_dhz8RuGCTqJm1Ui"
        assert form_filler.driver is not None
        assert form_filler.wait is not None

    def test_esperar_carga(self, form_filler):
        """Test que verifica que el método esperar_carga funciona"""
        with patch('form1.time.sleep') as mock_sleep:
            form_filler.esperar_carga(2)
            mock_sleep.assert_called_once_with(2)

    def test_secciones_config_estructura(self):
        """Test que verifica que SECCIONES_CONFIG tiene la estructura correcta"""
        secciones_esperadas = [
            'atencion',
            'talento_humano',
            'psicosocial',
            'dinamizadores',
            'desarrollo_propuesta',
            'aspectos_satisfaccion',
            'aspectos_dinamizador'
        ]

        for seccion in secciones_esperadas:
            assert seccion in SECCIONES_CONFIG
            assert 'QID' in SECCIONES_CONFIG[seccion]
            assert 'question_id' in SECCIONES_CONFIG[seccion]
            assert 'choice_ids' in SECCIONES_CONFIG[seccion]
            assert 'nombre' in SECCIONES_CONFIG[seccion]

    def test_llenar_pagina_1(self, form_filler):
        """Test que verifica el llenado de la página 1"""
        # Mock de elementos
        mock_institucion = Mock()
        mock_proyecto = Mock()
        mock_radio = Mock()

        form_filler.wait.until = Mock(return_value=mock_institucion)
        form_filler.driver.find_element = Mock(side_effect=[mock_proyecto, mock_radio, mock_radio])

        with patch('form1.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = mock_radio

            form_filler.llenar_pagina_1(
                institucion="Colegio Test",
                proyecto="Proyecto Test",
                recomendacion=10,
                satisfaccion=10
            )

            mock_institucion.clear.assert_called()
            mock_institucion.send_keys.assert_called_with("Colegio Test")
            mock_proyecto.clear.assert_called()
            mock_proyecto.send_keys.assert_called_with("Proyecto Test")

    def test_seleccionar_escala_matriz(self, form_filler):
        """Test que verifica la selección en matriz de escala"""
        mock_label = Mock()
        form_filler.driver.find_element = Mock(return_value=mock_label)
        form_filler.driver.execute_script = Mock()

        with patch('form1.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = mock_label

            form_filler.seleccionar_escala_matriz('27', '1', 3, 10)

            # Verificar que se intentó hacer clic en el label
            assert form_filler.driver.execute_script.called

    def test_llenar_seccion_con_valores_correctos(self, form_filler):
        """Test que verifica el llenado de una sección con valores correctos"""
        form_filler.seleccionar_escala_matriz = Mock()

        valores = [10, 9, 8, 7, 6, 5, 4]
        form_filler.llenar_seccion('atencion', valores)

        # Verificar que se llamó seleccionar_escala_matriz el número correcto de veces
        assert form_filler.seleccionar_escala_matriz.call_count == 7

    def test_llenar_seccion_sin_valores(self, form_filler):
        """Test que verifica el llenado de una sección sin valores (usa defaults)"""
        form_filler.seleccionar_escala_matriz = Mock()

        form_filler.llenar_seccion('atencion')

        # Verificar que se llamó con valores por defecto (10)
        assert form_filler.seleccionar_escala_matriz.call_count == 7

    def test_llenar_seccion_invalida(self, form_filler):
        """Test que verifica que se lanza excepción con sección inválida"""
        with pytest.raises(ValueError):
            form_filler.llenar_seccion('seccion_inexistente')

    def test_responder_pregunta_si_no_demo_si(self, form_filler):
        """Test que verifica responder Sí a pregunta demo"""
        mock_label = Mock()
        form_filler.driver.find_element = Mock(return_value=mock_label)

        form_filler.responder_pregunta_si_no_demo("Si")

        mock_label.click.assert_called_once()

    def test_responder_pregunta_si_no_demo_no(self, form_filler):
        """Test que verifica responder No a pregunta demo"""
        mock_label = Mock()
        form_filler.driver.find_element = Mock(return_value=mock_label)

        form_filler.responder_pregunta_si_no_demo("No")

        mock_label.click.assert_called_once()

    def test_seleccionar_checkboxes_pqrs(self, form_filler):
        """Test que verifica la selección de checkboxes PQRS"""
        mock_label = Mock()
        form_filler.wait.until = Mock(return_value=mock_label)
        form_filler.driver.execute_script = Mock()

        opciones = ['Pagina web', 'Correo electronico']
        form_filler.seleccionar_checkboxes_pqrs(opciones)

        # Verificar que se intentó seleccionar ambas opciones
        assert form_filler.driver.execute_script.call_count >= 2

    def test_hacer_click_siguiente(self, form_filler):
        """Test que verifica hacer clic en botón siguiente"""
        mock_button = Mock()
        form_filler.driver.find_element = Mock(return_value=mock_button)

        with patch('form1.time.sleep'):
            form_filler.hacer_click_siguiente()

            mock_button.click.assert_called_once()

    def test_llenar_pagina_2_completa(self, form_filler):
        """Test que verifica el llenado completo de la página 2"""
        # Mockear todos los métodos que se llaman
        form_filler.llenar_seccion = Mock()
        form_filler.responder_pregunta_si_no_demo = Mock()
        form_filler.responder_pregunta_si_no_coor = Mock()
        form_filler.responder_pregunta_si_no_recla = Mock()
        form_filler.seleccionar_checkboxes_pqrs = Mock()
        form_filler.llenar_sugerencias = Mock()

        datos_pagina_2 = {
            'atencion': [10, 10, 10, 10, 10, 10, 10],
            'talento_humano': [10, 10, 10, 10, 10, 10, 10, 10, 10],
            'psicosocial': [10, 10, 10, 10, 10, 10, 10],
            'dinamizadores': [10, 10, 10, 10, 10, 10, 10],
            'contacto_dinamizador': 'No',
            'contacto_coordinador': 'Si',
            'aspectos_satisfaccion': [10, 10, 10, 10, 10],
            'pqrs_medios': ['Pagina web'],
            'ha_reclamado': 'No',
            'desarrollo_propuesta': [10, 10, 10, 10, 10, 10, 10],
            'sugerencias': 'Test sugerencias'
        }

        form_filler.llenar_pagina_2(datos_pagina_2)

        # Verificar que se llamaron los métodos esperados
        assert form_filler.llenar_seccion.call_count >= 5
        form_filler.responder_pregunta_si_no_demo.assert_called_once()
        form_filler.seleccionar_checkboxes_pqrs.assert_called_once()

    def test_datos_formulario_estructura_valida(self):
        """Test que verifica que la estructura de datos del formulario es válida"""
        datos_formulario = {
            'institucion': 'Colegio Test',
            'proyecto': 'Proyecto Test',
            'recomendacion': 10,
            'recomendacion_text': "Test",
            'satisfaccion': 10,
            'satisfaccion_text': "Test",
            'pagina_2': {
                'atencion': [10, 10, 10, 10, 10, 10, 10],
                'talento_humano': [10, 10, 10, 10, 10, 10, 10, 10, 10],
                'psicosocial': [10, 10, 10, 10, 10, 10, 10],
                'dinamizadores': [10, 10, 10, 10, 10, 10, 10],
                'contacto_dinamizador': 'No',
                'contacto_coordinador': 'Si',
                'aspectos_satisfaccion': [10, 10, 10, 10, 10],
                'pqrs_medios': ['Pagina web'],
                'ha_reclamado': 'No',
                'desarrollo_propuesta': [10, 10, 10, 10, 10, 10, 10],
                'sugerencias': 'Test'
            }
        }

        # Verificar campos requeridos
        assert 'institucion' in datos_formulario
        assert 'proyecto' in datos_formulario
        assert 'pagina_2' in datos_formulario
        assert isinstance(datos_formulario['pagina_2'], dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
