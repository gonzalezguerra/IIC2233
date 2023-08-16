from copy import copy
from functools import reduce
from itertools import groupby
from typing import Generator

from utilidades import (
    Categoria, Producto, duplicador_generadores, generador_a_lista
)


# ----------------------------------------------------------------------------
# Parte 1: Cargar dataset
# ----------------------------------------------------------------------------

def cargar_productos(ruta: str) -> Generator:
    # TODO: Completar
    with open(ruta, "r") as file:
        lineas = file.readlines()
        lineas.pop(0)
    for row in lineas:
        x = row.strip("\n").split(",")
        yield Producto(int(x[0]),x[1],int(x[2]),x[3],int(x[4]),x[5])

def cargar_categorias(ruta: str) -> Generator:
    # TODO: Completar
    with open(ruta, "r") as file:
        lineas = file.readlines()
        lineas.pop(0)
    for row in lineas:
        x = row.strip("\n").split(",")
        yield Categoria(x[0], int(x[1]))


# ----------------------------------------------------------------------------
# Parte 2: Consultas sobre generadores
# ----------------------------------------------------------------------------

def obtener_productos(generador_productos: Generator) -> map:
    # TODO: Completar
    def nombre_produto(row):
        return row[1]
    return map(nombre_produto, generador_productos)
    


def obtener_precio_promedio(generador_productos: Generator) -> int:
    # TODO: Completar
    y = len(duplicador_generadores(generador_productos))
    def nombre_produto(row):
        return row[2]
    x = map(nombre_produto, generador_productos)

    
    return round(reduce(lambda a, b: a+b, x)/y)


def filtrar_por_medida(generador_productos: Generator,
                       medida_min: float, medida_max: float, unidad: str
                       ) -> filter:
    # TODO: Completar
    def medida(object):
        medi = object.medida
        unida = object.unidad_medida
        if medi > medida_min and medi < medida_max and unidad == unida:
            return True
        return False
    
    return filter(medida, generador_productos)



def filtrar_por_categoria(generador_productos: Generator,
                          generador_categorias: Generator,
                          nombre_categoria: str) -> Generator:
    # TODO: Completar
    def cat(object):
        cate = object.nombre_categoria
        id = object.id_producto
        if cate == nombre_categoria:
            return True
        return False
    
    y = filter(cat, generador_categorias)

    def nombre_produto(row):
        return row[1]
    x = map(nombre_produto, y)
    z = generador_a_lista(x)

    def ides(object, lista=z.copy()):
        i = object.id_producto
        if i in lista:
            return True
        return False
    
    return filter(ides, generador_productos)


def agrupar_por_pasillo(generador_productos: Generator) -> Generator:
    # TODO: Completar
    return groupby(generador_productos, lambda x : x.pasillo)


# ----------------------------------------------------------------------------
# Parte 3: Iterables
# ----------------------------------------------------------------------------

class Carrito:
    def __init__(self, productos: list) -> None:
        self.productos = productos

    def __iter__(self):
        # TODO: Completar
        return IteradorCarrito(self.productos)


class IteradorCarrito:
    def __init__(self, iterable_productos: list) -> None:
        self.productos_iterable = copy(iterable_productos)

    def __iter__(self):
        # TODO: Completar
        return self

    def __next__(self):
        # TODO: Completar
        if not self.productos_iterable:
            raise StopIteration()
        def precio(object):
            return object.precio
        lista_ordenada = sorted(self.productos_iterable.copy(),key=precio)
        proximo_pedido = lista_ordenada.pop(0)
        self.productos_iterable.remove(proximo_pedido)
        return proximo_pedido
