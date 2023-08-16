from functions import parametro_json


def encriptar(msg: bytearray, ID=None) -> bytearray:
    mensaje_encriptado = bytearray(msg[:])
    N = parametro_json("N_PONDERADOR")
    espacios = parametro_json("N_PONDERADOR")
    for i in range(espacios):
        ultimo = mensaje_encriptado.pop()
        mensaje_encriptado.insert(0, ultimo)
    primero = mensaje_encriptado[0]
    posicion_n = mensaje_encriptado[N]
    mensaje_encriptado[0] = posicion_n
    mensaje_encriptado[N] = primero
    return mensaje_encriptado


def desencriptar(msg: bytearray, ID=None):
    mensaje_desencriptado = bytearray(msg[:])
    N = parametro_json("N_PONDERADOR")
    primero = mensaje_desencriptado[0]
    posicion_n = mensaje_desencriptado[N]
    mensaje_desencriptado[0] = posicion_n
    mensaje_desencriptado[N] = primero
    espacios = parametro_json("N_PONDERADOR")
    for i in range(espacios):
        primero = mensaje_desencriptado.pop(0)
        mensaje_desencriptado.append(primero)
    return mensaje_desencriptado
