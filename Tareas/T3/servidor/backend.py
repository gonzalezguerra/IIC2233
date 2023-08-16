import socket
import threading
from pickle import loads, dumps
from random import random, randint, choice
from PyQt5.QtCore import QThread
from functions import parametro_json, codificar, decodificar
from cripto import encriptar, desencriptar


class Mensaje:

    def __init__(self, tipo, info, nombre) -> None:
        self.tipo = tipo
        self.info = info
        self.nombre = nombre


class Servidor:

    def __init__(self, port, host):
        self.max_recv = 2**16
        self.host = host
        self.port = port
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockets = {}
        nombre_1 = ''.join(parametro_json("NOMBRE_1"))
        nombre_2 = ''.join(parametro_json("NOMBRE_2"))
        nombre_3 = ''.join(parametro_json("NOMBRE_3"))
        nombre_4 = ''.join(parametro_json("NOMBRE_4"))
        self.nombres = [nombre_1, nombre_2, nombre_3, nombre_4]
        self.nombres_usados = []
        self.lobby = True
        self.desconectados = []
        self.ultima_jugada = Mensaje("", "", "")
        self.ultima_accion = Mensaje("", "", "")
        self.ultimo_anunciado = 0
        self.bind_listen()
        self.accept_connections()
        self.online()

    def bind_listen(self):
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen(250)
        print(f'Servidor escuchando en {self.host} : {self.port}')

    def accept_connections(self):
        thread = threading.Thread(target=self.accept_connections_thread, daemon=True)
        thread.start()

    def accept_connections_thread(self):
        while True:
            client_socket, address = self.socket_server.accept()
            if len(self.nombres_usados) < 4 and self.lobby:
                while True:
                    x = choice(self.nombres)
                    if x not in self.nombres_usados:
                        nombre_cliente = x
                        self.nombres_usados.append(x)
                        break
                self.sockets[client_socket] = nombre_cliente
                self.send(Mensaje("nombre", nombre_cliente, ""), client_socket)
                QThread.msleep(50)
                listening_client_thread = threading.Thread( \
                    target=self.listen_client_thread, \
                    args=(client_socket, ), \
                    daemon=True)
                listening_client_thread.start()
                print(f"{self.sockets[client_socket]} conectado a servidor")
                self.iniciar_lobby(client_socket, self.sockets[client_socket])
                QThread.msleep(50)
                self.chat_management(Mensaje("conexion", self.sockets[client_socket], ""))
            else:
                listening_client_thread = threading.Thread( \
                    target=self.listen_client_thread, \
                    args=(client_socket, ), \
                    daemon=True)
                listening_client_thread.start()
                QThread.msleep(50)
                if self.lobby:
                    print("Un cliente no se pudo conectar [la sala esta llena]")
                    self.send(Mensaje("sala", "", ""), client_socket)
                else:
                    print("Un cliente no se pudo conectar [partida en juego]")
                    self.send(Mensaje("juego", "", ""), client_socket)
                QThread.msleep(50)
                client_socket.close()

    def listen_client_thread(self, client_socket):
        while True:
            try:
                x = client_socket.recv(2**16)
                if len(x) == 0:
                    print(f"Cliente desconectado, clientes actuales en sala {len(self.sockets)-1}")
                    self.nombres_usados.remove(self.sockets[client_socket])
                    if self.lobby:
                        self.chat_management(Mensaje("desconexion",self.sockets[client_socket],""))
                        del self.sockets[client_socket]
                        self.reiniciar_lobby()
                    else:
                        self.desconectados.append(self.sockets[client_socket])
                        del self.sockets[client_socket]
                        self.verificar_bot()
                    break
                try:
                    mensaje = x
                    self.recibir_mensajes(mensaje)
                except ConnectionResetError:
                    print(f"Cliente desconectado, clientes actuales en sala {len(self.sockets)-1}")
                    self.nombres_usados.remove(self.sockets[client_socket])
                    if self.lobby:
                        self.chat_management(Mensaje("desconexion",self.sockets[client_socket],""))
                        del self.sockets[client_socket]
                        self.reiniciar_lobby()
                    else:
                        self.desconectados.append(self.sockets[client_socket])
                        del self.sockets[client_socket]
                        self.verificar_bot()
                    break
            except (OSError, EOFError, ValueError):
                pass

    def online(self):
        while True:
            pass

    def chat_management(self, msg):
        try:
            for skt in self.sockets.keys():
                self.send(msg, skt)
                QThread.msleep(50)
        except RuntimeError:
            pass

    def iniciar_lobby(self, sock, nombre):
        if self.lobby:
            for skt in self.sockets:
                if self.sockets[skt] != nombre:
                    msg = Mensaje("conexion", self.sockets[skt], "")
                    self.send(msg, sock)
                    QThread.msleep(20)

    def reiniciar_lobby(self):
        if self.lobby:
            for skt in self.sockets.keys():
                self.iniciar_lobby(skt, "")
                QThread.msleep(20)

    def recibir_mensajes(self, msg):
        mensaje = loads(desencriptar(decodificar(msg)))
        if mensaje.tipo == "comenzar":
            primero = choice(self.nombres)
            lista = self.nombres.copy()
            lista.remove(primero)
            lista.insert(0, primero)
            penultimo = lista[1]
            segundo = lista[3]
            self.orden = lista.copy()
            self.orden[1] = segundo
            self.orden[3] = penultimo
            print("Comenzando la partida")
            nombres_usuarios = ", ".join(self.nombres_usados)
            print(f"Jugadores conectados: {nombres_usuarios}")
            self.vidas = parametro_json("NUMERO_VIDAS")
            lista.append(str(self.vidas))
            self.chat_management(Mensaje("comenzar", lista, ""))
            QThread.msleep(20)
            self.lobby = False
            self.inicio_partida()
            self.chat_management(Mensaje("turno", self.orden[0], ""))
            self.verificar_bot()
        elif mensaje.tipo == "anunciar" and mensaje.nombre == self.orden[0]:
            print(f"{mensaje.nombre} anuncia un {mensaje.info}")
            self.ultimo_anunciado = int(mensaje.info)
            self.chat_management(Mensaje("anunciar", mensaje.info, ""))
            QThread.msleep(20)
            self.ultima_jugada = Mensaje("anunciar", mensaje.info, mensaje.nombre)
            self.ultima_accion = Mensaje("anunciar", mensaje.info, mensaje.nombre)
            self.pasar_turno()
            QThread.msleep(20)
        elif mensaje.tipo == "pasar" and mensaje.nombre == self.orden[0]:
            print(f"{mensaje.nombre} prefiere pasar")
            self.chat_management(Mensaje("pasar", mensaje.info, ""))
            QThread.msleep(20)
            self.ultima_jugada = Mensaje("pasar", "", mensaje.nombre)
            self.ultima_accion = Mensaje("pasar", "", mensaje.nombre)
            QThread.msleep(20)
            self.pasar_turno()
        elif mensaje.tipo == "poder" and mensaje.nombre == self.orden[0]:
            if mensaje.info in self.nombres:
                dados = self.dados[mensaje.nombre]
                if (int(dados[0]) + int(dados[1])) == 3:
                    print(f"{mensaje.nombre} decide atacar a {mensaje.info}")
                    self.ultima_jugada = Mensaje("poder", "", mensaje.nombre)
                    self.ultima_accion = Mensaje("poder", "", mensaje.nombre)
                    self.perder_vidas(mensaje.info)
                    QThread.msleep(5000)
                    self.arreglar_orden(mensaje.info)
                    QThread.msleep(20)
                    self.reiniciar_partida()
                    QThread.msleep(20)
                    self.verificar_bot()
                elif (int(dados[0]) + int(dados[1])) == 4:
                    print(f"{mensaje.nombre} provoca un terremoto a {mensaje.info}")
                    vida_nueva = randint(1, int(parametro_json("NUMERO_VIDAS")))
                    self.ultima_jugada = Mensaje("poder", "", mensaje.nombre)
                    self.ultima_accion = Mensaje("poder", "", mensaje.nombre)
                    self.vidas[mensaje.info] = (vida_nueva + 1)
                    QThread.msleep(20)
                    self.perder_vidas(mensaje.info)
                    QThread.msleep(500)
                    self.arreglar_orden(mensaje.info)
                    QThread.msleep(50)
                    self.reiniciar_partida()
                    QThread.msleep(20)
                    self.verificar_bot()
        elif mensaje.tipo == "cambiar" and mensaje.nombre == self.orden[0]:
            if self.ultima_accion.tipo != "cambiar" and self.ultima_accion.nombre !=mensaje.nombre:
                print(f"{mensaje.nombre} acaba de cambiar sus dados")
                dado_1 = randint(1, 6)
                dado_2 = randint(1, 6)
                nuevos_dados = [dado_1, dado_2]
                self.dados[mensaje.nombre] = nuevos_dados
                self.chat_management(Mensaje("dados", self.dados, ""))
                QThread.msleep(20)
                self.ultima_accion = Mensaje("cambiar", "", mensaje.nombre)
        elif mensaje.tipo == "dudar" and mensaje.nombre == self.orden[0]:
            if self.ultima_accion.tipo not in ["", "poder", "dudar", "cambiar"]:
                QThread.msleep(20)
                self.chat_management(Mensaje("dudar", self.dados, self.nombres))
                QThread.msleep(300)
                print(f"{mensaje.nombre} duda a {self.ultima_jugada.nombre}")
                if self.ultima_jugada.tipo == "anunciar":
                    dados = self.dados[self.ultima_jugada.nombre]
                    if int(self.ultima_jugada.info) > (int(dados[0]) + int(dados[1])):
                        self.perder_vidas(self.ultima_jugada.nombre)
                        self.arreglar_orden(self.ultima_jugada.nombre)
                    else:
                        self.perder_vidas(mensaje.nombre)
                        self.arreglar_orden(mensaje.nombre)
                elif self.ultima_jugada.tipo == "pasar":
                    dados = self.dados[self.ultima_jugada.nombre]
                    if int(parametro_json("VALOR_PASO")) != (int(dados[0]) + int(dados[1])):
                        self.perder_vidas(self.ultima_jugada.nombre)
                        self.arreglar_orden(self.ultima_jugada.nombre)
                    else:
                        self.perder_vidas(mensaje.nombre)
                        self.arreglar_orden(mensaje.nombre)
                self.ultima_jugada = Mensaje("dudar", "", mensaje.nombre)
                self.ultima_accion = Mensaje("dudar", "", mensaje.nombre)
                self.reiniciar_partida()
                QThread.msleep(20)
                self.verificar_bot()

    def send(self, msg, sock):
        mensaje = codificar(encriptar(dumps(msg)))
        sock.send(mensaje)

    def inicio_partida(self):
        numeros = []
        for j in self.nombres:
            if j not in self.nombres_usados:
                self.desconectados.append(j)
        for i in range(8):
            numero = randint(1, 6)
            numeros.append(numero)
        self.dados = {}
        self.vidas = {}
        for i in range(4):
            self.dados[self.nombres[i]] = [int(numeros.pop(0)), int(numeros.pop(0))]
            self.vidas[self.nombres[i]] = int(parametro_json("NUMERO_VIDAS"))
        self.chat_management(Mensaje("dados", self.dados.copy(), ""))

    def jugar_bot(self, nombre):
        if random() < parametro_json("PROB_DUDAR"):
            mensaje = Mensaje("dudar", "", nombre)
            self.recibir_mensajes(codificar(encriptar(dumps(mensaje))))
            QThread.msleep(3000)
        else:
            mensaje = Mensaje("cambiar", "", nombre)
            self.recibir_mensajes(codificar(encriptar(dumps(mensaje))))
            QThread.msleep(3000)
            if random() < parametro_json("PROB_ANUNCIAR"):
                numero = randint(self.ultimo_anunciado, 12)
                if numero == 12:
                    mensaje = Mensaje("pasar", "", nombre)
                    self.recibir_mensajes(codificar(encriptar(dumps(mensaje))))
                else:
                    mensaje = Mensaje("anunciar", numero, nombre)
                    self.recibir_mensajes(codificar(encriptar(dumps(mensaje))))
            else:
                mensaje = Mensaje("pasar", "", nombre)
                self.recibir_mensajes(codificar(encriptar(dumps(mensaje))))

    def verificar_bot(self):
        if self.orden[0] in self.desconectados:
            self.jugar_bot(self.orden[0])

    def pasar_turno(self):
        ultimo = self.orden.pop(0)
        self.orden.append(ultimo)
        QThread.msleep(20)
        self.chat_management(Mensaje("turno", self.orden[0], ""))
        QThread.msleep(20)
        print(f"comenzo el turno de {self.orden[0]}")
        QThread.msleep(20)
        self.verificar_bot()

    def arreglar_orden(self, nombre):
        if nombre in self.orden:
            while self.orden[0] != nombre:
                ultimo = self.orden.pop(0)
                self.orden.append(ultimo)
            self.chat_management(Mensaje("turno", self.orden[0], ""))

    def perder_vidas(self, nombre):
        self.vidas[nombre] -= 1
        QThread.msleep(20)
        self.chat_management(Mensaje("vidas", self.vidas, self.nombres))
        QThread.msleep(20)
        print(f"{nombre} acaba de perder una vida, le quedan {self.vidas[nombre]}")
        if self.vidas[nombre] == 0:
            self.orden.remove(nombre)
            print(f"{nombre} acaba de perder su ultima vida, perdio el juego")
            if nombre not in self.desconectados:
                self.chat_management(Mensaje("perder", "", nombre))
            if len(self.orden) == 1:
                print(f"{self.orden[0]} acaba de ganar el juego")
                if nombre not in self.desconectados:
                    self.chat_management(Mensaje("ganar", "", nombre))

    def reiniciar_partida(self):
        self.chat_management(Mensaje("tapar", "", ""))
        self.ultimo_anunciado = 0
        self.chat_management(Mensaje("anunciar", 0, ""))
        QThread.msleep(100)
        numeros = []
        for i in range(8):
            numero = randint(1, 6)
            numeros.append(numero)
        self.dados = {}
        for i in range(4):
            self.dados[self.nombres[i]] = [int(numeros.pop(0)), int(numeros.pop(0))]
        QThread.msleep(100)
        self.chat_management(Mensaje("dados", self.dados.copy(), ""))
        QThread.msleep(500)
