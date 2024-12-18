import sqlite3
from colorama import *

ruta_db = "inventario.db"

init() # Se inicia colorama

# Función que crea la tabla "productos" si no existe
def crear_tabla_productos_dt():
    try:
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS productos(
                       Id INTEGER PRIMARY KEY AUTOINCREMENT,
                       Nombre TEXT NOT NULL,
                       Descripcion TEXT,
                       Categoria TEXT NOT NULL,
                       Cantidad INTEGER NOT NULL,
                       Precio REAL NOT NULL
                       )""")
        conexion.commit()
    except sqlite3.Error as error:
        print(f"Error al crear la tabla: {error}")
    finally:
        conexion.close()

# Función que agrega un producto nuevo a la tabla recibido por parámetro y retorna un booleano indicando True si se agregó o False si no se agregó
def insertar_producto_dt(producto)-> bool:
    producto_insertado = False

    try:
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        query = "INSERT INTO productos(Nombre, Descripcion, Categoria, Cantidad, Precio) VALUES (?, ?, ?, ?, ?)"
        placeholders = (
            producto["Nombre"],
            producto["Descripcion"],
            producto["Categoria"],
            producto["Cantidad"],
            producto["Precio"]
        )
        cursor.execute(query, placeholders)
        conexion.commit()
        producto_insertado = True
    except sqlite3.IntegrityError as error:
        print(f"Error al insertar el producto: {error}")
    finally:
        conexion.close()
    
    return producto_insertado

# Función que recupera todos los datos guardados en la tabla y los retorna en una lista
def obtener_productos_db()-> list:
    lista_productos = None

    try:
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        query = "SELECT * FROM productos"
        cursor.execute(query)
        filas = cursor.fetchall()
        columnas = [description[0] for description in cursor.description]
        lista_productos = [filas, columnas]
    except sqlite3.Error as error:
        print(f"Error al obtener los productos: {error}")
    finally:
        conexion.close()

    return lista_productos

# Función que busca un producto de la tabla por Id recibido por parámetro y retorna una tupla si se encuentra o None si no lo hace
def buscar_producto_por_id_db(id)-> tuple:
    producto = None

    try:
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        query = "SELECT * FROM productos WHERE Id = ?"
        placeholders = (id, )
        cursor.execute(query, placeholders)
        producto = cursor.fetchone()
    except sqlite3.Error as error:
        print(f"Producto no encontrado: {error}")
    finally:
        conexion.close()

    return producto

# Función que recibe un Id por parámetro para buscar un producto y lo elimina si se encuentra. Retorna True si se elimina o False en caso contrario
def eliminar_producto_db(id)-> bool:
    producto_eliminado = False

    try:
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        query = "DELETE FROM productos WHERE Id = ?"
        placeholders = (id,)
        cursor.execute(query, placeholders)
        conexion.commit()
        producto_eliminado = True
    except sqlite3.Error as error:
        print(f"El producto no pudo ser eliminado: {error}")
    finally:
        conexion.close()

    return producto_eliminado

# Función que recibe un Id y una cantidad por parámetro para buscar y actualizar la cantidad de un producto específico.
# Se buscar por Id el producto. Se retorna True si se actualizó el producto o False en caso contrario.
def actualizar_cantidad_producto_db(id, cantidad_nueva)-> bool:
    producto_actualizado = False

    try:
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        query = "UPDATE productos SET Cantidad = ? WHERE Id = ?"
        placeholders = (cantidad_nueva, id)
        cursor.execute(query, placeholders)
        conexion.commit()
        producto_actualizado = True
    except sqlite3.Error as error:
        print(f"La cantidad del producto no pudo ser actualizada: {error}")
    finally:
        conexion.close()

    return producto_actualizado

# Función que busca un producto de la tabla por el nombre recibido por parámetro y retorna una lista si se encuentra o None si no lo hace
def buscar_producto_por_nombre_db(nombre)-> list:
    lista_productos = None

    try:
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        query = "SELECT * FROM productos WHERE Nombre = ?"
        placeholders = (nombre, )
        cursor.execute(query, placeholders)
        filas = cursor.fetchall()
        columnas = [description[0] for description in cursor.description]
        lista_productos = [filas, columnas]
    except sqlite3.Error as error:
        print(f"Nombre no encontrado: {error}")
    finally:
        conexion.close()

    return lista_productos

# Función que busca un producto de la tabla por la categoría recibida por parámetro y retorna una lista si se encuentra o None si no lo hace
def buscar_producto_por_categoria_db(categoria)-> list:
    lista_productos = None

    try:
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        query = "SELECT * FROM productos WHERE Categoria = ?"
        placeholders = (categoria, )
        cursor.execute(query, placeholders)
        filas = cursor.fetchall()
        columnas = [description[0] for description in cursor.description]
        lista_productos = [filas, columnas]
    except sqlite3.Error as error:
        print(f"Categoría no encontrada: {error}")
    finally:
        conexion.close()

    return lista_productos

# Función que busca los productos de la tabla según sea menor o igual a una cantidad recibida por parámetro. Retorna una lista si se encuentra o None si no lo hace
def buscar_producto_por_baja_cantidad_db(cantidad)-> list:
    lista_productos = None

    try:
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        query = "SELECT * FROM productos WHERE Cantidad <= ?"
        placeholders = (cantidad, )
        cursor.execute(query, placeholders)
        filas = cursor.fetchall()
        columnas = [description[0] for description in cursor.description]
        lista_productos = [filas, columnas]
    except sqlite3.Error as error:
        print(f"Productos no encontrados: {error}")
    finally:
        conexion.close()

    return lista_productos

# Función que busca los nombres guardados en la base de datos y las retorna en una lista
def mostrar_nombres_db()-> list:
    nombres = None

    try:
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        query = "SELECT Nombre FROM productos"
        cursor.execute(query)
        nombres = cursor.fetchall()
    except sqlite3.Error as error:
        print(f"Productos no encontrados: {error}")
    finally:
        conexion.close()

    return nombres

# Función que busca las categorías guardadas en la base de datos y las retorna en una lista
def mostrar_categorias_db()-> list:
    categorias = None

    try:
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()
        query = "SELECT Categoria FROM productos"
        cursor.execute(query)
        categorias = cursor.fetchall()
    except sqlite3.Error as error:
        print(f"Productos no encontrados: {error}")
    finally:
        conexion.close()

    return categorias