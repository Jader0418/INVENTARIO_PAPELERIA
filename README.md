# MISCELANEA JADER — Inventario de Papelería

Interfaz web ligera para gestionar un inventario de papelería: agregar, editar, eliminar y listar productos.

---

## Resumen

Proyecto minimalista construido con FastAPI y Jinja2 que permite administrar productos de una papelería llamada **MISCELANEA JADER**. Está pensado como una base fácil de extender para aplicaciones pequeñas o prototipos.

Características principales:
- Interfaz web organizada y responsiva.
- Formulario para agregar productos con validación.
- Edición in-place y eliminación de productos desde la tabla.
- Estilos CSS sencillos y funcionales para una buena experiencia de usuario.

## Estructura del repositorio

- `main.py` — Aplicación FastAPI; rutas para ver/crear/editar/eliminar productos.
- `templates/` — Plantillas Jinja2 (principal: `productos.html`).
- `static/style.css` — Estilos para la interfaz.
- `data.json` — (opcional) presente en el repositorio; la implementación actual usa almacenamiento en memoria.

## Requisitos

- Python 3.10+ (recomendado)
- Dependencias (instalarlas en un entorno virtual):

```bash
python -m pip install fastapi uvicorn jinja2 python-multipart
```

## Instalación y ejecución

1. Clona o copia el repositorio en tu máquina.
2. (Opcional) Crea y activa un entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn jinja2 python-multipart
```

3. Inicia la aplicación:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

4. Abre en el navegador: `http://127.0.0.1:8000`

## Endpoints disponibles

- `GET /` — Página principal (muestra `productos.html`).
- `GET /productos` — Lista y formulario (misma vista que `/`).
- `POST /productos` — Crear un producto (envío desde formulario).
- `POST /productos/actualizar` — Actualizar un producto existente (recibe `idx` y campos).
- `POST /productos/eliminar` — Eliminar producto (recibe `idx`).

Nota: los productos se almacenan actualmente en memoria en la variable `productos_db` en `main.py`. Si reinicias la app, los datos se perderán. Se puede adaptar fácilmente para persistencia en `data.json`, SQLite u otra DB.

## Validaciones

La clase `ProductoPapeleria` (Pydantic) valida campos básicos:
- `nombre`: longitud mínima y sin espacios vacíos.
- `categoria`: debe ser una de `Escolar`, `Oficina`, `Arte`, `Tecnología`.
- `precio`: mayor que 0.
- `stock`: entero >= 0.
- `Descripcion`: se normaliza y guarda en mayúsculas.

## Diseño y UX

La plantilla `templates/productos.html` incluye:
- Un bloque informativo para **MISCELANEA JADER** (dirección, horario, contacto, misión).
- Formulario de alta con ayudas y validación básica del lado del servidor.
- Tabla con las acciones `Editar` y `Eliminar` por fila.
- Estilos responsivos en `static/style.css`.

## Personalización rápida

- Cambia los textos (nombre, dirección, horario) editando `templates/productos.html` en la sección `hero`.
- Para persistir datos, reemplaza el uso de `productos_db` por lectura/escritura en `data.json` o una base de datos.

## Contribuciones

1. Haz un fork y crea una rama (`feature/mi-cambio`).
2. Realiza commits claros y descriptivos.
3. Abre un Pull Request con la descripción de los cambios.

## Licencia

Este repositorio no incluye una licencia explícita. Para uso público, añade un archivo `LICENSE` (por ejemplo MIT) si deseas permitir reutilización.

## Contacto

Si necesitas ayuda o quieres que adapte la aplicación (persistencia, autenticación, exportes CSV, etc.), contáctame y lo implemento.

---

Gracias por usar MISCELANEA JADER — listo para seguir mejorando según tus necesidades.
