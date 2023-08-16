from collections import defaultdict, deque


class Jugador:
    def __init__(self, nombre: str, velocidad: int) -> None:
        self.nombre = nombre
        self.velocidad = velocidad
    
    def __repr__(self) -> None:
        return f'Jugador: {self.nombre}, Velocidad: {self.velocidad}'


class Equipo:
    def __init__(self) -> None:
        self.jugadores = dict()
        self.dict_adyacencia = defaultdict(set)
    
    def agregar_jugador(self, id_jugador: int, jugador: Jugador) -> bool:
        '''Agrega un nuevo jugador al equipo.'''
        # Completar
        if id_jugador not in self.jugadores:
            self.jugadores[id_jugador] = jugador
            return True
        else:
            return False

    def agregar_vecinos(self, id_jugador: int, vecinos: list[int]) -> int:
        '''Agrega una lista de vecinos a un jugador.'''
        # Completar
        if id_jugador not in self.dict_adyacencia:
            return -1
        else:
            numero_agregados = 0
            for i in vecinos:
                if i not in self.dict_adyacencia[id_jugador]:
                    self.dict_adyacencia[id_jugador].add(i)
                    numero_agregados += 1
            return numero_agregados

    def mejor_amigo(self, id_jugador: int) -> Jugador:
        '''Retorna al vecino con la velocidad más similar.'''
        # Completar
        if len(self.dict_adyacencia[id_jugador]) == 0:
            return None
        else:
            vel_jugador = self.jugadores[id_jugador].velocidad
            velocidad = vel_jugador
            for i in self.dict_adyacencia[id_jugador]:
                if abs(self.jugadores[i].velocidad - vel_jugador) < velocidad:
                    velocidad = abs(self.jugadores[i].velocidad - vel_jugador)
                    mejor_amigo = self.jugadores[i]
            return mejor_amigo

    def peor_compañero(self, id_jugador: int) -> Jugador:
        '''Retorna al compañero de equipo con la mayor diferencia de velocidad.'''
        # Completar
        if len(self.jugadores) == 1:
            return None
        else:
            vel_jugador = self.jugadores[id_jugador].velocidad
            velocidad = 0
            for i in self.jugadores:
                if abs(self.jugadores[i].velocidad - vel_jugador) > velocidad:
                    velocidad = abs(self.jugadores[i].velocidad - vel_jugador)
                    peor_amigo = self.jugadores[i]
            return peor_amigo

    def peor_conocido(self, id_jugador: int) -> Jugador:
        '''Retorna al amigo con la mayor diferencia de velocidad.'''
        # Completar
        if len(self.dict_adyacencia[id_jugador]) == 0:
            return None
        else:
            vel_jugador = self.jugadores[id_jugador].velocidad
            velocidad = 0
            lista = self.visitar(id_jugador)
            for i in lista:
                if abs(self.jugadores[i].velocidad - vel_jugador) > velocidad:
                    velocidad = abs(self.jugadores[i].velocidad - vel_jugador)
                    peor_amigo = self.jugadores[i]
        return peor_amigo

    def distancia(self, id_jugador_1: int, id_jugador_2: int) -> int:
        '''Retorna el tamaño del camino más corto entre los jugadores.'''    
        rutas = self.recorrido(id_jugador_1, id_jugador_2)
        if len(rutas) == 0:
            return -1
        rutas.sort(key = lambda ruta: len(ruta)) # Solo se ordenan las rutas por largo.
        return len(rutas[0]) -1

    def recorrido(self, id_jugador_1: int, id_jugador_2: int, visitados = set()):
        rutas = [] # Aquí rutas, es una lista que contendrá a todas las posibles rutas, donde cada una será otra lista.
        if id_jugador_1 == id_jugador_2:
            rutas.append([id_jugador_1]) # Caso base, si el nodo actual es el destino agregamos la ruta y retornamos la lista.
            return rutas

        visitados.add(id_jugador_1)

        for hijo in self.dict_adyacencia[id_jugador_1]:
            if hijo not in visitados:

                r_hijo = self.recorrido(hijo, id_jugador_2, visitados.copy()) # VER NOTA ABAJO
                # Al igual que antes rutas_rec siempre retorna una lista

                for ruta in r_hijo: #Ya que esta vez lo retornado es una lista de listas, recorremos cada ruta
                    ruta.insert(0, hijo) #Agregamos el nodo actual a la ruta

                    rutas.append(ruta) #agregamos esta ruta a las rutas locales

        return rutas

    def visitar(self, nodo, visitados=list()):
        for hijo in self.dict_adyacencia[nodo]:
            if hijo not in visitados:
                visitados.append(hijo)
                nuevos = self.visitar(hijo, visitados.copy())
                for i in nuevos:
                    if i not in visitados:
                        visitados.append(i)
        return visitados

if __name__ == '__main__':
    equipo = Equipo()
    jugadores = {
        0: Jugador('Alonso', 1),
        1: Jugador('Alba', 3),
        2: Jugador('Alicia', 6),
        3: Jugador('Alex', 10)
    }
    adyacencia = {
        0: [1],
        1: [0, 2],
        2: [1],
    }
    for idj, jugador in jugadores.items():
        equipo.agregar_jugador(id_jugador=idj, jugador=jugador)
    for idj, vecinos in adyacencia.items():
        equipo.agregar_vecinos(id_jugador=idj, vecinos=vecinos)
    
    print(f'El mejor amigo de Alba es {equipo.mejor_amigo(1)}') 
    print(f'El peor compañero de Alonso es {equipo.peor_compañero(0)}')
    print(f'El peor amigo de Alicia es {equipo.peor_compañero(2)}')
    print(f'La distancia entre Alicia y Alonso es {equipo.distancia(2, 0)}')
    print(f'La distancia entre Alba y Alex es {equipo.distancia(1, 3)}')