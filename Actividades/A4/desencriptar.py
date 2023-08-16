from typing import List
import json
from errors import JsonError, SequenceError


def deserializar_diccionario(mensaje_codificado: bytearray) -> dict:
    # Completar
    try:
        string = mensaje_codificado.decode("utf-8")
        diccionario = json.loads(string)
    except json.JSONDecodeError:
        raise JsonError
    return diccionario


def decodificar_largo(mensaje: bytearray) -> int:
    # Completar
    largo = int.from_bytes(mensaje[0:4], byteorder = "big")
    return largo


def separar_msg_encriptado(mensaje: bytearray) -> List[bytearray]:
    m_bytes_secuencia = bytearray()
    m_reducido = bytearray()
    secuencia_codificada = bytearray()
    # Completar
    largo = decodificar_largo(mensaje)
    m_bytes_secuencia = mensaje[largo:largo*2]
    string_json = json.dumps(m_bytes_secuencia)
    bytes_json = string_json.encode()
    secuencia_codificada = bytes_json
    m_reducido = mensaje[:-4]
    return [m_bytes_secuencia, m_reducido, secuencia_codificada]


def decodificar_secuencia(secuencia_codificada: bytearray) -> List[int]:
    # Completar
    secuencia = []
    for i in range(len(secuencia_codificada)//2):
        c = int.from_bytes(secuencia_codificada[i*2:(2*i)+1], byteorder = "big")
        secuencia.append(c)
    return secuencia


def desencriptar(mensaje: bytearray) -> bytearray:
    # Completar
    pass


if __name__ == "__main__":
    mensaje = bytearray(b'\x00\x00\x00\x04"a}a{tm": 1\x00\x01\x00\x05\x00\n\x00\x03')
    desencriptado = desencriptar(mensaje)
    diccionario = deserializar_diccionario(desencriptado)
    print(diccionario)
