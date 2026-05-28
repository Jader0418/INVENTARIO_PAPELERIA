# MISCELANEA JADER — Inventario de Papelería

Aplicación web sencilla para administrar el inventario de una papelería, desarrollada con FastAPI y Jinja2.

---

## Descripción

Esta aplicación permite crear, editar, eliminar y listar productos de una papelería desde una interfaz web ligera.

El objetivo es ofrecer una base clara y fácil de personalizar para proyectos pequeños o prototipos de gestión de inventario.

## Características principales

- Gestión de productos en una sola vista.
- Validación de formulario en el servidor mediante Pydantic.
- Edición y eliminación de productos directamente desde la tabla.
- Plantillas Jinja2 y CSS personalizado para un diseño limpio.

## Estructura del proyecto

- `main.py` — Servidor FastAPI con rutas para CRUD de productos.
- `templates/productos.html` — Vista principal con formulario y tabla de productos.
- `static/style.css` — Estilos para la interfaz.
- `data.json` — Archivo presente en el repositorio, sin uso activo en la implementación actual.

## Requisitos

- Python 3.10 o superior
- Paquetes:

```bash
python -m pip install fastapi uvicorn jinja2 python-multipart
```

## Instalación rápida

```bash
git clone <repositorio>
cd INVENTARIO_PAPELERIA
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn jinja2 python-multipart
```

## Ejecución

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Abre `http://127.0.0.1:8000` en tu navegador.

## Endpoints disponibles

- `GET /` — Página principal.
- `GET /productos` — Muestra la lista de productos y el formulario.
- `POST /productos` — Agrega un producto.
- `POST /productos/actualizar` — Actualiza un producto existente.
- `POST /productos/eliminar` — Elimina un producto.

> Nota: El almacenamiento actual es en memoria (`productos_db`). Los datos se perderán al reiniciar la aplicación.

## Validaciones de producto

La clase `ProductoPapeleria` aplica las siguientes validaciones:

- `nombre`: mínimo 3 caracteres, sin espacios vacíos.
- `categoria`: valores permitidos: `Estudiantil`, `Oficina`, `Tecnología`.
- `precio`: mayor que 0.
- `stock`: entero mayor o igual a 0.
- `Descripcion`: se normaliza y se guarda en mayúsculas.

## Personalización

- Edita los textos y los datos de la papelería en `templates/productos.html`.
- Para persistencia real, integra lectura/escritura en `data.json`, una base de datos SQLite o cualquier otro motor.

## Mejora recomendada

- Implementar persistencia de datos en `data.json` o SQLite.
- Añadir autenticación para proteger el acceso.
- Exportar el inventario a CSV o PDF.

## Contribuciones

1. Crea una nueva rama: `feature/mi-cambio`.
2. Realiza commits pequeños y descriptivos.
3. Abre un Pull Request explicando tus cambios.

## Licencia

No se incluye una licencia explícita. Si deseas compartir el proyecto públicamente, añade un archivo `LICENSE`.

## Contacto

Para consultas o mejoras adicionales (persistencia, autenticación, exportación de datos, etc.), contáctame y lo ajustamos.