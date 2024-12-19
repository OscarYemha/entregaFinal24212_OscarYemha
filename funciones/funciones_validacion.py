from funciones.funciones_database import *

# Valida que la cadena de caracteres ingresada sea sólo de letras y no esté vacía. En caso contrario, se muestra el mensaje de error. 
# Una vez se cumpla la condición, se retorna la cadena.
def validar_cadena(cadena_recibida: str, mensaje_error: str)-> str:
    cadena_retornada = cadena_recibida.split()

    while all(palabra.isalpha() == False for palabra in cadena_retornada):
        cadena_retornada = input(mensaje_error).split()
    
    cadena_retornada = " ".join(cadena_retornada)

    return cadena_retornada

# Se valida que la cadena ingresada sea sólo de números y evalúa también que ese número sea mayor a cierto mínimo el cual es por defecto 0. Luego se retorna un número entero.
# Mientras no se cumplan las condiciones, se muestra un mensaje de error.
def validar_numero_entero(numero_recibido: str, mensaje_error: str, minimo: int = 0)-> int:
    numero_retornado = numero_recibido

    while numero_retornado.isdigit() == False or int(numero_retornado) < minimo:
        numero_retornado = input(mensaje_error)

    numero_retornado = int(numero_retornado)

    return numero_retornado

# Se valida que la cadena ingresada contenga un número decimal y se evalúa que sea mayor a cierto mínimo el cual es 0 por defecto. 
# Si es así, se retorna un número decimal. En caso contrario, se muestra un mensaje de error.
def validar_numero_flotante(numero_recibido: str, mensaje_error: str, minimo: float = 0)-> float:
    numero_retornado = numero_recibido

    while True: # Se usa un bucle que sólo se rompe si el número ingresado es mayor o igual al mínimo y es flotante
        try:
            if float(numero_retornado) >= minimo: 
                numero_retornado = float(numero_retornado)
                break
            else:
                numero_retornado = input(mensaje_error)
        except ValueError:
            numero_retornado = input(mensaje_error)

    return numero_retornado

# Función que valida si hay productos cargados en la base de datos. Si los hay se retorna True y en caso contrario, False.
def validar_productos_cargados_en_db()-> bool:
    productos_cargados_db = False

    lista_productos = obtener_productos_db()
    if lista_productos[0]:
        productos_cargados_db = True

    return productos_cargados_db