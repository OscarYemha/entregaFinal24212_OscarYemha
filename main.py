from funciones.funciones_database import *
from funciones.funciones_menu import *
from colorama import *

# Se declara como constantes la cantidad mínima y el precio mínimo
CANTIDAD_MINIMA = 1
PRECIO_MINIMO = 0.01

# Se inicia colorama.
init()

# Función principal de la aplicación main()
def main():

    mostrar_menu = True

    crear_tabla_productos_dt() # Se crea la tabla si no existe
    
    while mostrar_menu:
        limpiar_consola_menu()
        
        # Se muestra el menú y la función regresa la opción ingresada
        opcion_seleccionada = mostrar_menu_opciones()
        # Se llama a las diferentes funciones según la opción ingresada
        if opcion_seleccionada == "1":
            agregar_producto_menu(CANTIDAD_MINIMA, PRECIO_MINIMO)
        elif opcion_seleccionada == "2":
            mostrar_productos_menu(opcion_seleccionada)
        elif opcion_seleccionada == "3":
            actualizar_cantidad_producto_menu(opcion_seleccionada, CANTIDAD_MINIMA)
        elif opcion_seleccionada == "4":
            eliminar_producto_menu(opcion_seleccionada)
        elif opcion_seleccionada == "5":
            buscar_producto_menu()
        elif opcion_seleccionada == "6":
            buscar_producto_por_baja_cantidad_menu()
        elif opcion_seleccionada == "7":
            limpiar_consola_menu()
            mostrar_menu = False
            input(Fore.CYAN + Style.BRIGHT + "Gracias por utilizar esta aplicación. Presione Enter para finalizar... " + Fore.RESET + Style.RESET_ALL)
        else:
            input(Back.RED + Fore.WHITE + Style.BRIGHT + "Opción incorrecta. Presione Enter para volver al menu... " + Back.RESET + Fore.RESET + Style.RESET_ALL)

    limpiar_consola_menu()

main()            