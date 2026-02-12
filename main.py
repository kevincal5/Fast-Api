# Importamos FastAPI para el framework, HTTPException para errores HTTP
from fastapi import FastAPI, HTTPException
# Pydantic nos permite definir esquemas de datos con validación automática
from pydantic import BaseModel
# Usamos typing para definir tipos de datos complejos (listas, opcionales)
from typing import List, Optional

# Instanciamos la aplicación. El título aparecerá en la documentación automática (/docs)
app = FastAPI(title="API de Inventario DAM/DAW")


# --- MODELO DE DATOS ---
# Definimos la estructura de un 'Producto' heredando de BaseModel.
# FastAPI usará esto para validar que el cliente envíe los datos correctos.
class Producto(BaseModel):
    id: int  # Obligatorio y debe ser entero
    nombre: str  # Obligatorio y debe ser cadena de texto
    precio: float  # Obligatorio y debe ser número decimal
    stock: int  # Obligatorio y debe ser entero


# --- BASE DE DATOS FICTICIA ---
# Simulamos una base de datos en memoria usando una lista de diccionarios
db_productos = [
    {"id": 1, "nombre": "Teclado Mecánico", "precio": 85.50, "stock": 10},
    {"id": 2, "nombre": "Ratón Gaming", "precio": 45.00, "stock": 25}
]


# --- ENDPOINTS (RUTAS) ---

# Ruta raíz: Útil para verificar que el servidor está levantado
@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "Bienvenido al sistema de inventario"}


# Listar productos: Devuelve la lista completa.
# 'response_model' asegura que la salida siempre cumpla con el formato de nuestra clase Producto.
@app.get("/productos", response_model=List[Producto], tags=["Productos"])
def obtener_productos():
    return db_productos


# Buscar un producto por ID:
# El parámetro 'producto_id' se extrae directamente de la URL.
@app.get("/productos/{producto_id}", tags=["Productos"])
def obtener_producto(producto_id: int):
    # Buscamos en nuestra "base de datos" el ID solicitado
    for p in db_productos:
        if p["id"] == producto_id:
            return p

    # Si el bucle termina sin éxito, lanzamos un error 404 (No encontrado)
    # Esto es una práctica esencial en el desarrollo de APIs profesionales.
    raise HTTPException(status_code=404, detail="Producto no encontrado")


# Crear producto (POST):
# FastAPI recibe un JSON, lo convierte en un objeto 'Producto' y lo valida.
@app.post("/productos", tags=["Productos"])
def crear_producto(nuevo: Producto):
    # Convertimos el objeto Pydantic a diccionario y lo guardamos
    db_productos.append(nuevo.dict())
    return {"mensaje": f"Producto '{nuevo.nombre}' añadido correctamente"}