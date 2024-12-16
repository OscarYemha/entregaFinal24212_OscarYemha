from funciones.funciones_database import *
from tabulate import tabulate
from colorama import *
import os

sistema_operativo_utilizado = os.name
cadena_limpiar_consola = ""
if sistema_operativo_utilizado == "nt":
    cadena_limpiar_consola = "cls"
else:
    cadena_limpiar_consola = "clear"


init()

def mostrar_menu_opciones() -> str:

    
    print(Fore.CYAN + "-" * 40)
    print("Menú Principal")
    print("-" * 40)
    print(Fore.RESET + "1. Agregar producto\n2. Mostrar productos\n3. Actualizar cantidad de producto\n4. Eliminar producto\n5. Buscar producto\n6. Reporte de bajo stock\n7. Salir\n")
    opcion_seleccionada = input("Seleccione una opción: ")
    os.system(cadena_limpiar_consola)

    return opcion_seleccionada

def agregar_producto_menu():
    producto_cargado = False

    print(Fore.CYAN + "Ingrese los siguientes datos del producto: ")
    nombre = input(Fore.RESET + "Ingrese el nombre del producto: ").capitalize()
    descripcion = input("Ingrese la descripcion del producto: ").capitalize()
    categoria = input("Ingrese la categoria del producto: ").capitalize()
    cantidad = input("Ingrese la cantidad del producto: ")
    precio = input("Ingrese el precio del producto: ")

    producto = {
        "Nombre": nombre,
        "Descripcion": descripcion,
        "Categoria": categoria,
        "Cantidad": cantidad,
        "Precio": precio
    }

    producto_cargado = insertar_producto_dt(producto)

    if producto_cargado:
        input(Back.RED + Fore.BLACK + Style.BRIGHT + "Producto cargado exitosamente. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)
    else:
        input(Back.RED + Fore.BLACK + Style.BRIGHT + "El producto no pudo ser cargado. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)

def mostrar_productos_menu(opcion_seleccionada)-> None|str:
    lista_productos = obtener_productos_db()

    valor_retornado = None
    
    if lista_productos[0]:
        print(tabulate(lista_productos[0], headers = lista_productos[1], tablefmt="fancy_grid"), "\n")
        if opcion_seleccionada == "2":
            input("Presione Enter para volver al menú... ")
        elif opcion_seleccionada == "3":
            valor_retornado = input("Ingrese el Id del producto a actualizar la cantidad: ")
        elif opcion_seleccionada == "4":
            valor_retornado = input("Ingrese el Id del producto a eliminar: ")
    else:
        input("Aún no se han cargado productos. Presione Enter para continuar... ")

    return valor_retornado

def eliminar_producto_menu(opcion_seleccionada):
    producto_encontrado = False
    producto_eliminado = False

    id = mostrar_productos_menu(opcion_seleccionada)

    producto_encontrado = buscar_producto_por_id_db(id)
    
    if producto_encontrado:
        opcion_eliminar = input("¿Está seguro de eliminar el producto seleccionado? S/N ").lower()
        if opcion_eliminar == "s":
            producto_eliminado = eliminar_producto_db(id)
            
    if producto_eliminado:
        input(Back.RED + Fore.BLACK + Style.BRIGHT + f"El producto({producto_encontrado[1]}) fue eliminado. Presione Enter para volver continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)
    else:
        input(Back.RED + Fore.BLACK + Style.BRIGHT + f"El producto no pudo ser eliminado. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)   

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
        input(Back.RED + Fore.BLACK + Style.BRIGHT + f"La cantidad del producto ({producto_encontrado[1]}) fue actualizada. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)
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
            input("\nPresione Enter para continuar... ")
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
            input("\nPresione Enter para continuar... ")
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
            input("\nPresione Enter para continuar... ")
        else:
            input(Back.RED + Fore.BLACK + Style.BRIGHT + f"El producto no pudo ser encontrado. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)
    else:
        input(Back.RED + Fore.BLACK + Style.BRIGHT + "Opción no válida. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)

def buscar_producto_por_baja_cantidad_menu():
    cantidad_indicada = int(input("Buscar productos con un stock menor o igual a: "))
    productos_obtenidos = buscar_producto_por_baja_cantidad_db(cantidad_indicada)
   
    if productos_obtenidos[0]:
        os.system(cadena_limpiar_consola)
        print("Se encontró lo siguiente: ")
        print(tabulate(productos_obtenidos[0], headers = productos_obtenidos[1], tablefmt="fancy_grid"), "\n")
        input("Presione Enter para volver al menú... ")
    else:
        input(Back.RED + Fore.BLACK + Style.BRIGHT + f"No se han encontrado productos con un stock menor o igual a {cantidad_indicada}. Presione Enter para continuar... " + Back.RESET + Fore.RESET + Style.RESET_ALL)