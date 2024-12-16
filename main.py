from funciones.funciones_database import *
from funciones.funciones_menu import *
import os

def main():

    crear_tabla_productos_dt()

    sistema_operativo_utilizado = os.name

    cadena_limpiar_consola = ""
    if sistema_operativo_utilizado == "nt":
        cadena_limpiar_consola = "cls"
    else:
        cadena_limpiar_consola = "clear"

    mostrar_menu = True

    
    while mostrar_menu:
        os.system(cadena_limpiar_consola)
        
        opcion_seleccionada = mostrar_menu_opciones()

        if opcion_seleccionada == "1":
            agregar_producto_menu()
        elif opcion_seleccionada == "2":
            mostrar_productos_menu(opcion_seleccionada)
        elif opcion_seleccionada == "3":
            actualizar_cantidad_producto_menu(opcion_seleccionada)
        elif opcion_seleccionada == "4":
            eliminar_producto_menu(opcion_seleccionada)
        elif opcion_seleccionada == "5":
            buscar_producto_menu()
        elif opcion_seleccionada == "6":
            buscar_producto_por_baja_cantidad_menu()
        elif opcion_seleccionada == "7":
            os.system(cadena_limpiar_consola)
            input("Gracias por utilizar esta aplicación. Presione Enter para finalizar... ")
            mostrar_menu = False
        else:
            input("Opción incorrecta. Presione Enter para volver al menu... ")

    os.system(cadena_limpiar_consola)

main()            