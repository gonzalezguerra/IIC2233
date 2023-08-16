import parametros
from random import choices, random, randint
from entidades_2 import Arena, Tareo, Docencio, Hibrido
from listas import lista_tareo, lista_docencio, lista_hibrido, lista_excavadores, lista_arenas


class Torneo:

    def __init__(self, Arena, equipo):
        self.arena = Arena
        self.eventos = ["lluvia", "terremoto", "derrumbe"]
        self.equipo = equipo
        self.mochila = []
        self.metros_cavados = 0
        self.meta = parametros.metros_meta
        self.dias_transcurridos = 0
        self.dias_totales = parametros.dias_totales_torneo

    def simular_dia(self):
        print(f"DIA {self.dias_transcurridos}")
        print("")
        print("Metros Cavados:")
        metros_cavados_dia = 0
        self.dias_transcurridos += 1

        if self.arena.tipo == "magnetica":
            self.arena.humedad = randint(1, 10)
            self.arena.dureza = randint(1, 10)

        for excavador in self.equipo:
            if excavador.dias_descanso == 0:
                metros = excavador.cavar(self.arena)
                print(f"{excavador.nombre} ha cavado {metros} metros")
                self.metros_cavados += metros
                metros_cavados_dia += metros
            elif excavador.dias_descanso > 0:
                print(f"{excavador.nombre} esta descansando")
        print(f"El equipo ha conseguido excavar {metros_cavados_dia} metros")
        print("")

        lista_items_dia = [[], []]
        for excavador in self.equipo:
            if excavador.dias_descanso == 0:
                item = excavador.encontrar_item(self.arena)
                if item == None:
                    print(f"{excavador.nombre} no encontro un objeto")
                else:
                    print(f"{excavador.nombre} encontro un {item.tipo} que se llama {item.nombre}")
                    if item.tipo == "Tesoros":
                        lista_items_dia[0].append(item)
                    elif item.tipo == "Consumibles":
                        lista_items_dia[1].append(item)
                excavador.gastar_energia()
                if excavador.energia <= 0:
                    excavador.descansar()
            elif excavador.dias_descanso > 0:
                print(f"{excavador.nombre}: esta descansando")
                excavador.dias_descanso -= 1
                if excavador.dias_descanso == 0:
                    excavador.energia = 100

        print("")
        texto_de_items = "El total de items econtrados fueron"
        print(f"{texto_de_items} {len(lista_items_dia[0]) + len(lista_items_dia[1])}")
        print(f"Se encontraron {len(lista_items_dia[0])} Tesoros")
        for objeto in lista_items_dia[0]:
            self.mochila.append(objeto)
        print(f"Se encontraron {len(lista_items_dia[1])} Consumibles")
        for objeto in lista_items_dia[1]:
            self.mochila.append(objeto)

        evento = self.iniciar_evento()
        if evento != None:
            print("")
            print(f"Durante el dia de trabajo ocurrio un {evento}")
            print(f"La arena final es del tipo {self.arena.tipo}")
            print(f"Tu equipo ha perdido {parametros.felicidad_perdida} de felicidad")

        for excavador in self.equipo:
            if excavador.dias_descanso > 0:
                print(f"{excavador.nombre} se encuentra descansando")

    def mostrar_estado(self):
        print("")
        print("ESTADO TORNEO")
        print("")
        print(f"Dia actual: {self.dias_transcurridos}")
        print(f"Tipo de arena: {self.arena.tipo}")
        print(f"Metros excavados: {self.metros_cavados} / {self.meta}")
        print("")
        print("Excavadores:")
        print("")
        formato = "{: ^14s} | {: ^8s} | {: ^8s} | {: ^8s} | {: ^8s} | {: ^8s} "
        print(formato.format("Nombre", "Clase", "Energia", "Fuerza", "Suerte", "Felicidad"))
        for excavador in self.equipo:
            primera_parte = f"{excavador.nombre:14s} | {excavador.clase: ^8s} | "
            segunda_parte = f"{excavador.energia: ^8d} | {excavador.fuerza: ^8d} | "
            tercera_parte = f"{excavador.suerte:^8d} | {excavador.felicidad:^8d}"
            print(f"{primera_parte}{segunda_parte}{tercera_parte}")

    def ver_mochila(self):
        print("")
        print("*** MENU ITEMS ***")
        print("")
        contador = 0
        print(" {:^32} | {: ^11s} | {: ^65s} ".format("Nombre", "Tipo", "Descripcion"))
        for item in self.mochila:
            contador += 1
            print(f"[{contador}]{item.nombre:^30} | {item.tipo: ^11s} | {item.descripcion: ^65s} ")
        print("")
        print(f"[{contador+1}] Volver")
        print(f"[X] Salir del programa")
        print("")
        print("Indique su opcion")
        respuesta = input("-> ")
        print("")
        return respuesta

    def usar_consumible(self, consumible):
        for excavador in self.equipo:
            excavador.consumir(consumible)

    def abrir_tesoro(self, tesoro):
        if int(tesoro.calidad) == 1:
            if tesoro.cambio == "docencio":
                excavador = choices(lista_docencio, k=1)
            elif tesoro.cambio == "tareo":
                excavador = choices(lista_tareo, k=1)
            elif tesoro.cambio == "hibrido":
                excavador = choices(lista_hibrido, k=1)
            excavador = excavador[0]
            self.equipo.append(excavador)
        elif int(tesoro.calidad) == 2:
            if self.arena.tipo != tesoro.cambio:
                while True:
                    buscar = choices(lista_arenas, k=1)
                    buscar = buscar[0]
                    if buscar.tipo == tesoro.cambio:
                        self.arena = buscar
                        break

    def iniciar_evento(self):
        if random() <= parametros.prob_iniciar_evento:

            for excavador in self.equipo:
                excavador.felicidad -= parametros.felicidad_perdida

            opciones = ["derrumbe", "lluvia", "terremoto"]
            pesos = [parametros.prob_derrumbe, parametros.prob_lluvia, parametros.prob_terremoto]
            eleccion = choices(opciones, weights=pesos, k=1)
            eleccion = eleccion[0]

            if eleccion == "derrumbe":
                if self.arena.tipo != "normal":
                    while True:
                        buscar = choices(lista_arenas, k=1)
                        buscar = buscar[0]
                        if buscar.tipo == "normal":
                            self.arena = buscar
                            self.metros_cavados -= parametros.metros_perdido_derrumbe
                            break

            elif eleccion == "lluvia":
                if self.arena.tipo == "normal":
                    while True:
                        buscar = choices(lista_arenas, k=1)
                        buscar = buscar[0]
                        if buscar.tipo == "mojada":
                            self.arena = buscar
                            break
                elif self.arena.tipo == "rocosa":
                    while True:
                        buscar = choices(lista_arenas, k=1)
                        buscar = buscar[0]
                        if buscar.tipo == "magnetica":
                            self.arena = buscar
                            break

            elif eleccion == "terremoto":
                if self.arena.tipo == "normal":
                    while True:
                        buscar = choices(lista_arenas, k=1)
                        buscar = buscar[0]
                        if buscar.tipo == "rocosa":
                            self.arena = buscar
                            break
                elif self.arena.tipo == "mojada":
                    while True:
                        buscar = choices(lista_arenas, k=1)
                        buscar = buscar[0]
                        if buscar.tipo == "magnetica":
                            self.arena = buscar
                            break
            return eleccion
        return None
