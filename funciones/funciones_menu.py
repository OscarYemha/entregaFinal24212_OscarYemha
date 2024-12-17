from funciones.funciones_database import *
from funciones.funciones_validacion import *
from tabulate import tabulate
from colorama import *
import os


# Función que verifica el sistema operativo para limpiar la consola y generar una mejor experiencia visual al usuario
def limpiar_consola():
    sistema_operativo_utilizado = os.name
    cadena_limpiar_consola = ""
    if sistema_operativo_utilizado == "nt":
        cadena_limpiar_consola = "cls"
    else:
        cadena_limpiar_consola = "clear"

    os.system(cadena_limpiar_consola)

def verificar_productos_cargados_en_db_menu()-> bool:
    productos_cargados_db = False

    lista_productos = obtener_productos_db()
    if lista_productos[0]:
        productos_cargados_db = True

    return productos_cargados_db


init() # Se inicia colorama

# Función que muestra el menú de opciones y retorna la opción ingresada
def mostrar_menu_opciones()-> str:

    
    print(Fore.CYAN + "-" * 40)
    print("Menú Principal")
    print("-" * 40)
    print(Fore.RESET + "1. Agregar producto\n2. Mostrar productos\n3. Actualizar cantidad de producto\n4. Eliminar producto\n5. Buscar producto\n6. Reporte de bajo stock\n7. Salir\n")
    opcion_seleccionada = input("Seleccione una opción: ")
    limpiar_consola()

    return opcion_seleccionada

# Función que agrega un producto a la base de datos. Recibe la cantidad mínima y el precio mínimo por parámetros para el producto a agregar
def agregar_producto_menu(minima_cantidad: int, minimo_precio: float):
    producto_cargado = False

    # Se piden los datos y se validan los mismos
    print(Fore.CYAN + "Ingrese los siguientes datos del producto: \n")
    nombre = validar_cadena(input(Fore.RESET + "Ingrese el nombre del producto: ").capitalize(), "Error. Ingrese el nombre del producto: ")
    descripcion = input("Ingrese la descripcion del producto: ").capitalize()
    categoria = validar_cadena(input("Ingrese la categoria del producto: ").capitalize(), "Error. Ingrese la categoría del producto: ")
    cantidad = validar_numero_entero(input("Ingrese la cantidad del producto: "), "Error. Ingrese la cantidad del producto: ", minima_cantidad)
    precio = validar_numero_flotante(input("Ingrese el precio del producto: "), "Error. Ingrese el precio del producto: ", minimo_precio)

    # Se crea un objeto "producto" con los datos ingresados
    producto = {
        "Nombre": nombre,
        "Descripcion": descripcion,
        "Categoria": categoria,
        "Cantidad": cantidad,
        "Precio": precio
    }

    # Se carga el producto a la base de datos
    producto_cargado = insertar_producto_dt(producto)

    # Se informa si el producto fue cargado o no y se pregunta si se quiere cargar nuevamente
    if producto_cargado:
        limpiar_consola()
        print(Fore.CYAN + Style.BRIGHT + "Producto cargado exitosamente " +  Fore.RESET + Style.RESET_ALL)
    else:
        limpiar_consola()
        print(Back.RED + Fore.WHITE + Style.BRIGHT + "El producto no pudo ser cargado " + Back.RESET + Fore.RESET + Style.RESET_ALL)
        
    # Se pregunta si se quiere cargar otro producto
    opcion_seguir_cargando_producto = input("\n¿Desea cargar otro producto? S/N: ")
    if opcion_seguir_cargando_producto == "s":
        limpiar_consola()
        agregar_producto_menu()

# Función que muestra los productos cargados en la base de datos. Si no hay productos cargados aún, se informa tal situación
# Recibe la opción seleccionada en el menú por parámetro
# Según la opción recibida, puede devolver una cadena o puede no retornar nada
def mostrar_productos_menu(opcion_seleccionada: str)-> None|str:
    lista_productos = obtener_productos_db()

    valor_retornado = None
    
    if verificar_productos_cargados_en_db_menu(): # Se muestran los productos
        print(tabulate(lista_productos[0], headers = lista_productos[1], tablefmt="fancy_grid"), "\n")
        if opcion_seleccionada == "2": # Si la opción seleccionada antes en el menú es 2, se vuelve al menú
            input("Presione Enter para volver al menú... ")
        elif opcion_seleccionada == "3": # Si la opción seleccionada antes en el menú es 3, se prosigue con la actualización de la cantidad de un producto
            valor_retornado = input("Ingrese el Id del producto a actualizar la cantidad: ")
        elif opcion_seleccionada == "4": # Si la opción seleccionada antes en el menú es 4, se prosigue con la eliminación de un producto
            valor_retornado = input("Ingrese el Id del producto a eliminar: ")
    else:
        input(Back.RED + Fore.WHITE + Style.BRIGHT + "Aún no se han cargado productos. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)

    return valor_retornado

# Función que elimina un producto. Recibe la opción seleccionada en el menú por parámetro
def eliminar_producto_menu(opcion_seleccionada: str):
    # Se inicializan variables para luego saber si se ha encontrado y eliminado el producto
    producto_encontrado = False
    producto_eliminado = False

    if verificar_productos_cargados_en_db_menu():
    # Se muestran los productos cargados y se pide el Id del producto a eliminar
        id = mostrar_productos_menu(opcion_seleccionada)

        # Se busca el producto por el Id ingresado
        producto_encontrado = buscar_producto_por_id_db(id)
        
        # Si el producto se encuentra, se pregunta si se quiere eliminar o no.
        if producto_encontrado:
            opcion_eliminar = input("\n¿Está seguro de eliminar el producto seleccionado? S/N ").lower()
            if opcion_eliminar == "s":
                producto_eliminado = eliminar_producto_db(id)

        # Se informa si se eliminó o no el producto y se pregunta si se quiere seguir eliminando        
        if producto_eliminado:
            print(Fore.CYAN + Style.BRIGHT + f"\nEl producto({producto_encontrado[1]}) fue eliminado " + Fore.RESET + Style.RESET_ALL)
        else:
            print(Back.RED + Fore.BLACK + Style.BRIGHT + f"\nEl producto no pudo ser eliminado " + Back.RESET + Fore.RESET + Style.RESET_ALL)

        # Se pregunta si se quiere eliminar otro producto
        opcion_seguir_eliminando_producto = input("\n¿Desea eliminar otro producto? S/N: ")
        if opcion_seguir_eliminando_producto == "s":
            limpiar_consola()
            eliminar_producto_menu(opcion_seleccionada)
    else:
        input(Back.RED + Fore.WHITE + Style.BRIGHT + "Aún no se han cargado productos. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)

# Función que actualiza la cantidad de un producto. Recibe la opción seleccionada en el menú por parámetro y la cantidad mínima que puede tener el producto
def actualizar_cantidad_producto_menu(opcion_seleccionada: str, minimo: int):
    # Se inicializan variables para luego saber si se ha encontrado y actualizado el producto
    producto_encontrado = False
    producto_actualizado = False
    
    if verificar_productos_cargados_en_db_menu():
    # Se muestran los productos cargados y se pide el Id del producto a actualizar
        id = mostrar_productos_menu(opcion_seleccionada)

        # Se busca el producto por el Id ingresado
        producto_encontrado = buscar_producto_por_id_db(id)

        # Si el producto se encuentra, se pregunta si se quiere actualizar o no.
        if producto_encontrado:
            limpiar_consola()
            opcion_actualizar_cantidad = input(Back.RED + Fore.WHITE + Style.BRIGHT + "¿Está seguro que quiere modificar la cantidad del producto seleccionado? S/N " + Back.RESET + Fore.RESET + Style.RESET_ALL).lower()
            if opcion_actualizar_cantidad == "s":
                limpiar_consola()
                cantidad_nueva = validar_numero_entero(input(f"{producto_encontrado[1]} --> Cantidad actual: {producto_encontrado[4]}\nIngrese la nueva cantidad: "), "Error. Ingrese la cantidad del producto: ", minimo)
                producto_actualizado = actualizar_cantidad_producto_db(id, cantidad_nueva)

        # Se informa si se eliminó o no el producto y se pregunta si se quiere seguir actualizando
        if producto_actualizado:
            limpiar_consola()
            print(Fore.CYAN + Style.BRIGHT + f"\nLa cantidad del producto ({producto_encontrado[1]}) fue actualizada " + Fore.RESET + Style.RESET_ALL)
        else:
            limpiar_consola()
            print(Back.RED + Fore.WHITE + Style.BRIGHT + f"\nEl producto no pudo ser encontrado " + Back.RESET + Fore.RESET + Style.RESET_ALL)

        # Se pregunta si se quiere actualizar la cantidad de otro producto
        opcion_seguir_actualizando_cantidad = input("\n¿Desea modificar la cantidad de otro producto? S/N:  ")
        if opcion_seguir_actualizando_cantidad == "s":
            limpiar_consola()
            actualizar_cantidad_producto_menu(opcion_seleccionada, minimo)
    else:
        input(Back.RED + Fore.WHITE + Style.BRIGHT + "Aún no se han cargado productos. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)

# Función que busca un producto por Id, Nombre o Categoría
def buscar_producto_menu():
    
    if verificar_productos_cargados_en_db_menu():
        opcion_elegida = input("Para buscar por Id ingrese 1.\nPara buscar por Nombre ingrese 2.\nPara buscar por Categoría ingrese 3.\n\nIngrese la opción: ")

        # Se inicializa una variable donde luego se guardarán los productos obtenidos si se los encuentra
        productos_obtenidos = None
        limpiar_consola()

        # De acuerdo a la opción seleccionada, se busca por Id, Nombre o Categoría
        if opcion_elegida == "1":
            id = int(input("Ingrese el Id a buscar: "))
            productos_obtenidos = buscar_producto_por_id_db(id)

            # Si se encuentran productos, se muestran en una tabla
            if productos_obtenidos:
                limpiar_consola()
                print("Se encontró lo siguiente: ")
                encabezados = ["Id", "Nombre", "Descripción", "Categoría", "Cantidad", "Precio"]
                print(tabulate([productos_obtenidos], headers = encabezados, tablefmt = 'fancy_grid'))
            else:
                limpiar_consola()
                print(Back.RED + Fore.WHITE + Style.BRIGHT + f"\nEl producto con Id = {id} no pudo ser encontrado" + Back.RESET + Fore.RESET + Style.RESET_ALL)
        elif opcion_elegida == "2":
            nombre = input("Ingrese el nombre a buscar: ").capitalize()
            productos_obtenidos = buscar_producto_por_nombre_db(nombre)

            if productos_obtenidos[0]:
                limpiar_consola()
                print("Se encontró lo siguiente: ")
                print(tabulate(productos_obtenidos[0], headers = productos_obtenidos[1], tablefmt="fancy_grid"))
            else:
                limpiar_consola()
                print(Back.RED + Fore.WHITE + Style.BRIGHT + f"\nEl producto con nombre = {nombre} no pudo ser encontrado" + Back.RESET + Fore.RESET + Style.RESET_ALL)
        elif opcion_elegida == "3":
            # Se muestran las categorías guardadas para que el usuario busque por las categorías guardadas
            lista_categorias = mostrar_categorias_db()
            lista_categorias_sin_duplicados = list(set(lista_categorias))
            print(tabulate(lista_categorias_sin_duplicados, headers = [Style.BRIGHT + "CATEGORÍAS" + Style.RESET_ALL], tablefmt = "fancy_grid"))

            categoria = input("\nIngrese la categoría a buscar: ").capitalize()
            productos_obtenidos = buscar_producto_por_categoria_db(categoria)
            
            if productos_obtenidos[0]:
                limpiar_consola()
                print("Se encontró lo siguiente: ")
                print(tabulate(productos_obtenidos[0], headers = productos_obtenidos[1], tablefmt="fancy_grid"))
            else:
                limpiar_consola()
                print(Back.RED + Fore.WHITE + Style.BRIGHT + f"\nEl producto con categoría = {categoria} no pudo ser encontrado" + Back.RESET + Fore.RESET + Style.RESET_ALL)
                
        else:
            print(Back.RED + Fore.WHITE + Style.BRIGHT + "Opción no válida" + Back.RESET + Fore.RESET + Style.RESET_ALL)

        # Se pregunta si se quiere volver a buscar
        opcion_seguir_buscando = input("\n¿Desea volver a buscar otro producto? S/N: ").lower()
        if opcion_seguir_buscando == "s":
            limpiar_consola()
            buscar_producto_menu()
    else:
        input(Back.RED + Fore.WHITE + Style.BRIGHT + "Aún no se han cargado productos. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)

# Función que busca los productos que tienen un stock menor o igual al ingresado por el usuario
def buscar_producto_por_baja_cantidad_menu():

    if verificar_productos_cargados_en_db_menu():
        # Se pide el stock a buscar
        cantidad_indicada = int(input("Buscar productos con un stock menor o igual a: "))
        productos_obtenidos = buscar_producto_por_baja_cantidad_db(cantidad_indicada)
    
        # Si hay productos con un stock igual o menor al ingresado, se muestran. Si no hay, se informa tal situación.
        if productos_obtenidos[0]:
            limpiar_consola()
            print(f"Se encontró lo siguiente con un stock menor o igual a {cantidad_indicada}: ")
            print(tabulate(productos_obtenidos[0], headers = productos_obtenidos[1], tablefmt="fancy_grid"), "\n") 
        else:
            print(Back.RED + Fore.WHITE + Style.BRIGHT + f"No se han encontrado productos con un stock menor o igual a {cantidad_indicada}" + Back.RESET + Fore.RESET + Style.RESET_ALL)
        
        # Se pregunta si se quiere seguir buscando
        opcion_seguir_buscando = input("\n¿Desea volver a buscar? S/N: ")
        if opcion_seguir_buscando == "s":
            limpiar_consola()
            buscar_producto_por_baja_cantidad_menu()
    else:
        input(Back.RED + Fore.WHITE + Style.BRIGHT + "Aún no se han cargado productos. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)


##################### SEGUIR MODIFICANDO ELIMINAR PARA LIMPIAR CONSOLA, AGREGAR ESTILO ####################