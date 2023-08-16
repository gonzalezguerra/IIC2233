import socket
import threading
from pickle import loads, dumps
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from functions import codificar, decodificar
from cripto import encriptar, desencriptar


class Mensaje:

    def __init__(self, tipo, info, nombre) -> None:
        self.tipo = tipo
        self.info = info
        self.nombre = nombre


class Cliente(QObject):

    update_lobby = pyqtSignal(str)
    reset_lobby = pyqtSignal()
    desconectar = pyqtSignal(str)
    servidor_off = pyqtSignal()
    comenzar_on = pyqtSignal(list)
    enviar_dados = pyqtSignal(list)
    enviar_turno = pyqtSignal(str)
    recibir_anunciar = pyqtSignal(str)
    enviar_vidas = pyqtSignal(list)
    senal_tapar = pyqtSignal()
    senal_perder = pyqtSignal()
    senal_ganar = pyqtSignal()

    def __init__(self, port, host):
        super().__init__()
        self.port = port
        self.host = host
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lobby = True
        self.connect_to_server()
        self.listen()

    def set_username(self, event):
        self.username = event

    def connect_to_server(self):
        self.socket_cliente.connect((self.host, self.port))
        print('Cliente conectado a servidor')

    def listen(self):
        thread = threading.Thread(target=self.listen_thread, daemon=True)
        thread.start()

    def listen_thread(self):
        while True:
            try:
                data = self.socket_cliente.recv(2**16)
                if len(data) == 0:
                    self.servidor_off.emit()
                    QThread.msleep(50)
                    break
                QThread.msleep(50)
                self.recibir_mensajes(data)
            except (ConnectionResetError, EOFError):
                print("servidor cerrado")
                self.servidor_off.emit()
                QThread.msleep(50)
                break

    def send(self, msg):
        self.socket_cliente.send(codificar(encriptar(dumps(msg))))

    def recibir_mensajes(self, msg):
        mensaje = loads(desencriptar(decodificar(msg)))
        if mensaje.tipo == "conexion":
            self.update_lobby.emit(mensaje.info)
        elif mensaje.tipo == "desconexion":
            if self.lobby:
                self.reset_lobby.emit()
        elif mensaje.tipo == "sala":
            self.desconectar.emit("sala")
        elif mensaje.tipo == "juego":
            self.desconectar.emit("juego")
        elif mensaje.tipo == "comenzar":
            self.comenzar_on.emit(mensaje.info)
            self.vidas = mensaje.info[4]
            self.lobby = False
        elif mensaje.tipo == "nombre":
            self.nombre = mensaje.info
        elif mensaje.tipo == "dados":
            self.dados = mensaje.info[self.nombre].copy()
            lista = self.dados.copy()
            lista.insert(0, self.nombre)
            self.enviar_dados.emit(lista)
        elif mensaje.tipo == "turno":
            self.enviar_turno.emit(mensaje.info)
        elif mensaje.tipo == "anunciar":
            self.recibir_anunciar.emit(str(mensaje.info))
        elif mensaje.tipo == "dudar":
            for i in mensaje.nombre:
                lista = mensaje.info[i].copy()
                lista.insert(0, i)
                self.enviar_dados.emit(lista)
                QThread.msleep(20)
        elif mensaje.tipo == "vidas":
            for i in mensaje.nombre:
                lista = [mensaje.info[i]]
                lista.insert(0, i)
                self.enviar_vidas.emit(lista)
                QThread.msleep(20)
        elif mensaje.tipo == "tapar":
            self.senal_tapar.emit()
        elif mensaje.tipo == "perder" and mensaje.nombre == self.nombre:
            self.senal_perder.emit()
        elif mensaje.tipo == "ganar" and mensaje.nombre == self.nombre:
            self.senal_ganar.emit()

    def enviar_anunciar(self, numero):
        self.send(Mensaje("anunciar", numero, self.nombre))

    def enviar_pasar(self):
        self.send(Mensaje("pasar", "", self.nombre))

    def enviar_poder(self, nombre):
        self.send(Mensaje("poder", nombre, self.nombre))

    def enviar_cambiar(self):
        self.send(Mensaje("cambiar", "", self.nombre))

    def enviar_dudar(self):
        self.send(Mensaje("dudar", "", self.nombre))

    def comenzar_partida(self):
        self.send(Mensaje("comenzar", "", ""))
