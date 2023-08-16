from abc import ABC, abstractmethod


class Animal(ABC):
    identificador = 0

    def __init__(self, peso="", nombre="", *args, **kwargs) -> None:
        self.peso = peso
        self.nombre = nombre
        self.__energia = 100
        Animal.identificador += 1

    @property
    def energia(self):
        return self.__energia

    @energia.setter
    def energia(self, value):
        if value < 0:
            self.__energia = 0
        else:
            self.__energia = value

    @abstractmethod
    def desplazarse(self) -> None:
        pass


class Terrestre(Animal, ABC):
    def __init__(self, cantidad_patas="", *args, **kwargs) -> None:
        super().__init__(**kwargs)
        self.cantidad_patas = cantidad_patas

    def energia_gastada_por_desplazamiento(self) -> int:
        return self.peso * 5

    def desplazarse(self) -> str:
        self.energia -= self.energia_gastada_por_desplazamiento()
        print("caminando...")


class Acuatico(Animal, ABC):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**kwargs)

    def energia_gastada_por_desplazamiento(self) -> int:
        return self.peso * 2

    def desplazarse(self) -> str:
        self.energia -= self.energia_gastada_por_desplazamiento()
        print("nadando...")


class Perro(Terrestre):
    def __init__(self, raza="", **kwargs) -> None:
        super().__init__(cantidad_patas=4, **kwargs)
        self.raza = raza

    def ladrar(self) -> str:
        return ("guau guau")


class Pez(Acuatico):
    def __init__(self, color="", **kwargs) -> None:
        super().__init__(**kwargs)
        self.color = color

    def nadar(self) -> str:
        return ("moviendo aleta")


class Ornitorrinco(Terrestre, Acuatico):
    def __init__(self, **kwargs) -> None:
        super().__init__(cantidad_patas=4, **kwargs)

    def energia_gastada_por_desplazamiento(self) -> int:
        return round(self.peso * 3.5)

    def desplazarse(self) -> str:
        super().desplazarse()
        self.energia += self.energia_gastada_por_desplazamiento()


if __name__ == '__main__':
    perro = Perro(nombre='Pongo', raza='Dalmata', peso=3)
    pez = Pez(nombre='Nemo', color='rojo', peso=1)
    ornitorrinco = Ornitorrinco(nombre='Perry', peso=2)

    perro.desplazarse()
    pez.desplazarse()
    ornitorrinco.desplazarse()