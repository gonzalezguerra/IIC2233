import json
from math import ceil


def parametro_json(parametro, nombre_archivo="parametros.json"):
    with open(nombre_archivo, "r") as file:
        diccionario = json.load(file)
    return diccionario[parametro]


def codificar(mensaje: bytearray):
    mensaje = bytearray(mensaje)
    array = bytearray()
    largo = len(mensaje)
    bloques = ceil(largo / 128)
    largo_encriptado = int.to_bytes(largo, 4, "little")
    array.extend(largo_encriptado)
    for i in range(bloques):
        array.extend(int.to_bytes(i, 4, "big"))
        for j in range(128):
            if len(mensaje) > 0:
                array.append(mensaje.pop(0))
            else:
                array.extend(int.to_bytes(0, 1, "little"))
    return array


def decodificar(mensaje: bytearray):
    mensaje = bytearray(mensaje)
    largo_codificado = mensaje[0:4]
    bloques = len(mensaje) // 132
    largo_int = int.from_bytes(largo_codificado, "little")
    datos = mensaje[4:].copy()
    numero_ceros = len(datos) - (bloques * 4) - largo_int
    array_decodificada = bytearray()
    for i in range(bloques):
        for j in range(4):
            datos.pop(0)
        for j in range(128):
            array_decodificada.append(datos.pop(0))
    for n in range(numero_ceros):
        array_decodificada.pop()
    return array_decodificada
