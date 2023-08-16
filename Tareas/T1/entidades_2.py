from abc import ABC
import parametros
from random import choices, random


class Arena:

    def __init__(self, nombre, tipo, rareza, humedad, dureza, estatica):
        self.nombre = nombre
        self.tipo = tipo
        self.__rareza = int(rareza)
        self.__humedad = int(humedad)
        self.__dureza = int(dureza)
        self.__estatica = int(estatica)
        self.items = [[], []]
        dificultad = (self.rareza + self.humedad + self.dureza + self.estatica) / 40
        self.dificultad_arena = round(dificultad, 2)
        self.dificultad_normal = round((self.dificultad_arena * parametros.pond_arena_normal), 2)
        parametros_dif_rocosa = (self.rareza + self.humedad + 2 * self.dureza + self.estatica)
        self.dificultad_rocosa = round(parametros_dif_rocosa / 50, 2)

        archivo = open("tesoros.csv", encoding="UTF-8")
        lineas_tesoros = archivo.readlines()
        lineas_tesoros = lineas_tesoros[1:]
        for linea in lineas_tesoros:
            linea = linea.strip("\n")
            linea = linea.split(",")
            self.items[0].append(Tesoros(linea[0], linea[1], linea[2], linea[3]))
        archivo.close()

        archivo = open("consumibles.csv", encoding="UTF-8")
        lineas_consumibles = archivo.readlines()
        lineas_consumibles = lineas_consumibles[1:]
        for linea in lineas_consumibles:
            linea = linea.strip("\n")
            linea = linea.split(",")
            consumible = Consumibles(linea[0], linea[1], linea[2], linea[3], linea[4], linea[5])
            self.items[1].append(consumible)
        archivo.close()

    @property
    def rareza(self):
        return self.__rareza

    @rareza.setter
    def rareza(self, valor):
        self.__rareza = valor
        if self.__rareza < 1:
            self.__rareza = 1
        elif self.__rareza > 10:
            self.__rareza = 10

    @property
    def humedad(self):
        return self.__humedad

    @humedad.setter
    def humedad(self, valor):
        self.__humedad = valor
        if self.__humedad < 1:
            self.__humedad = 1
        elif self.__humedad > 10:
            self.__humedad = 10

    @property
    def dureza(self):
        return self.__dureza

    @dureza.setter
    def dureza(self, valor):
        self.__dureza = valor
        if self.__dureza < 1:
            self.__dureza = 1
        elif self.__dureza > 10:
            self.__dureza = 10

    @property
    def estatica(self):
        return self.__estatica

    @estatica.setter
    def estatica(self, valor):
        self.__estatica = valor
        if self.__estatica < 1:
            self.__estatica = 1
        elif self.__estatica > 10:
            self.__estatica = 10


class Item(ABC):

    def __init__(self, nombre, tipo, descripcion):
        self.nombre = nombre
        self.tipo = tipo
        self.descripcion = descripcion


class Consumibles(Item):

    def __init__(self, nombre, descripcion, energia, fuerza, suerte, felicidad):
        super().__init__(nombre, "Consumibles", descripcion)
        self.tipo = "Consumibles"
        self.energia = int(energia)
        self.fuerza = int(fuerza)
        self.suerte = int(suerte)
        self.felicidad = int(felicidad)


class Tesoros(Item):

    def __init__(self, nombre, descripcion, calidad, cambio):
        super().__init__(nombre, "Tesoros", descripcion)
        self.tipo = "Tesoros"
        self.calidad = calidad
        self.cambio = cambio


class Excavador(ABC):

    def __init__(self, nombre, edad, energia, fuerza, suerte, felicidad):
        self.nombre = nombre
        self.edad = int(edad)
        self.__energia = int(energia)
        self.__fuerza = int(fuerza)
        self.__suerte = int(suerte)
        self.__felicidad = int(felicidad)
        self.dias_descanso = 0

    @property
    def energia(self):
        return self.__energia

    @energia.setter
    def energia(self, valor):
        self.__energia = valor
        if self.__energia < 0:
            self.__energia = 0
        elif self.__energia > 100:
            self.__energia = 100

    @property
    def fuerza(self):
        return self.__fuerza

    @fuerza.setter
    def fuerza(self, valor):
        self.__fuerza = valor
        if self.__fuerza < 1:
            self.__fuerza = 1
        elif self.__fuerza > 10:
            self.__fuerza = 10

    @property
    def suerte(self):
        return self.__suerte

    @suerte.setter
    def suerte(self, valor):
        self.__suerte = valor
        if self.__suerte < 1:
            self.__suerte = 1
        elif self.__suerte > 10:
            self.__suerte = 10

    @property
    def felicidad(self):
        return self.__felicidad

    @felicidad.setter
    def felicidad(self, valor):
        self.__felicidad = valor
        if self.__felicidad < 1:
            self.__felicidad = 1
        elif self.__felicidad > 10:
            self.__felicidad = 10

    def cavar(self, Arena):
        if Arena.tipo == "normal":
            dificultad = Arena.dificultad_normal
        elif Arena.tipo == "mojada":
            dificultad = Arena.dificultad_arena
        elif Arena.tipo == "rocosa" or Arena.tipo == "magnetica":
            dificultad = Arena.dificultad_rocosa
        metros = ((30 / self.edad) + (self.felicidad + 2 * self.fuerza) / 10) / (10 * dificultad)
        return round(metros, 2)

    def descansar(self):
        dias = round(self.edad / 20)
        self.dias_descanso = dias

    def encontrar_item(self, Arena):
        if Arena.tipo == "mojada" or Arena.tipo == "magnetica":
            probabilidad_item = 1
            pesos = [0.5, 0.5]
        elif Arena.tipo == "normal" or Arena.tipo == "rocosa":
            probabilidad_item = parametros.probabilidad_item * (self.suerte / 10)
            pesos = [parametros.prob_encontrar_consumible, parametros.prob_encontrar_tesoro]
        if random() <= probabilidad_item:
            opciones = ["consumible", "tesoro"]
            eleccion = choices(opciones, weights=pesos, k=1)
            eleccion = eleccion[0]
            if eleccion == "tesoro":
                objeto = choices(Arena.items[0])
            elif eleccion == "consumible":
                objeto = choices(Arena.items[1])
            objeto = objeto[0]
            return objeto
        return None

    def gastar_energia(self):
        energia_gastada = round((10 / self.fuerza) + (self.edad / 6))
        self.energia -= energia_gastada

    def consumir(self, item_consumir):
        self.energia += item_consumir.energia
        self.fuerza += item_consumir.fuerza
        self.suerte += item_consumir.suerte
        self.felicidad += item_consumir.felicidad


class Docencio(Excavador):

    def __init__(self, nombre, edad, energia, fuerza, suerte, felicidad):
        self.clase = "docencio"
        super().__init__(nombre, int(edad), int(energia), int(fuerza), int(suerte), int(felicidad))

    def cavar(self, Arena):
        if Arena.tipo == "normal":
            dificultad = Arena.dificultad_normal
        elif Arena.tipo == "mojada":
            dificultad = Arena.dificultad_arena
        elif Arena.tipo == "rocosa" or Arena.tipo == "magnetica":
            dificultad = Arena.dificultad_rocosa
        metros = ((30 / self.edad) + (self.felicidad + 2 * self.fuerza) / 10) / (10 * dificultad)
        self.felicidad += parametros.felicidad_adicional_docencio
        self.fuerza += parametros.fuerza_adicional_docencio
        self.energia = int(self.energia) - parametros.energia_perdida_docencio
        return round(metros, 2)


class Tareo(Excavador):

    def __init__(self, nombre, edad, energia, fuerza, suerte, felicidad):
        self.clase = "tareo"
        super().__init__(nombre, int(edad), int(energia), int(fuerza), int(suerte), int(felicidad))

    def consumir(self, item_consumir):
        self.energia += item_consumir.energia + parametros.energia_adicional_tareo
        self.fuerza += item_consumir.fuerza
        self.suerte += item_consumir.suerte + parametros.suerte_adicional_tareo
        self.felicidad += item_consumir.felicidad - parametros.felicidad_perdida_tareo
        self.edad += parametros.edad_adicional_tareo


class Hibrido(Docencio, Tareo):

    def __init__(self, nombre, edad, energia, fuerza, suerte, felicidad):
        self.clase = "hibrido"
        super().__init__(nombre, int(edad), int(energia), int(fuerza), int(suerte), int(felicidad))
        self.__energia = int(energia)

    @property
    def energia(self):
        return self.__energia

    @energia.setter
    def energia(self, valor):
        self.__energia = valor
        if self.__energia < 20:
            self.__energia = 20
        elif self.__energia > 100:
            self.__energia = 100

    def gastar_energia(self):
        energia_gastada = round(((10 / self.fuerza) + (self.edad / 6)) / 2)
        self.energia -= energia_gastada
