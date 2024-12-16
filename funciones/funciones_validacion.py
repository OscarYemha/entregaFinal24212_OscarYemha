# Valida que la cadena de caracteres ingresada sea sólo caracteres y una sola palabra para luego retornarla
def validar_cadena(cadena_recibida: str, mensaje_error: str)-> str:
    cadena_retornada = cadena_recibida

    while cadena_retornada.isalpha() == False:
        cadena_retornada = input(mensaje_error)
    
    return cadena_retornada

# Se valida que el número ingresado sea un número y luego se retorna un número entero
def validar_numero_entero(numero_recibido: str, mensaje_error: str, minimo: int)-> int:
    numero_retornado = numero_recibido

    while numero_retornado.isdigit() == False or int(numero_retornado) < minimo:
        numero_retornado = input(mensaje_error)

    numero_retornado = int(numero_retornado)

    return numero_retornado

# Se valida que el número ingresado sea un número decimal y se retorna un número decimal
def validar_numero_flotante(numero_recibido: str, mensaje_error: str, minimo: float)-> float:
    numero_retornado = numero_recibido

    while True:
        try:
            if float(numero_retornado) >= minimo:
                numero_retornado = float(numero_retornado)
                break
            else:
                numero_retornado = input(mensaje_error)
        except ValueError:
            numero_retornado = input(mensaje_error)

    return numero_retornado