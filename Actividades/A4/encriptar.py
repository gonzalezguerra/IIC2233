from typing import List
import json
from errors import JsonError, SequenceError


def serializar_diccionario(dictionary: dict) -> bytearray:
    # Completar
    try:
        string = json.dumps(dictionary)
        string2 = string.encode("utf-8")
    except TypeError:
        raise JsonError
    return bytearray(string2)


def verificar_secuencia(mensaje: bytearray, secuencia: List[int]) -> None:
    # Completar
    lista = []
    repetidos = False
    for i in secuencia:
        if i in lista:
            repetidos = True
        lista.append(i)

    if max(secuencia) > len(mensaje) or repetidos:
        raise SequenceError


def codificar_secuencia(secuencia: List[int]) -> bytearray:
    retorno = bytearray()
    for i in secuencia:
        byte = i.to_bytes(2, byteorder = "big")
        retorno.append(byte[0])
        retorno.append(byte[1])
    return retorno


def codificar_largo(largo: int) -> bytearray:
    # Completar
    retorno = bytearray()
    byte = largo.to_bytes(4, byteorder = "big")
    retorno.append(byte[0])
    retorno.append(byte[1])
    retorno.append(byte[2])
    retorno.append(byte[3])
    return retorno


def separar_msg(mensaje: bytearray, secuencia: List[int]) -> List[bytearray]:
    m_bytes_secuencia = bytearray()
    m_reducido = bytearray()
    for i in range(len(mensaje)):
        if i not in secuencia:
            m_reducido.append(mensaje[i])
        else:
            m_bytes_secuencia.append(mensaje[i])
    # Completar

    return [m_bytes_secuencia, m_reducido]


def encriptar(mensaje: dict, secuencia: List[int]) -> bytearray:
    verificar_secuencia(mensaje, secuencia)

    m_bytes_secuencia, m_reducido = separar_msg(mensaje, secuencia)
    secuencia_codificada = codificar_secuencia(secuencia)

    return (
        codificar_largo(len(secuencia))
        + m_bytes_secuencia
        + m_reducido
        + secuencia_codificada
    )


if __name__ == "__main__":
    original = serializar_diccionario({"tama": 1})
    encriptado = encriptar(original, [1, 5, 10, 3])
    print(original)
    print(encriptado)
