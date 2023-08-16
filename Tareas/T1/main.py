import entidades
import parametros
from random import choices
from os import path
from copy import deepcopy

volver = "volver"
salir = "salir"


def menu_inicio():
    retorno_menu = None
    while retorno_menu != salir:
        print("")
        print("*** MENU DE INICIO ***")
        print("")
        print("[1] Nueva partida")
        print("[2] Cargar partida")
        print("[X] Salir")
        print("")
        print("Indique su opcion (1, 2 o X):")
        opcion = input("-> ")
        print("")

        if opcion == "1":
            equipo = []
            while True:
                buscar = choices(entidades.lista_arenas, k=1)
                buscar = buscar[0]
                if buscar.tipo == parametros.arena_inicial:
                    Arena = buscar
                    break
            for i in range(parametros.cantidad_excavadores_iniciales):
                excavador = choices(entidades.lista_excavadores, k=1)
                excavador = excavador[0]
                equipo.append(deepcopy(excavador))
            Torneo_actual = entidades.Torneo(Arena, equipo)
            retorno_menu = menu_principal(Torneo_actual)

        elif opcion == "2":
            if path.exists(f"DCCavaCava.txt"):
                archivo = open("DCCavaCava.txt", "r", encoding="UTF-8")
                lineas = archivo.readlines()
                archivo.close()
                for linea in lineas:
                    linea = linea.strip("\n")
                lineas[2] = lineas[2].strip("\n")
                init = lineas[0].split(",")
                arena = entidades.Arena(init[0], init[1], init[2], init[3], init[4], init[5])
                equipo = []
                for i in range(1, 4):
                    lineas[i] = lineas[i].split("$")
                for info in lineas[1]:
                    info = info.split(",")
                    clase = info.pop(1).strip(" ")
                    dias_descanso = info[6]
                    name = info[0]
                    edad = info[1]
                    ener = info[2]
                    if clase == "tareo":
                        excavador = entidades.Tareo(name, edad, ener, info[3], info[4], info[5])
                        excavador.dias_descanso = int(dias_descanso)
                    elif clase == "docencio":
                        excavador = entidades.Docencio(name, edad, ener, info[3], info[4], info[5])
                        excavador.dias_descanso = int(dias_descanso)
                    elif clase == "hibrido":
                        excavador = entidades.Hibrido(name, edad, ener, info[3], info[4], info[5])
                        excavador.dias_descanso = int(dias_descanso)
                    equipo.append(excavador)
                mochila = []

                for info in lineas[2]:
                    info = info.split(",")
                    name = info[0]
                    ener = info[2]
                    fuer = info[3]
                    consumible = entidades.Consumibles(name, info[1], ener, fuer, info[4], info[5])
                    mochila.append(consumible)

                for info in lineas[3]:
                    info = info.split(",")
                    tesoros = entidades.Tesoros(info[0], info[1], info[2], info[3])
                    mochila.append(tesoros)

                lineas[4] = lineas[4].split(",")
                metros_cavados = lineas[4][0]
                meta = lineas[4][1]
                dias_transcurridos = lineas[4][2]
                dias_totales = lineas[4][3]

                Torneo_guardado = entidades.Torneo(arena, equipo)
                Torneo_guardado.mochila = mochila
                Torneo_guardado.metros_cavados = float(metros_cavados)
                Torneo_guardado.meta = float(meta)
                Torneo_guardado.dias_transcurridos = int(dias_transcurridos)
                Torneo_guardado.dias_totales = int(dias_totales)
                retorno_menu = menu_principal(Torneo_guardado)
            else:
                print("No hay partidas guardadas")

        elif opcion == "X":
            retorno_menu = salir
            print("EL PROGRAMA SE HA CERRADO")

        else:
            print("Opcion invalida")


def menu_principal(Torneo):
    while True:
        print("")
        print("*** MENU PRINCIPAL ***")
        print("")
        print(f"Dia torneo DCCavaCava: {Torneo.dias_transcurridos} / {Torneo.dias_totales}")
        print(f"Tipo de arena: {Torneo.arena.tipo}")
        print("[1] Simular dia torneo")
        print("[2] Ver estado torneo")
        print("[3] Ver items")
        print("[4] Guardar partida")
        print("[5] Volver")
        print("[X] Salir del programa")
        print("")
        print("Indique su opcion (1, 2, 3, 4, 5 o X):")

        opcion = input("-> ")
        print("")
        if opcion == "1":
            if Torneo.metros_cavados >= Torneo.meta:
                print("FELICIDADES, GANASTE!!!")
            elif Torneo.dias_transcurridos >= Torneo.dias_totales:
                print("PERDISTE :(")
            else:
                Torneo.simular_dia()

        elif opcion == "2":
            Torneo.mostrar_estado()

        elif opcion == "3":
            retorno_menu = menu_items(Torneo)
            if retorno_menu == salir:
                return salir

        elif opcion == "4":
            archivo = open("DCCavaCava.txt", "w", encoding="UTF-8")
            arena_1 = f"{Torneo.arena.nombre},{Torneo.arena.tipo},{Torneo.arena.rareza},"
            arena_2 = f"{Torneo.arena.humedad},{Torneo.arena.dureza},{Torneo.arena.estatica}"
            excavadores = ""

            for excavador in Torneo.equipo:
                datos_excavador = f"{excavador.nombre}, {excavador.clase}, {excavador.edad}, "
                datos_2 = f"{excavador.energia}, {excavador.fuerza}, {excavador.suerte},"
                datos_3 = f" {excavador.fuerza}, {excavador.suerte}, "
                datos_4 = f"{excavador.felicidad}, {excavador.dias_descanso}"
                excavadores += f"{datos_excavador}{datos_2}{datos_3}{datos_4}$"
            excavadores = excavadores[:-1]
            consumibles = ""
            tesoros = ""

            for item in Torneo.mochila:
                if item.tipo == "Consumibles":
                    consumibles += f"{item.nombre},{item.descripcion},{item.energia}"
                    consumibles += f",{item.fuerza},{item.suerte},{item.felicidad}$"
                elif item.tipo == "Tesoros":
                    tesoros += f"{item.nombre},{item.descripcion},{item.calidad},{item.cambio}$"
            consumibles = consumibles[:-1]
            tesoros = tesoros[:-1]
            metros_cavados = Torneo.metros_cavados
            meta = Torneo.meta
            dias_transcurridos = Torneo.dias_transcurridos
            dias_totales = Torneo.dias_totales
            print(f"{arena_1}{arena_2}", file=archivo)
            print(f"{excavadores}", file=archivo)
            print(f"{consumibles}", file=archivo)
            print(f"{tesoros}", file=archivo)
            print(f"{metros_cavados},{meta},{dias_transcurridos},{dias_totales}", file=archivo)
            print("La partida ha sido guardada exitosamente")

        elif opcion == "5":
            return volver

        elif opcion == "X":
            return salir

        else:
            print("Opcion invalida")


def menu_items(Torneo):
    while True:
        respuesta = Torneo.ver_mochila()
        if respuesta.isnumeric():
            if int(respuesta) <= len(Torneo.mochila):
                item = Torneo.mochila.pop(int(respuesta) - 1)
                if item.tipo == "Consumibles":
                    Torneo.usar_consumible(item)
                elif item.tipo == "Tesoros":
                    Torneo.abrir_tesoro(item)
                print(item.descripcion)
            elif int(respuesta) == len(Torneo.mochila) + 1:
                return volver

        elif respuesta == "X":
            return salir

        else:
            print("Opcion invalida")


menu_inicio()
