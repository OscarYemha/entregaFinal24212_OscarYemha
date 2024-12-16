from funciones.funciones_database import *
from funciones.funciones_validacion import *
from tabulate import tabulate
from colorama import *
import os

# Verificamos sistema operativo para limpiar consola y generar una mejor experiencia visual al usuario
sistema_operativo_utilizado = os.name
cadena_limpiar_consola = ""
if sistema_operativo_utilizado == "nt":
    cadena_limpiar_consola = "cls"
else:
    cadena_limpiar_consola = "clear"


init() # Se inicia colorama

# Función que muestra el menú de opciones y retorna la opción ingresada
def mostrar_menu_opciones()-> str:

    
    print(Fore.CYAN + "-" * 40)
    print("Menú Principal")
    print("-" * 40)
    print(Fore.RESET + "1. Agregar producto\n2. Mostrar productos\n3. Actualizar cantidad de producto\n4. Eliminar producto\n5. Buscar producto\n6. Reporte de bajo stock\n7. Salir\n")
    opcion_seleccionada = input("Seleccione una opción: ")
    os.system(cadena_limpiar_consola)

    return opcion_seleccionada

# Función que agrega un producto a la base de datos.
def agregar_producto_menu():
    producto_cargado = False

    # Se piden los datos y se validan los mismos
    print(Fore.CYAN + "Ingrese los siguientes datos del producto: ")
    nombre = validar_cadena(input(Fore.RESET + "Ingrese el nombre del producto: ").capitalize(), "Error. Ingrese el nombre del producto: ")
    descripcion = input("Ingrese la descripcion del producto: ").capitalize()
    categoria = validar_cadena(input("Ingrese la categoria del producto: ").capitalize(), "Error. Ingrese la categoría del producto: ")
    cantidad = validar_numero_entero(input("Ingrese la cantidad del producto: "), "Error. Ingrese la cantidad del producto: ")
    precio = validar_numero_flotante(input("Ingrese el precio del producto: "), "Error. Ingrese el precio del producto: ")

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
        opcion_seguir_cargando_producto = input(Back.RED + Fore.BLACK + Style.BRIGHT + "Producto cargado exitosamente. ¿Desea cargar otro producto? S/N: " + Back.RESET + Fore.RESET + Style.RESET_ALL).lower()
        if opcion_seguir_cargando_producto == "s":
            os.system(cadena_limpiar_consola)
            agregar_producto_menu()
    else:
        opcion_seguir_cargando_producto = input(Back.RED + Fore.BLACK + Style.BRIGHT + "El producto no pudo ser cargado. ¿Desea cargar otro producto? S/N: " + Back.RESET + Fore.RESET + Style.RESET_ALL)
        if opcion_seguir_cargando_producto == "s":
            os.system(cadena_limpiar_consola)
            agregar_producto_menu()

# Función que muestra los productos cargados en la base de datos.
# Si no hay productos cargados aún, se informa tal situación
def mostrar_productos_menu(opcion_seleccionada)-> None|str:
    lista_productos = obtener_productos_db()

    valor_retornado = None
    
    if lista_productos[0]: # Se muestran los productos
        print(tabulate(lista_productos[0], headers = lista_productos[1], tablefmt="fancy_grid"), "\n")
        if opcion_seleccionada == "2": # Si la opción seleccionada antes en el menú es 2, se vuelve al menú
            input("Presione Enter para volver al menú... ")
        elif opcion_seleccionada == "3": # Si la opción seleccionada antes en el menú es 3, se prosigue con la actualización de la cantidad de un producto
            valor_retornado = input("Ingrese el Id del producto a actualizar la cantidad: ")
        elif opcion_seleccionada == "4": # Si la opción seleccionada antes en el menú es 4, se prosigue con la eliminación de un producto
            valor_retornado = input("Ingrese el Id del producto a eliminar: ")
    else:
        input("Aún no se han cargado productos. Presione Enter para continuar... ")

    return valor_retornado

# Función que elimina un producto
def eliminar_producto_menu(opcion_seleccionada):
    producto_encontrado = False
    producto_eliminado = False

    # Se muestran los productos cargados y se pide el Id del producto a eliminar
    id = mostrar_productos_menu(opcion_seleccionada)

    # Se busca el producto por el Id ingresado
    producto_encontrado = buscar_producto_por_id_db(id)
    
    # Si el producto se encuentra, se pregunta si se quiere eliminar o no.
    if producto_encontrado:
        opcion_eliminar = input("¿Está seguro de eliminar el producto seleccionado? S/N ").lower()
        if opcion_eliminar == "s":
            producto_eliminado = eliminar_producto_db(id)

    # Se informa si se eliminó o no el producto y se pregunta si se quiere seguir eliminando        
    if producto_eliminado:
        opcion_seguir_eliminando_producto = input(Back.RED + Fore.BLACK + Style.BRIGHT + f"El producto({producto_encontrado[1]}) fue eliminado. ¿Desea eliminar otro producto? S/N: " + Back.RESET + Fore.RESET + Style.RESET_ALL).lower()
        if opcion_seguir_eliminando_producto == "s":
            os.system(cadena_limpiar_consola)
            eliminar_producto_menu(opcion_seleccionada)
    else:
        opcion_seguir_eliminando_producto = input(Back.RED + Fore.BLACK + Style.BRIGHT + f"El producto no pudo ser eliminado. ¿Desea eliminar otro producto? S/N: " + Back.RESET + Fore.RESET + Style.RESET_ALL)
        if opcion_seguir_eliminando_producto == "s":
            os.system(cadena_limpiar_consola)
            eliminar_producto_menu(opcion_seleccionada)

def actualizar_cantidad_producto_menu(opcion_seleccionada):
    producto_encontrado = False
    producto_actualizado = False
    
    id = mostrar_productos_menu(opcion_seleccionada)

    producto_encontrado = buscar_producto_por_id_db(id)

    if producto_encontrado:
        opcion_actualizar = input("¿Está seguro de querer modificar la cantidad del producto seleccionado? S/N ").lower()
        if opcion_actualizar == "s":
            os.system(cadena_limpiar_consola)
            cantidad_nueva = int(input(f"{producto_encontrado[1]} --> Cantidad actual: {producto_encontrado[4]}\nIngrese la nueva cantidad: "))
            producto_actualizado = actualizar_cantidad_producto_db(id, cantidad_nueva)

    if producto_actualizado:
        opcion_seguir_actualizando_cantidad = input(Back.RED + Fore.BLACK + Style.BRIGHT + f"La cantidad del producto ({producto_encontrado[1]}) fue actualizada. ¿Desea modificar la cantidad de otro producto? S/N:  " + Back.RESET + Fore.RESET + Style.RESET_ALL).lower()
        if opcion_seguir_actualizando_cantidad == "s":
            os.system(cadena_limpiar_consola)
            actualizar_cantidad_producto_menu(opcion_seleccionada)
    else:
        input(Back.RED + Fore.BLACK + Style.BRIGHT + f"El producto no pudo ser encontrado. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)


def buscar_producto_menu():
    opcion_elegida = input("Para buscar por Id ingrese 1.\nPara buscar por Nombre ingrese 2.\nPara buscar por Categoría ingrese 3.\nIngrese la opción: ")

    productos_obtenidos = None
    os.system(cadena_limpiar_consola)

    if opcion_elegida == "1":
        id = int(input("Ingrese el Id a buscar: "))
        productos_obtenidos = buscar_producto_por_id_db(id)

        if productos_obtenidos:
            os.system(cadena_limpiar_consola)
            encabezados = ["Id", "Nombre", "Descripción", "Categoría", "Cantidad", "Precio"]
            print("Se encontró el siguiente producto: ")
            print(tabulate([productos_obtenidos], headers=encabezados, tablefmt='fancy_grid'))
        else:
            input(Back.RED + Fore.BLACK + Style.BRIGHT + f"El producto no pudo ser encontrado. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)
    elif opcion_elegida == "2":
        nombre = input("Ingrese el nombre a buscar: ").capitalize()
        productos_obtenidos = buscar_producto_por_nombre_db(nombre)

        if productos_obtenidos:
            os.system(cadena_limpiar_consola)
            encabezados = ["Id", "Nombre", "Descripción", "Categoría", "Cantidad", "Precio"]
            print("Se encontró el siguiente producto: ")
            print(tabulate(productos_obtenidos[0], headers = productos_obtenidos[1], tablefmt="fancy_grid"))
        else:
            input(Back.RED + Fore.BLACK + Style.BRIGHT + f"El producto no pudo ser encontrado. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)
    elif opcion_elegida == "3":
        categoria = input("Ingrese la categoría a buscar: ").capitalize()
        productos_obtenidos = buscar_producto_por_categoria_db(categoria)
        
        if productos_obtenidos:
            os.system(cadena_limpiar_consola)
            encabezados = ["Id", "Nombre", "Descripción", "Categoría", "Cantidad", "Precio"]
            print("Se encontró el siguiente producto: ")
            print(tabulate(productos_obtenidos[0], headers = productos_obtenidos[1], tablefmt="fancy_grid"))
        else:
            input(Back.RED + Fore.BLACK + Style.BRIGHT + f"El producto no pudo ser encontrado. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)
    else:
        input(Back.RED + Fore.BLACK + Style.BRIGHT + "Opción no válida. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)


    opcion_seguir_buscando = input("\n¿Desea buscar otro producto? S/N: ").lower()

    if opcion_seguir_buscando == "s":
        os.system(cadena_limpiar_consola)
        buscar_producto_menu()

def buscar_producto_por_baja_cantidad_menu():
    cantidad_indicada = int(input("Buscar productos con un stock menor o igual a: "))
    productos_obtenidos = buscar_producto_por_baja_cantidad_db(cantidad_indicada)
   
    if productos_obtenidos[0]:
        os.system(cadena_limpiar_consola)
        print(f"Se encontró lo siguiente con un stock menor o igual a {cantidad_indicada}: ")
        print(tabulate(productos_obtenidos[0], headers = productos_obtenidos[1], tablefmt="fancy_grid"), "\n")
        input("Presione Enter para volver al menú... ")
    else:
        input(Back.RED + Fore.BLACK + Style.BRIGHT + f"No se han encontrado productos con un stock menor o igual a {cantidad_indicada}. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)