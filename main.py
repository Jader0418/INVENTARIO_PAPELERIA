from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, ValidationError, field_validator
from datetime import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

productos_db = []


class ProductoPapeleria(BaseModel):
    nombre: str = Field(min_length=3, max_length=80)
    categoria: str = Field(min_length=3, max_length=40)
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)
    Descripcion: str = Field(min_length=3, max_length=20)

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, value):
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío")
        return value.strip()

    @field_validator("categoria")
    @classmethod
    def validar_categoria(cls, value):
        categorias_validas = ["Escolar", "Oficina", "Arte", "Tecnología"]
        if value not in categorias_validas:
            raise ValueError("La categoría no es válida")
        return value

    @field_validator("Descripcion")
    @classmethod
    def validar_Descripcion(cls, value):
        return value.strip().upper()


@app.get("/")
def inicio(request: Request):
    # Mostrar directamente la vista de productos en la raíz
    return ver_productos(request)


@app.get("/productos", response_class=HTMLResponse)
def ver_productos(request: Request):
    # Permitir indicar un índice a editar mediante query param ?editar=0
    editar = request.query_params.get("editar")
    edit_index = None
    edit_data = None
    if editar is not None:
        try:
            idx = int(editar)
            if 0 <= idx < len(productos_db):
                edit_index = idx
                # convertir el modelo pydantic a dict para rellenar el formulario
                edit_data = productos_db[idx].model_dump()
        except Exception:
            edit_index = None

    return templates.TemplateResponse(
        "productos.html",
        {
            "request": request,
            "title": "Papelería Central",
            "heading": "Inventario de Papelería",
            "year": datetime.now().year,
            "productos": productos_db,
            "errores": [],
            "form_data": {},
            "edit_index": edit_index,
            "edit_data": edit_data,
        }
    )


@app.post("/productos", response_class=HTMLResponse)
def crear_producto_html(
    request: Request,
    nombre: str = Form(...),
    categoria: str = Form(...),
    precio: float = Form(...),
    stock: int = Form(...),
    Descripcion: str = Form(...)
):
    form_data = {
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock,
        "Descripcion": Descripcion
    }

    try:
        producto = ProductoPapeleria(
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            stock=stock,
            Descripcion=Descripcion
        )
        productos_db.append(producto)
        errores = []
        form_data = {}
    except ValidationError as e:
        errores = [err["msg"] for err in e.errors()]

    return templates.TemplateResponse(
        "productos.html",
        {
            "request": request,
            "title": "Papelería Central",
            "heading": "Inventario de Papelería",
            "year": datetime.now().year,
            "productos": productos_db,
            "errores": errores,
            "form_data": form_data
        }
    )


@app.post("/productos/actualizar", response_class=HTMLResponse)
def actualizar_producto_html(
    request: Request,
    idx: int = Form(...),
    nombre: str = Form(...),
    categoria: str = Form(...),
    precio: float = Form(...),
    stock: int = Form(...),
    Descripcion: str = Form(...),
):
    errores = []
    try:
        producto = ProductoPapeleria(
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            stock=stock,
            Descripcion=Descripcion,
        )
        if 0 <= idx < len(productos_db):
            productos_db[idx] = producto
        else:
            errores.append("Índice de producto inválido")
    except ValidationError as e:
        errores = [err["msg"] for err in e.errors()]

    return templates.TemplateResponse(
        "productos.html",
        {
            "request": request,
            "title": "Papelería Central",
            "heading": "Inventario de Papelería",
            "year": datetime.now().year,
            "productos": productos_db,
            "errores": errores,
            "form_data": {},
            "edit_index": None,
            "edit_data": None,
        },
    )


@app.post("/productos/eliminar", response_class=HTMLResponse)
def eliminar_producto_html(request: Request, idx: int = Form(...)):
    errores = []
    try:
        if 0 <= idx < len(productos_db):
            productos_db.pop(idx)
        else:
            errores.append("Índice de producto inválido")
    except Exception as e:
        errores.append(str(e))

    return templates.TemplateResponse(
        "productos.html",
        {
            "request": request,
            "title": "Papelería Central",
            "heading": "Inventario de Papelería",
            "year": datetime.now().year,
            "productos": productos_db,
            "errores": errores,
            "form_data": {},
            "edit_index": None,
            "edit_data": None,
        },
    )