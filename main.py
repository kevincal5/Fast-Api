from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

# 1. Creamos la instancia de la aplicación
app = FastAPI()

# 2. Definimos un modelo de datos usando Pydantic
# Esto nos ayuda a validar que los datos que nos envíen sean correctos
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

# 3. Definimos una ruta básica (GET)
# Al entrar a la raíz "/" devolverá este diccionario JSON
@app.get("/")
def read_root():
    return {"Mensaje": "¡Hola! Bienvenido a mi API con FastAPI"}

# 4. Ruta con parámetros (GET)
# Capturamos el 'item_id' de la URL y un parámetro opcional 'q'
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "query_param": q}

# 5. Ruta para crear datos (POST)
# FastAPI validará automáticamente que el 'item' tenga nombre y precio
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id, "price": item.price}