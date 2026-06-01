from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, ValidationError, field_validator
from datetime import datetime
import sqlite3
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DB_PATH = "inventario.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            descripcion TEXT NOT NULL,
            creado_en TEXT NOT NULL
        )
    """)
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_productos_nombre ON productos(nombre)")
    conn.commit()
    conn.close()


init_db()


def get_producto_by_nombre(nombre: str):
    conn = get_db()
    row = conn.execute("SELECT * FROM productos WHERE lower(nombre) = lower(?)", (nombre.strip(),)).fetchone()
    conn.close()
    return dict(row) if row else None


class ProductoPapeleria(BaseModel):
    nombre: str = Field(min_length=3, max_length=80)
    categoria: str = Field(min_length=3, max_length=40)
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)
    descripcion: str = Field(min_length=3, max_length=20)

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, value):
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío")
        return value.strip()

    @field_validator("categoria")
    @classmethod
    def validar_categoria(cls, value):
        categorias_validas = ["Estudiantil", "Oficina", "Tecnología"]
        if value not in categorias_validas:
            raise ValueError("La categoría no es válida")
        return value

    @field_validator("precio")
    @classmethod
    def validar_precio(cls, value):
        if value < 1000:
            raise ValueError("El precio debe ser igual o superior a $1.000")
        return value

    @field_validator("stock")
    @classmethod
    def validar_stock(cls, value):
        if value < 1:
            raise ValueError("El stock debe ser mínimo 1 unidad")
        if value > 150:
            raise ValueError("El stock no puede exceder 150 unidades")
        return value

    @field_validator("descripcion")
    @classmethod
    def validar_descripcion(cls, value):
        return value.strip().upper()


def get_all_productos():
    conn = get_db()
    rows = conn.execute("SELECT * FROM productos ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_producto_by_id(pid: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM productos WHERE id = ?", (pid,)).fetchone()
    conn.close()
    return dict(row) if row else None


def insert_producto(p: ProductoPapeleria):
    conn = get_db()
    conn.execute(
        "INSERT INTO productos (nombre, categoria, precio, stock, descripcion, creado_en) VALUES (?,?,?,?,?,?)",
        (p.nombre, p.categoria, p.precio, p.stock, p.descripcion, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def update_producto(pid: int, p: ProductoPapeleria):
    conn = get_db()
    conn.execute(
        "UPDATE productos SET nombre=?, categoria=?, precio=?, stock=?, descripcion=? WHERE id=?",
        (p.nombre, p.categoria, p.precio, p.stock, p.descripcion, pid)
    )
    conn.commit()
    conn.close()


def delete_producto(pid: int):
    conn = get_db()
    conn.execute("DELETE FROM productos WHERE id = ?", (pid,))
    conn.commit()
    conn.close()


def base_context(request: Request, **kwargs):
    return {
        "title": "Miscelánea Jader's",
        "heading": "Inventario de Papelería",
        "year": datetime.now().year,
        **kwargs
    }


@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):
    return ver_productos(request)


@app.get("/productos", response_class=HTMLResponse)
def ver_productos(request: Request):
    editar_id = request.query_params.get("editar")
    edit_data = None
    if editar_id:
        try:
            edit_data = get_producto_by_id(int(editar_id))
        except Exception:
            pass

    return templates.TemplateResponse(
        request=request,
        name="productos.html",
        context=base_context(
            request,
            productos=get_all_productos(),
            errores=[],
            form_data={},
            edit_data=edit_data,
        )
    )


@app.post("/productos", response_class=HTMLResponse)
def crear_producto(
    request: Request,
    nombre: str = Form(...),
    categoria: str = Form(...),
    precio: float = Form(...),
    stock: int = Form(...),
    descripcion: str = Form(...)
):
    form_data = {"nombre": nombre, "categoria": categoria,
                 "precio": precio, "stock": stock, "descripcion": descripcion}
    errores = []
    try:
        producto = ProductoPapeleria(**form_data)
        if get_producto_by_nombre(producto.nombre):
            errores.append("Ya existe un producto con ese nombre")
        else:
            insert_producto(producto)
            form_data = {}
    except ValidationError as e:
        errores = [err["msg"] for err in e.errors()]

    return templates.TemplateResponse(
        request=request,
        name="productos.html",
        context=base_context(
            request,
            productos=get_all_productos(),
            errores=errores,
            form_data=form_data,
            edit_data=None,
        )
    )


@app.post("/productos/actualizar", response_class=HTMLResponse)
def actualizar_producto(
    request: Request,
    pid: int = Form(...),
    nombre: str = Form(...),
    categoria: str = Form(...),
    precio: float = Form(...),
    stock: int = Form(...),
    descripcion: str = Form(...),
):
    errores = []
    try:
        producto = ProductoPapeleria(
            nombre=nombre, categoria=categoria,
            precio=precio, stock=stock, descripcion=descripcion
        )
        existing = get_producto_by_nombre(producto.nombre)
        if existing and existing["id"] != pid:
            errores.append("Ya existe otro producto con ese nombre")
        else:
            update_producto(pid, producto)
    except ValidationError as e:
        errores = [err["msg"] for err in e.errors()]

    return templates.TemplateResponse(
        request=request,
        name="productos.html",
        context=base_context(
            request,
            productos=get_all_productos(),
            errores=errores,
            form_data={},
            edit_data=None,
        )
    )


@app.post("/productos/eliminar", response_class=HTMLResponse)
def eliminar_producto(request: Request, pid: int = Form(...)):
    errores = []
    try:
        delete_producto(pid)
    except Exception as e:
        errores.append(str(e))

    return templates.TemplateResponse(
        request=request,
        name="productos.html",
        context=base_context(
            request,
            productos=get_all_productos(),
            errores=errores,
            form_data={},
            edit_data=None,
        )
    )