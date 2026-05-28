# MISCELANEA JADER — Inventario de Papelería

Interfaz web ligera para gestionar un inventario de papelería: agregar, editar, eliminar y listar productos.

---

## Resumen

Proyecto minimalista construido con FastAPI y Jinja2 que permite administrar productos de una papelería llamada **MISCELANEA JADER**. Está pensado como una base fácil de extender para aplicaciones pequeñas o prototipos.

Características principales:
- Interfaz web organizada y funcional.
- Formulario para crear productos con validación de servidor.
- Edición y eliminación de productos desde la misma vista.
- Estilos CSS sencillos para una buena experiencia de usuario.

## Estructura del repositorio

- `main.py` — Aplicación FastAPI con rutas para ver, crear, actualizar y eliminar productos.
- `templates/` — Plantillas Jinja2 (`productos.html`).
- `static/style.css` — Estilos para la interfaz.
- `data.json` — Archivo opcional; la implementación actual usa almacenamiento temporal en memoria.

## Requisitos

- Python 3.10+
- Dependencias:

```bash
python -m pip install fastapi uvicorn jinja2 python-multipart
```

## Instalación y ejecución

1. Clona o copia el repositorio en tu máquina.
2. (Recomendado) Crea y activa un entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn jinja2 python-multipart
```

3. Ejecuta la aplicación:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

4. Abre el navegador en: `http://127.0.0.1:8000`

## Endpoints disponibles

- `GET /` — Página principal con la lista de productos.
- `GET /productos` — Misma vista que `/`, con soporte opcional de edición.
- `POST /productos` — Crea un producto nuevo desde el formulario.
- `POST /productos/actualizar` — Actualiza un producto existente.
- `POST /productos/eliminar` — Elimina un producto.

> Nota: los datos se guardan en memoria en la variable `productos_db` de `main.py`. Al reiniciar la aplicación, los productos se perderán.

## Validaciones de producto

La clase `ProductoPapeleria` valida los campos de cada producto:
- `nombre`: no puede estar vacío y debe tener entre 3 y 80 caracteres.
- `categoria`: debe ser una de `Estudiantil`, `Oficina`, `Tecnología`.
- `precio`: debe ser un número mayor que 0.
- `stock`: debe ser un entero mayor o igual a 0.
- `Descripcion`: se normaliza y guarda en mayúsculas.

## Diseño y UX

La plantilla `templates/productos.html` incluye:
- Un bloque informativo para la papelería.
- Formulario de alta de productos con validación en el servidor.
- Tabla de productos con botones para `Editar` y `Eliminar`.
- Estilos responsivos en `static/style.css`.

## Personalización rápida

- Ajusta los textos y datos de la papelería en `templates/productos.html`.
- Para persistencia real, reemplaza `productos_db` por lectura/escritura en `data.json`, SQLite u otra base de datos.

## Contribuciones

1. Crea una rama nueva (`feature/mi-cambio`).
2. Haz commits claros y descriptivos.
3. Envía un Pull Request con la descripción de tus cambios.

## Licencia

Este proyecto no define una licencia explícita. Si deseas uso público o colaboración abierta, añade un archivo `LICENSE`.

## Contacto

Si necesitas ayuda con la app (persistencia, autenticación, exportes CSV, etc.), dime y lo adaptamos.

---

Gracias por usar MISCELANEA JADER. ¡Listo para seguir mejorando!