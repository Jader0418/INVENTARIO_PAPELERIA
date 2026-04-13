import json  # Permite trabajar con archivos JSON
from typing import List  # Permite usar listas tipadas
from pydantic import BaseModel  # Permite crear modelos de datos validados

# MODELO

class Item(BaseModel):
    id: int        # Identificador del producto
    name: str      # Nombre del producto
    price: float   # Precio del producto


# FUNCIÓN PARA LEER DATOS

def load_items() -> List[Item]:
    """
    Esta función lee los datos almacenados en el archivo data.json
    y los convierte en una lista de objetos tipo Item.
    """
    try:
        # Abre el archivo en modo lectura ("r")
        with open("data.json", "r") as f:
            
            # Convierte el contenido JSON a una lista de diccionarios
            raw_data = json.load(f)
            
            # Convierte cada diccionario en un objeto Item
            # **item desempaqueta el diccionario en los atributos del modelo
            items = [Item(**item) for item in raw_data]
            
            # Retorna la lista de objetos Item
            return items

    except FileNotFoundError:
        # Si el archivo no existe, retorna una lista vacía
        return []

#  FUNCIÓN PARA GUARDAR DATOS

def save_items(items: List[Item]) -> None:
    """
    Esta función guarda una lista de objetos Item en el archivo data.json.
    """
    
    # Convierte cada objeto Item en un diccionario
    # Esto es necesario porque JSON no guarda objetos directamente
    data_to_save = [item.dict() for item in items]
    
    # Abre el archivo en modo escritura ("w")
    # Si no existe, lo crea automáticamente
    with open("data.json", "w") as f:
        
        # Guarda los datos en formato JSON
        # indent=2 hace que el archivo sea más legible (ordenado)
        json.dump(data_to_save, f, indent=2)


#  FUNCIÓN PARA AGREGAR UN ITEM

def add_item(new_item: Item) -> Item:
    """
    Esta función agrega un nuevo Item al archivo JSON.
    """
    
    # Carga los datos actuales del archivo
    items = load_items()
    
    # Agrega el nuevo item a la lista
    items.append(new_item)
    
    # Guarda nuevamente toda la lista con el nuevo elemento incluido
    save_items(items)
    
    # Retorna el item agregado
    return new_item

#  PRUEBA DEL PROGRAMA

if __name__ == "__main__":
    """
    Este bloque solo se ejecuta si el archivo se corre directamente.
    Sirve para probar el funcionamiento del programa.
    """

    # Crear algunos objetos de prueba
    item1 = Item(id=1, name="Cuaderno", price=5000)
    item2 = Item(id=2, name="Lapiz", price=1000)

    # Agregar los items al archivo JSON
    add_item(item1)
    add_item(item2)

    # Leer y mostrar los datos guardados
    print(load_items())