from funciones.funciones_database import *

# Valida que la cadena de caracteres ingresada sea sólo de letras. Una vez que así sea, se retorna la cadena.
def validar_cadena(cadena_recibida: str, mensaje_error: str)-> str:
    cadena_retornada = cadena_recibida.split()

    while all(palabra.isalpha() == False for palabra in cadena_retornada):
        cadena_retornada = input(mensaje_error)
    
    cadena_retornada = cadena_recibida

    return cadena_retornada

# Se valida que el número ingresado sea un número y luego se retorna un número entero.
def validar_numero_entero(numero_recibido: str, mensaje_error: str, minimo: int)-> int:
    numero_retornado = numero_recibido

    while numero_retornado.isdigit() == False or int(numero_retornado) < minimo:
        numero_retornado = input(mensaje_error)

    numero_retornado = int(numero_retornado)

    return numero_retornado

# Se valida que el número ingresado sea un número decimal y se retorna un número decimal
def validar_numero_flotante(numero_recibido: str, mensaje_error: str, minimo: float)-> float:
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

# Función que valida si hay productos cargados en la base de datos
def validar_productos_cargados_en_db()-> bool:
    productos_cargados_db = False

    lista_productos = obtener_productos_db()
    if lista_productos[0]:
        productos_cargados_db = True

    return productos_cargados_db