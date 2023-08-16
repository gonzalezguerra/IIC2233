from os import path


def cargar_tablero(nombre_archivo: str) -> list:
    path_relativo = path.join("Archivos", f"{nombre_archivo}")
    archivo = open(path_relativo, "rt")
    informacion_archivo = archivo.readlines()
    lista_datos = ",".join(informacion_archivo).split(",")
    size_tablero = int(lista_datos.pop(0))
    tablero = []
    for i in range(size_tablero):
        fila_tablero = []
        for j in range(size_tablero):
            casilla_tablero = lista_datos.pop(0)
            fila_tablero.append(casilla_tablero)
        tablero.append(fila_tablero)
    archivo.close()
    return tablero


def guardar_tablero(nombre_archivo: str, tablero: list) -> None:
    path_relativo = path.join("Archivos", f"{nombre_archivo}")
    with open("path_relativo", "wt") as archivo:
        archivo.write(tablero)


def verificar_valor_bombas(tablero: list) -> int:
    cantidad_bombas_malas = 0
    for i in tablero:
        for j in i:
            if str(j).isnumeric():
                alcance_maximo = (len(tablero) * 2)
                if (int(j) >= alcance_maximo) or (int(j) < 2):
                    cantidad_bombas_malas += 1
    return cantidad_bombas_malas


def verificar_alcance_bomba(tablero: list, coordenada: tuple) -> int:
    if not str(tablero[coordenada[0]][coordenada[1]]).isnumeric():
        return 0
    else:
        casillas_explosion = 1
        for i in [[0, 1], [-1, 0], [0, -1], [1, 0]]:
            actual = [coordenada[0], coordenada[1]]
            while True:
                actual[0] += i[0]
                actual[1] += i[1]
                sobre = (len(tablero) - 1 < actual[0]) or (len(tablero) - 1 < actual[1])
                bajo = (0 > actual[0]) or (0 > actual[1])
                if sobre or bajo or tablero[actual[0]][actual[1]] == "T":
                    break
                casillas_explosion += 1
        return casillas_explosion


# agranda el tablero para que no se indetermine en los bordes "index out of range"
def agrandar_tablero(tablero: list) -> list:
    size_tablero = len(tablero)
    size_nuevo = size_tablero + 2
    tablero_nuevo = [['-' for i in range(size_nuevo)] for i in range(size_nuevo)]
    for j in range(size_tablero):
        for k in range(size_tablero):
            tablero_nuevo[j + 1][k + 1] = tablero[j][k]
    return tablero_nuevo


def verificar_tortugas(tablero: list) -> int:
    tortugas_mal_colocadas = 0
    tablero_ampliado = agrandar_tablero(tablero)
    for i in range(len(tablero)):
        for j in range(len(tablero)):
            tortugas_cerca = False
            if tablero[i][j] == "T":
                if (i >= 0) and (i <= len(tablero)):
                    if (tablero_ampliado[i][j + 1] == "T") or (tablero_ampliado[i + 1][j] == "T"):
                        tortugas_cerca = True
                if (j >= 0) and (j <= len(tablero)):
                    if (tablero_ampliado[i + 1][j] == "T") or (tablero_ampliado[i + 1][j] == "T"):
                        tortugas_cerca = True
            if tortugas_cerca:
                tortugas_mal_colocadas += 1
    return tortugas_mal_colocadas


# verificar si todas las bombas explotan en la cantidad de espacios que deberian
def verificador_tablero(tablero: list) -> int:
    contador_bombas_incompletas = 0
    for k in range(len(tablero)):
        for n in range(len(tablero)):
            if str(tablero[k][n]).isnumeric():
                if verificar_alcance_bomba(tablero, (k, n)) != tablero[k][n]:
                    contador_bombas_incompletas += 1
    return contador_bombas_incompletas


# verifica que ninguna bomba explota por debajo de lo que deberia
def verificador_bombas(tablero: list) -> int:
    contador_bombas_incompletas = 0
    for k in range(len(tablero)):
        for n in range(len(tablero)):
            if str(tablero[k][n]).isnumeric():
                if verificar_alcance_bomba(tablero, (k, n)) < tablero[k][n]:
                    contador_bombas_incompletas += 1
    return contador_bombas_incompletas


# dice si la ubicacion esta dentro del tablero
def esta_dentro(tablero: list, ubicacion: list) -> bool:
    if ubicacion[0] < 0 or ubicacion[1] < 0:
        return False
    if ubicacion[0] == len(tablero) - 1 and ubicacion[1] > len(tablero) - 1:
        return False
    if ubicacion[0] > len(tablero) - 1 or ubicacion[1] > len(tablero) - 1:
        return False
    return True


# nos dice si la posicion donde queremos colocar una Tortuga es valida
def es_valido(tablero: list, ubicacion: list) -> bool:
    tablero_pruebas = tablero.copy()
    direcciones = [[-1, 0], [0, 1], [-1, 0], [0, 1], [0, 0]]
    if not esta_dentro(tablero, ubicacion):
        return False
    if tablero[ubicacion[0]][ubicacion[1]] == "T":
        return False
    if tablero[ubicacion[0]][ubicacion[1]] == "-":
        for i in direcciones:
            if esta_dentro(tablero, [i[0] + ubicacion[0], ubicacion[1] + i[1]]):
                if tablero[i[0] + ubicacion[0]][ubicacion[1] + i[1]] == "T":
                    return False
    if str(tablero[ubicacion[0]][ubicacion[1]]).isnumeric():
        return False
    tablero_pruebas[ubicacion[0]][ubicacion[1]] = "T"
    if verificador_bombas(tablero) > 0:
        return False
    return True


# avanza una celda dentro del tablero
def avanzar(tablero: list, ubicacion: list) -> list:
    if ubicacion[1] == len(tablero) - 1:
        ubicacion[0] += 1
        ubicacion[1] = 0
    else:
        ubicacion[1] += 1
    return ubicacion


# revisa si el tablero agregando un T, formaria parte de la lista tableros
def revisar_tablero(tablero: list, tableros: list, ubicacion: list) -> bool:
    tablero_revision = tablero.copy()
    tablero_revision[ubicacion[0]][ubicacion[1]] = "T"
    if tablero_revision in tableros:
        return False
    return True


# resuelve el tablero, pero con mas parametros que son todos listas
def solucionar(tablero, tablero_original, tableros_anteriores, ubicacion) -> list or None:
    if verificador_tablero(tablero) == 0:
        return tablero
    if es_valido(tablero, ubicacion) and revisar_tablero(tablero, tableros_anteriores, ubicacion):
        tablero[ubicacion[0]][ubicacion[1]] = "T"
        nueva_ubicacion = avanzar(tablero, ubicacion)
        return solucionar(tablero, tablero_original, tableros_anteriores, nueva_ubicacion)
    if esta_dentro(tablero, ubicacion):
        nueva_ubicacion = avanzar(tablero, ubicacion)
        return solucionar(tablero, tablero_original, tableros_anteriores, nueva_ubicacion)
    if tablero not in tableros_anteriores:
        tableros_anteriores.append(tablero)
        tablero = tablero_original.copy()
        return solucionar(tablero, tablero_original, tableros_anteriores, [0, 0])
    return None


def solucionar_tablero(tablero: list) -> list:
    primer_tablero = tablero.copy()
    return solucionar(tablero, primer_tablero, [], [0, 0])