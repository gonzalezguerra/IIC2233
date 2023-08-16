from entidades import Arena
from entidades_2 import Tareo, Docencio, Hibrido

lista_arenas = []
archivo = open("arenas.csv", encoding="UTF-8")
lineas_arenas = archivo.readlines()
lineas_arenas = lineas_arenas[1:]
for linea in lineas_arenas:
    linea = linea.strip("\n")
    linea = linea.split(",")
    lista_arenas.append(Arena(linea[0], linea[1], linea[2], linea[3], linea[4], linea[5]))
archivo.close()

lista_tareo = []
lista_docencio = []
lista_hibrido = []
lista_excavadores = []
archivo = open("excavadores.csv", encoding="UTF-8")
lineas_excavadores = archivo.readlines()
lineas_excavadores = lineas_excavadores[1:]

for linea in lineas_excavadores:
    linea = linea.strip("\n")
    linea = linea.split(",")
    if linea[1] == "tareo":
        tareo = Tareo(linea[0], linea[2], linea[3], linea[4], linea[5], linea[6])
        lista_tareo.append(Tareo(linea[0], linea[2], linea[3], linea[4], linea[5], linea[6]))
        lista_excavadores.append(tareo)
    elif linea[1] == "docencio":
        docencio = Docencio(linea[0], linea[2], linea[3], linea[4], linea[5], linea[6])
        lista_docencio.append(Docencio(linea[0], linea[2], linea[3], linea[4], linea[5], linea[6]))
        lista_excavadores.append(docencio)
    elif linea[1] == "hibrido":
        hibrido = Hibrido(linea[0], linea[2], linea[3], linea[4], linea[5], linea[6])
        lista_hibrido.append(Hibrido(linea[0], linea[2], linea[3], linea[4], linea[5], linea[6]))
        lista_excavadores.append(hibrido)
    archivo.close()
