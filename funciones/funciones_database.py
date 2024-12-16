import sqlite3

ruta_db = "entregaFinal_OscarYemha/inventario.db"

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

def buscar_producto_por_id_db(id)-> tuple:
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

def buscar_producto_por_nombre_db(nombre)-> tuple:
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

def buscar_producto_por_categoria_db(categoria)-> tuple:
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

def buscar_producto_por_baja_cantidad_db(cantidad)-> tuple:
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