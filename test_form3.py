"""
Tests unitarios para el formulario de Preescolar Integrales de Colsubsidio - Form3
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from form3 import ColsubsidioFormFiller, SECCIONES_CONFIG


class TestColsubsidioFormFillerForm3:
    """Tests para la clase ColsubsidioFormFiller del formulario 3"""

    @pytest.fixture
    def form_filler(self):
        """Fixture que crea una instancia del form filler con driver mockeado"""
        with patch('form3.webdriver.Chrome'):
            filler = ColsubsidioFormFiller()
            filler.driver = Mock()
            filler.wait = Mock()
            return filler

    def test_inicializacion(self, form_filler):
        """Test que verifica la inicialización correcta del form filler"""
        assert form_filler.url == "https://colsubsidio.az1.qualtrics.com/jfe/form/SV_cZQUXOINZrCcUx8"
        assert form_filler.driver is not None
        assert form_filler.wait is not None

    def test_esperar_carga(self, form_filler):
        """Test que verifica que el método esperar_carga funciona"""
        with patch('form3.time.sleep') as mock_sleep:
            form_filler.esperar_carga(2)
            mock_sleep.assert_called_once_with(2)

    def test_secciones_config_estructura(self):
        """Test que verifica que SECCIONES_CONFIG tiene la estructura correcta"""
        secciones_esperadas = [
            'proceso_aprendizaje',
            'habilidades_docentes',
            'auxiliar_salud_nutricion',
            'personal_administrativo',
            'actividades_administrativas',
            'alimentacion',
            'desarrollo_propuesta',
            'profesionales_psicosocial',
            'nutricionista',
            'evaluacion_aspectos',
            'coordinador_zona'
        ]

        for seccion in secciones_esperadas:
            assert seccion in SECCIONES_CONFIG
            assert 'QID' in SECCIONES_CONFIG[seccion]
            assert 'question_id' in SECCIONES_CONFIG[seccion]
            assert 'choice_ids' in SECCIONES_CONFIG[seccion]
            assert 'nombre' in SECCIONES_CONFIG[seccion]

    def test_llenar_pagina_1_con_unidad(self, form_filler):
        """Test que verifica el llenado de la página 1 con campo unidad"""
        mock_institucion = Mock()
        mock_proyecto = Mock()
        mock_unidad = Mock()
        mock_radio = Mock()

        form_filler.wait.until = Mock(return_value=mock_institucion)
        form_filler.driver.find_element = Mock(side_effect=[
            mock_proyecto, mock_unidad, mock_radio, mock_radio
        ])

        with patch('form3.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = mock_radio

            form_filler.llenar_pagina_1(
                institucion="Colegio Test",
                proyecto="Proyecto Test",
                unidad="Unidad Test",
                recomendacion=10,
                satisfaccion=10
            )

            mock_institucion.clear.assert_called()
            mock_institucion.send_keys.assert_called_with("Colegio Test")

    def test_seleccionar_escala_matriz(self, form_filler):
        """Test que verifica la selección en matriz de escala"""
        mock_label = Mock()
        form_filler.driver.find_element = Mock(return_value=mock_label)
        form_filler.driver.execute_script = Mock()

        with patch('form3.WebDriverWait') as mock_wait:
            mock_wait.return_value.until.return_value = mock_label

            form_filler.seleccionar_escala_matriz('27', '1', 3, 10)

            assert form_filler.driver.execute_script.called

    def test_llenar_seccion_coordinador_zona(self, form_filler):
        """Test que verifica el llenado de la sección coordinador_zona"""
        form_filler.seleccionar_escala_matriz = Mock()

        valores = [10, 9, 8, 7]
        form_filler.llenar_seccion('coordinador_zona', valores)

        # 'coordinador_zona' tiene 4 choice_ids
        assert form_filler.seleccionar_escala_matriz.call_count == 4

    def test_llenar_seccion_sin_valores(self, form_filler):
        """Test que verifica el llenado de una sección sin valores (usa defaults)"""
        form_filler.seleccionar_escala_matriz = Mock()

        form_filler.llenar_seccion('habilidades_docentes')

        # 'habilidades_docentes' tiene 7 choice_ids
        assert form_filler.seleccionar_escala_matriz.call_count == 7

    def test_llenar_seccion_invalida(self, form_filler):
        """Test que verifica que se lanza excepción con sección inválida"""
        with pytest.raises(ValueError):
            form_filler.llenar_seccion('seccion_inexistente')

    def test_responder_pregunta_si_no_psicosocial_si(self, form_filler):
        """Test que verifica responder Sí a pregunta psicosocial"""
        mock_label = Mock()
        form_filler.driver.find_element = Mock(return_value=mock_label)

        form_filler.responder_pregunta_si_no_psicosocail("Si")

        mock_label.click.assert_called_once()

    def test_responder_pregunta_si_no_nutricionista_no(self, form_filler):
        """Test que verifica responder No a pregunta nutricionista"""
        mock_label = Mock()
        form_filler.driver.find_element = Mock(return_value=mock_label)

        form_filler.responder_pregunta_si_no_nutricionista("No")

        mock_label.click.assert_called_once()

    def test_seleccionar_checkboxes_pqrs(self, form_filler):
        """Test que verifica la selección de checkboxes PQRS"""
        mock_label = Mock()
        form_filler.wait.until = Mock(return_value=mock_label)
        form_filler.driver.execute_script = Mock()

        opciones = ['Pagina web', 'Correo electronico']
        form_filler.seleccionar_checkboxes_medios_pqrs(opciones)

        assert form_filler.driver.execute_script.call_count >= 2

    def test_hacer_clic_boton_finalizar(self, form_filler):
        """Test que verifica hacer clic en botón finalizar"""
        mock_button = Mock()
        form_filler.wait.until = Mock(return_value=mock_button)
        form_filler.driver.execute_script = Mock()

        form_filler.hacer_clic_boton_finalizar()

        # Verificar que se intentó hacer clic
        assert form_filler.driver.execute_script.called or mock_button.click.called

    def test_llenar_pagina_2_completa(self, form_filler):
        """Test que verifica el llenado completo de la página 2"""
        form_filler.llenar_seccion = Mock()
        form_filler.responder_pregunta_si_no_psicosocail = Mock()
        form_filler.responder_pregunta_si_no_nutricionista = Mock()
        form_filler.responder_pregunta_si_no_spe_desa = Mock()
        form_filler.responder_pregunta_si_no_recla = Mock()
        form_filler.seleccionar_checkboxes_medios_pqrs = Mock()
        form_filler.hacer_clic_boton_siguiente = Mock()

        datos_pagina_2 = {
            'proceso_aprendizaje': [10, 10, 10, 10, 10],
            'habilidades_docentes': [10, 10, 10, 10, 10, 10, 10],
            'auxiliar_salud_nutricion': [10, 10, 10, 10],
            'personal_administrativo': [10, 10, 10, 10],
            'coordinador_zona': [10, 10, 10, 10],
            'actividades_administrativas': [10, 10, 10, 10],
            'alimentacion': [10, 10, 10],
            'desarrollo_propuesta': [10, 10, 10, 10, 10, 10, 10],
            'profesionales_psicosocial': [10, 10, 10, 10, 10],
            'nutricionista': [10, 10, 10, 10, 10],
            'evaluacion_aspectos': [10, 10, 10, 10, 10],
            'apoyo_piscosocial': 'No',
            'contacto_nutricionista': 'Si',
            'especialista_desarrollo': 'Si',
            'pqrs_medios': ['Pagina web'],
            'ha_reclamado': 'No'
        }

        form_filler.llenar_pagina_2(datos_pagina_2)

        # Verificar que se llamaron los métodos esperados
        assert form_filler.llenar_seccion.call_count >= 5
        form_filler.responder_pregunta_si_no_psicosocail.assert_called_once()

    def test_llenar_pagina_3_completa(self, form_filler):
        """Test que verifica el llenado completo de la página 3"""
        form_filler.seleccionar_checkboxes_medios_pqrs = Mock()
        form_filler.responder_pregunta_si_no_recla = Mock()
        form_filler.llenar_seccion = Mock()
        form_filler.llenar_sugerencias = Mock()

        datos_pagina_2 = {
            'pqrs_medios': ['Pagina web'],
            'ha_reclamado': 'No',
            'desarrollo_propuesta': [10, 10, 10, 10, 10, 10, 10],
            'sugerencias': 'Test sugerencias'
        }

        form_filler.llenar_pagina_3(datos_pagina_2)

        form_filler.seleccionar_checkboxes_medios_pqrs.assert_called_once()
        form_filler.responder_pregunta_si_no_recla.assert_called_once()

    def test_datos_formulario_estructura_valida(self):
        """Test que verifica que la estructura de datos del formulario es válida"""
        datos_formulario = {
            'lugar': 'Colegio Test',
            'nombre_proyecto': 'Proyecto Test',
            'unidad': 'Unidad Test',
            'recomendacion': 10,
            'recomendacion_text': "Test",
            'satisfaccion': 10,
            'satisfaccion_text': "Test",
            'pagina_2': {
                'proceso_aprendizaje': [10, 10, 10, 10, 10],
                'habilidades_docentes': [10, 10, 10, 10, 10, 10, 10],
                'coordinador_zona': [10, 10, 10, 10],
                'apoyo_piscosocial': 'No',
                'contacto_nutricionista': 'Si',
                'especialista_desarrollo': 'Si',
                'pqrs_medios': ['Pagina web'],
                'ha_reclamado': 'No',
                'sugerencias': 'Test'
            }
        }

        # Verificar campos requeridos
        assert 'lugar' in datos_formulario
        assert 'nombre_proyecto' in datos_formulario
        assert 'unidad' in datos_formulario
        assert 'pagina_2' in datos_formulario
        assert isinstance(datos_formulario['pagina_2'], dict)

    def test_ejecutar_flujo_completo_mock(self, form_filler):
        """Test que verifica el flujo completo de ejecución con mocks"""
        form_filler.llenar_pagina_1 = Mock()
        form_filler.hacer_click_siguiente = Mock()
        form_filler.llenar_pagina_2 = Mock()
        form_filler.llenar_pagina_3 = Mock()
        form_filler.hacer_clic_boton_finalizar = Mock()
        form_filler.driver.get = Mock()
        form_filler.driver.quit = Mock()

        datos = {
            'lugar': 'Test',
            'nombre_proyecto': 'Test',
            'unidad': 'Test',
            'recomendacion': 10,
            'satisfaccion': 10,
            'pagina_2': {}
        }

        with patch('builtins.input'):
            form_filler.ejecutar(datos)

        form_filler.llenar_pagina_1.assert_called_once()
        form_filler.llenar_pagina_2.assert_called_once()
        form_filler.llenar_pagina_3.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
