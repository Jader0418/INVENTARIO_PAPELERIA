import json
from typing import List
from pydantic import BaseModel

#  Modelo
class Item(BaseModel):
    id: int
    name: str
    price: float


#  FUNCIÓN PARA LEER

def load_items() -> List[Item]:
    try:
        with open("data.json", "r") as f:
            raw_data = json.load(f)  # Lee lista de dicts
            items = [Item(**item) for item in raw_data]  # Convierte a objetos Item
            return items
    except FileNotFoundError:
        return []


#  FUNCIÓN PARA GUARDAR

def save_items(items: List[Item]) -> None:
    data_to_save = [item.dict() for item in items]
    with open("data.json", "w") as f:
        json.dump(data_to_save, f, indent=2)