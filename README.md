# API de Formularios Colsubsidio

API REST construida con FastAPI para automatizar el llenado de formularios de Colsubsidio usando Selenium.

## Estructura del Proyecto

```
forms-sebas/
├── form1.py              # Formulario 1 - Preescolar Integrales
├── form2.py              # Formulario 2 - Jardín Infantil
├── form3.py              # Formulario 3 - Jardín con Unidad
├── form4.py              # Formulario 4 - Familia y Comunidad
├── app.py                # API FastAPI principal
├── test_form1.py         # Tests unitarios para form1
├── test_form2.py         # Tests unitarios para form2
├── test_form3.py         # Tests unitarios para form3
├── test_form4.py         # Tests unitarios para form4
├── requirements.txt      # Dependencias del proyecto
└── README.md            # Este archivo
```

## Instalación

1. Clonar el repositorio (si aplica)
2. Crear un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Instalar ChromeDriver (para Selenium):
   - Descargar desde: https://chromedriver.chromium.org/
   - Asegurarse de que esté en el PATH del sistema

## Uso

### Iniciar la API

```bash
python app.py
```

O usando uvicorn directamente:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

### Endpoints Disponibles

#### 1. Formulario 1

**POST** `/api/v1/form1`

```json
{
  "institucion": "Colegio San José",
  "proyecto": "Preescolar Integral 2025",
  "recomendacion": 10,
  "recomendacion_text": "Excelente servicio",
  "satisfaccion": 10,
  "satisfaccion_text": "Muy satisfecho",
  "pagina_2": {
    "atencion": [10, 10, 10, 10, 10, 10, 10],
    "talento_humano": [10, 10, 10, 10, 10, 10, 10, 10, 10],
    "psicosocial": [10, 10, 10, 10, 10, 10, 10],
    "dinamizadores": [10, 10, 10, 10, 10, 10, 10],
    "contacto_dinamizador": "No",
    "contacto_coordinador": "Si",
    "aspectos_satisfaccion": [10, 10, 10, 10, 10],
    "pqrs_medios": ["Pagina web", "Correo electronico"],
    "ha_reclamado": "No",
    "desarrollo_propuesta": [10, 10, 10, 10, 10, 10, 10],
    "sugerencias": "Excelente programa"
  }
}
```

#### 2. Formulario 2

**POST** `/api/v1/form2`

```json
{
  "lugar": "Colegio San José",
  "nombre_proyecto": "Jardín Infantil 2025",
  "recomendacion": 10,
  "satisfaccion": 10,
  "pagina_2": {
    "proceso_aprendizaje": [10, 10, 10, 10, 10],
    "habilidades_docentes": [10, 10, 10, 10, 10, 10, 10],
    "auxiliar_salud_nutricion": [10, 10, 10, 10],
    "personal_administrativo": [10, 10, 10, 10],
    "actividades_administrativas": [10, 10, 10, 10],
    "alimentacion": [10, 10, 10, 10],
    "desarrollo_propuesta": [10, 10, 10, 10, 10, 10, 10],
    "profesionales_psicosocial": [10, 10, 10, 10, 10],
    "nutricionista": [10, 10, 10, 10, 10],
    "evaluacion_aspectos": [10, 10, 10, 10, 10],
    "apoyo_piscosocial": "No",
    "contacto_nutricionista": "Si",
    "especialista_desarrollo": "Si",
    "pqrs_medios": ["Pagina web"],
    "ha_reclamado": "No",
    "sugerencias": "Excelente programa"
  }
}
```

#### 3. Formulario 3

**POST** `/api/v1/form3`

Similar al formulario 2, pero incluye campo `unidad` y `coordinador_zona`:

```json
{
  "lugar": "Colegio San José",
  "nombre_proyecto": "Jardín con Unidad 2025",
  "unidad": "Unidad Educativa Bogotá",
  "recomendacion": 10,
  "satisfaccion": 10,
  "pagina_2": {
    // ... campos similares a form2
    "coordinador_zona": [10, 10, 10, 10]
  }
}
```

#### 4. Formulario 4

**POST** `/api/v1/form4`

Similar al formulario 2, pero incluye campos adicionales:

```json
{
  "lugar": "Colegio San José",
  "nombre_proyecto": "Familia y Comunidad 2025",
  "recomendacion": 10,
  "satisfaccion": 10,
  "pagina_2": {
    // ... campos similares a form2
    "acompanamiento_familia": [10, 10, 10, 10, 10],
    "coordinador_pedagogico": [10, 10, 10, 10]
  }
}
```

#### 5. Consultar Estado de Tarea

**GET** `/api/v1/tasks/{task_id}`

Respuesta:
```json
{
  "task_id": "uuid-aqui",
  "status": "completed",
  "form_type": "form1",
  "created_at": "2025-01-15T10:00:00",
  "completed_at": "2025-01-15T10:01:30",
  "error": null,
  "result": {
    "message": "Formulario completado exitosamente"
  }
}
```

#### 6. Listar Tareas

**GET** `/api/v1/tasks?status=completed&form_type=form1&limit=10`

#### 7. Eliminar Tarea

**DELETE** `/api/v1/tasks/{task_id}`

## Ejecutar Tests

Ejecutar todos los tests:

```bash
pytest
```

Ejecutar tests con cobertura:

```bash
pytest --cov=. --cov-report=html
```

Ejecutar tests de un formulario específico:

```bash
pytest test_form1.py -v
```

## Estructura de Datos

### Campos Comunes

Todos los formularios comparten:

- `recomendacion`: Nivel de recomendación (0-10)
- `recomendacion_text`: Texto obligatorio si recomendación < 9
- `satisfaccion`: Nivel de satisfacción (1-10)
- `satisfaccion_text`: Texto obligatorio si satisfacción <= 6
- `pqrs_medios`: Lista de medios para PQRS
- `ha_reclamado`: "Si" o "No"
- `sugerencias`: Texto de sugerencias (opcional)

### Campos de Escala

Todos los campos que terminan en lista de números (ej: `atencion`, `talento_humano`)
aceptan valores del 1 al 10.

## Notas Importantes

1. **ChromeDriver**: Asegúrate de tener ChromeDriver instalado y en el PATH
2. **Ejecución en Background**: Los formularios se ejecutan en segundo plano (background tasks)
3. **Almacenamiento**: Las tareas se almacenan en memoria (en producción usar DB)
4. **Modo Headless**: Para ejecutar sin ventana visible, descomentar la línea en cada form:
   ```python
   chrome_options.add_argument('--headless')
   ```

## Ejemplos de Uso con cURL

### Ejecutar Form1:

```bash
curl -X POST "http://localhost:8000/api/v1/form1" \
  -H "Content-Type: application/json" \
  -d '{
    "institucion": "Colegio Test",
    "proyecto": "Proyecto Test",
    "recomendacion": 10,
    "satisfaccion": 10,
    "pagina_2": {
      "atencion": [10,10,10,10,10,10,10],
      "talento_humano": [10,10,10,10,10,10,10,10,10],
      "psicosocial": [10,10,10,10,10,10,10],
      "dinamizadores": [10,10,10,10,10,10,10],
      "contacto_dinamizador": "No",
      "contacto_coordinador": "Si",
      "aspectos_satisfaccion": [10,10,10,10,10],
      "desarrollo_propuesta": [10,10,10,10,10,10,10],
      "pqrs_medios": ["Pagina web"],
      "ha_reclamado": "No"
    }
  }'
```

### Consultar estado de tarea:

```bash
curl -X GET "http://localhost:8000/api/v1/tasks/{task_id}"
```

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto es para uso interno de Colsubsidio.

## Contacto

Para preguntas o soporte, contactar al equipo de desarrollo.
