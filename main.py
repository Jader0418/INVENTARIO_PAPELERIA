from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json

app = FastAPI()

#  Modelo
class Item(BaseModel):
    id: int
    name: str
    price: float

# Archivo JSON
FILE_NAME = "data.json"

# 🔹 FUNCIONES DE ARCHIVO


def load_items() -> List[Item]:
    try:
        with open(FILE_NAME, "r") as f:
            raw_data = json.load(f)
            items = [Item(**item) for item in raw_data]
            return items
    except FileNotFoundError:
        return []

def save_items(items: List[Item]):
    with open(FILE_NAME, "w") as f:
        json.dump([item.dict() for item in items], f, indent=4)

# 🔹 ENDPOINTS

# Obtener todos los items
@app.get("/items", response_model=List[Item])
def get_items():
    return load_items()

#  Crear un item
@app.post("/items", response_model=Item)
def create_item(item: Item):
    items = load_items()

    #  Validar ID único
    for i in items:
        if i.id == item.id:
            raise HTTPException(status_code=400, detail="El ID ya existe")

    items.append(item)
    save_items(items)
    return item