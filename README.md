# Automatización de Formulario de Qualtrics

Proyecto de automatización para el formulario de **Preescolar Integrales Bogotá y Cundinamarca** de Colsubsidio usando Selenium y Python.

## 🚀 Características

- ✅ Automatización completa del formulario de Qualtrics
- ✅ Manejo de modales condicionales (preguntas que aparecen según respuestas)
- ✅ Soporte para múltiples páginas
- ✅ Configuración mediante archivo JSON
- ✅ Script de inspección para identificar campos del formulario
- ✅ Logging detallado para debugging
- ✅ Manejo robusto de errores

## 📋 Requisitos

- Python 3.7+
- Google Chrome instalado
- ChromeDriver (se descarga automáticamente con selenium 4.11+)

## 🔧 Instalación

1. **Clonar el repositorio** (si aplica) o crear un directorio:
```bash
mkdir forms-automation
cd forms-automation
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

## 📁 Estructura del Proyecto

```
forms-sebas/
│
├── form_automation.py       # Clase principal de automatización
├── form_inspector.py         # Script para inspeccionar campos del formulario
├── run_form_automation.py    # Script ejecutable con configuración JSON
├── form_config.json          # Archivo de configuración (datos del formulario)
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Este archivo
```

## 🎯 Uso

### Opción 1: Inspeccionar el formulario primero (RECOMENDADO)

Antes de automatizar, es importante identificar los campos del formulario:

```bash
python form_inspector.py
```

Este script:
- Abre el formulario en Chrome
- Lista todos los campos (texto, radio buttons, checkboxes, dropdowns)
- Muestra los IDs, nombres y valores de cada campo
- Te permite navegar página por página
- Te ayuda a completar el archivo `form_config.json`

**Cómo usar el inspector:**
1. Ejecuta el script
2. Revisa cada página y anota los IDs de los campos que quieres llenar
3. Presiona ENTER para avanzar a la siguiente página
4. Escribe 'q' y ENTER para salir
5. Actualiza `form_config.json` con los datos reales

### Opción 2: Ejecutar con configuración JSON

Una vez que hayas actualizado `form_config.json` con los datos correctos:

```bash
python run_form_automation.py
```

**Opciones adicionales:**

```bash
# Ejecutar en modo headless (sin ventana)
python run_form_automation.py --headless

# Usar un archivo de configuración diferente
python run_form_automation.py --config mi_config.json
```

### Opción 3: Usar el módulo directamente en Python

```python
from form_automation import QualtricsFormFiller

# Inicializar
form_filler = QualtricsFormFiller(headless=False)

# Navegar al formulario
form_filler.navigate_to_form("URL_DEL_FORMULARIO")

# Definir datos de una página
page_data = {
    'text_fields': {
        'QR~QID1': 'Juan Pérez',
        'QR~QID2': 'juan@ejemplo.com'
    },
    'radio_buttons': [
        'Sí',  # Selecciona el radio button con label "Sí"
    ],
    'conditional_modals': [
        {
            'trigger': 'SI',
            'modal_data': {
                'text_fields': {
                    'modal_field': 'Datos del modal'
                }
            }
        }
    ]
}

# Llenar página
form_filler.fill_form_page(page_data)

# Avanzar
form_filler.click_next_button()

# Cerrar
form_filler.close()
```

## ⚙️ Configuración del Formulario

Edita el archivo `form_config.json` para especificar los datos que quieres ingresar:

```json
{
  "form_url": "https://colsubsidio.az1.qualtrics.com/jfe/form/SV_dhz8RuGCTqJm1Ui",
  "pages": [
    {
      "page_number": 1,
      "name": "Página 1 - Datos personales",
      "fields": {
        "text_fields": {
          "QR~QID1": "Nombre completo",
          "QR~QID2": "correo@ejemplo.com"
        },
        "radio_buttons": [
          "Sí"
        ],
        "conditional_modals": [
          {
            "trigger": "SI",
            "modal_data": {
              "text_fields": {
                "campo_modal": "Valor"
              }
            }
          }
        ]
      }
    }
  ]
}
```

### Tipos de campos soportados:

1. **text_fields**: Campos de texto, email, teléfono, textarea
   ```json
   "text_fields": {
     "campo_id": "valor a ingresar"
   }
   ```

2. **radio_buttons**: Botones de radio (por texto del label)
   ```json
   "radio_buttons": [
     "Opción 1",
     "Sí"
   ]
   ```

3. **radio_by_value**: Botones de radio (por name y value)
   ```json
   "radio_by_value": {
     "nombre_campo": "valor"
   }
   ```

4. **checkboxes**: Casillas de verificación
   ```json
   "checkboxes": {
     "checkbox_id": true
   }
   ```

5. **dropdowns**: Menús desplegables
   ```json
   "dropdowns": {
     "select_id": "Opción a seleccionar"
   }
   ```

6. **conditional_modals**: Modales que aparecen según respuestas
   ```json
   "conditional_modals": [
     {
       "trigger": "SI",
       "modal_data": {
         "text_fields": {...},
         "radio_by_value": {...}
       }
     }
   ]
   ```

## 🔍 Manejo de Modales Condicionales

El formulario de Qualtrics puede mostrar modales o preguntas adicionales basadas en tus respuestas. Este proyecto maneja esto automáticamente:

1. **Define el trigger**: La respuesta que activa el modal (ej: "SI", "NO", "Otro")
2. **Especifica modal_data**: Los campos que aparecen en el modal
3. El script detecta automáticamente cuando aparece un modal
4. Llena los campos del modal según la configuración
5. Cierra el modal y continúa

**Ejemplo:**

Si seleccionas "Sí" en una pregunta y esto abre un modal con más preguntas:

```json
{
  "radio_buttons": ["Sí"],
  "conditional_modals": [
    {
      "trigger": "SI",
      "modal_data": {
        "text_fields": {
          "motivo_field": "Mi razón para decir sí"
        }
      }
    }
  ]
}
```

## 🛠️ Métodos Principales de la Clase

### QualtricsFormFiller

```python
# Navegación
navigate_to_form(url)

# Llenar campos
fill_text_field(field_id, value)
select_radio_by_label(label_text)
select_radio_by_value(name, value)
select_checkbox(checkbox_id, check=True)
select_dropdown(select_id, option_text)

# Modales
handle_conditional_modal(trigger_response, modal_data)

# Navegación de páginas
click_next_button()

# Utilidades
wait_for_element(by, value, timeout)
wait_for_clickable(by, value, timeout)
```

## 📝 Ejemplo Completo

```python
from form_automation import QualtricsFormFiller

# Crear instancia
bot = QualtricsFormFiller(headless=False)

# Ir al formulario
bot.navigate_to_form("https://colsubsidio.az1.qualtrics.com/jfe/form/SV_dhz8RuGCTqJm1Ui")

# Página 1
page_1 = {
    'text_fields': {
        'nombre_id': 'Ana García',
        'email_id': 'ana@ejemplo.com'
    },
    'radio_buttons': ['Sí'],
    'conditional_modals': [
        {
            'trigger': 'SI',
            'modal_data': {
                'text_fields': {
                    'explicacion': 'Detalle adicional'
                }
            }
        }
    ]
}

bot.fill_form_page(page_1)
bot.click_next_button()

# Página 2
page_2 = {
    'radio_buttons': ['Opción B'],
    'checkboxes': {
        'acepto_terminos': True
    }
}

bot.fill_form_page(page_2)
bot.click_next_button()

# Cerrar
bot.close()
```

## 🐛 Debugging y Logs

El proyecto incluye logging detallado. Los mensajes muestran:
- ✅ Campos llenados exitosamente
- ⚠️ Advertencias (timeouts, elementos no encontrados)
- ❌ Errores con traceback completo

Para aumentar el nivel de detalle:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## ⚠️ Consideraciones Importantes

1. **IDs dinámicos**: Qualtrics puede generar IDs dinámicos. Usa el inspector para identificar los correctos.

2. **Tiempos de espera**: El script incluye esperas para cargar elementos dinámicos. Ajusta según tu conexión.

3. **Captchas**: Si el formulario tiene captcha, la automatización no funcionará.

4. **Términos de servicio**: Asegúrate de tener permiso para automatizar el formulario.

5. **Rate limiting**: No ejecutes el script repetidamente en poco tiempo para evitar bloqueos.

## 🆘 Solución de Problemas

### El script no encuentra un campo

1. Ejecuta `form_inspector.py` para ver el ID real
2. Verifica que el ID en `form_config.json` es correcto
3. Asegúrate de que el campo está en la página correcta

### El modal no se maneja correctamente

1. Verifica que el `trigger` coincide con el texto de la opción
2. Revisa los IDs de los campos del modal con el inspector
3. Aumenta los tiempos de espera si el modal tarda en cargar

### Error "Element not clickable"

- El elemento puede estar oculto o fuera de la vista
- El script hace scroll automático, pero puedes ajustar los tiempos de espera

### ChromeDriver no funciona

Con Selenium 4.11+, ChromeDriver se descarga automáticamente. Si hay problemas:
```bash
pip install --upgrade selenium
```

## 📞 Soporte

Para problemas o dudas:
1. Revisa los logs del script
2. Ejecuta el inspector para verificar los campos
3. Ajusta los tiempos de espera si es necesario

## 📄 Licencia

Este proyecto es para uso educativo y de automatización autorizada.

## 🎉 ¡Listo!

Ahora puedes automatizar el formulario de Qualtrics de manera eficiente y manejar todas las condiciones dinámicas del mismo.
