from backend import Luigi, Borde, Vertical, Horizontal, Star, Rock, Fuego, Pared
from PyQt5.QtWidgets import QMainWindow, QWidget, QComboBox, QLabel, QPushButton, QDialogButtonBox
from PyQt5.QtWidgets import QHBoxLayout, QApplication, QVBoxLayout, QLineEdit, QShortcut, QDialog
from PyQt5.QtCore import QEvent, QObject, Qt, pyqtSignal, QTimer, QUrl
from PyQt5.QtGui import QKeySequence
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from parametros import TIEMPO_CUENTA_REGRESIVA, CANTIDAD_VIDAS, MULTIPLICADOR_PUNTAJE
from os import path, listdir
import sys


class VentanaJuego(QWidget):

    senal_cerrar_inicio = pyqtSignal()
    senal_W = pyqtSignal()
    senal_A = pyqtSignal()
    senal_S = pyqtSignal()
    senal_D = pyqtSignal()
    senal_P = pyqtSignal()
    senal_G = pyqtSignal()
    senal_K = pyqtSignal()
    senal_I = pyqtSignal()
    senal_L = pyqtSignal()
    senal_N = pyqtSignal()
    senal_F = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(200, 200, 520, 600)
        self.setWindowTitle("DCCazaFantasmas")
        self.time = TIEMPO_CUENTA_REGRESIVA
        self.vidas = CANTIDAD_VIDAS
        self.setStyleSheet("background-color: black;")

        self.temporizador = QTimer()
        self.temporizador.setInterval(1000)
        self.temporizador.timeout.connect(self.paso_1_seg)

        self.layout_grande = QHBoxLayout()
        layout_timer = QVBoxLayout()

        self.boton_pausar = QPushButton("Pausar", self)
        self.boton_pausar.setMaximumSize(110, 60)
        self.boton_pausar.setStyleSheet("border: 3px solid grey;")
        self.boton_exit = QPushButton("Salir", self)
        self.boton_exit.setMaximumSize(110, 60)
        self.boton_exit.setStyleSheet("border: 3px solid grey;")
        self.label_tiempo = QLabel(f"Tiempo: {self.time} seg")
        self.label_tiempo.setMaximumSize(110, 50)
        self.label_vida = QLabel(f"Vidas: {self.vidas}")
        self.label_vida.setMaximumSize(110, 50)
        self.boton_pausar.clicked.connect(self.pausar_tiempo)
        self.boton_exit.clicked.connect(exit)

        layout_timer.addWidget(self.label_tiempo)
        layout_timer.addWidget(self.label_vida)
        layout_timer.addWidget(self.boton_pausar)
        layout_timer.addWidget(self.boton_exit)

        self.layout_grande.addLayout(layout_timer)

    def paso_1_seg(self):
        if self.mapa.cheatcode_infinito:
            if self.time > 0:
                self.time -= 1
                self.label_tiempo.setText(f"Tiempo: {self.time} seg")
            if self.time == 0:
                self.pausar_tiempo()
                self.acabar_tiempo()

    def pausar_tiempo(self):
        if self.boton_pausar.text() == "Resumir":
            self.boton_pausar.setText("Pausar")
            if self.mapa.cheatcode_infinito:
                self.temporizador.start()
        else:
            self.boton_pausar.setText("Resumir")
            if self.mapa.cheatcode_infinito:
                self.temporizador.stop()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W and not event.isAutoRepeat():
            self.mapa.press_w()
        elif event.key() == Qt.Key_A and not event.isAutoRepeat():
            self.mapa.press_a()
        elif event.key() == Qt.Key_S and not event.isAutoRepeat():
            self.mapa.press_s()
        elif event.key() == Qt.Key_D and not event.isAutoRepeat():
            self.mapa.press_d()
        elif event.key() == Qt.Key_P and not event.isAutoRepeat():
            if self.mapa.cheatcode_infinito:
                self.pausar_tiempo()
            self.mapa.press_p()
        elif event.key() == Qt.Key_G and not event.isAutoRepeat():
            self.mapa.press_g()
            self.ganar_partida()
        elif event.key() == Qt.Key_K and not event.isAutoRepeat():
            self.mapa.press_k()
        elif event.key() == Qt.Key_I and not event.isAutoRepeat():
            self.mapa.press_i()
        elif event.key() == Qt.Key_L and not event.isAutoRepeat():
            self.mapa.press_l()
        elif event.key() == Qt.Key_N and not event.isAutoRepeat():
            self.mapa.press_n()
        elif event.key() == Qt.Key_F and not event.isAutoRepeat():
            self.mapa.press_f()

    def iniciar_mapa(self, texto):
        ruta = path.join("mapas", texto)
        mapa_txt = open(ruta, "r")
        lineas = mapa_txt.readlines()
        for i in lineas:
            i = i.strip("\n")
        self.lineas = lineas
        self.mapa = Mapa()
        self.mapa.crear_mapa(lineas)
        self.mapa.setParent(self)
        self.layout_grande.addWidget(self.mapa)
        self.setLayout(self.layout_grande)
        self.senal_cerrar_inicio.emit()
        self.show()
        self.temporizador.start()

    def iniciar_mapa_constructor(self, lineas):
        self.lineas = lineas
        self.mapa = Mapa()
        self.mapa.setParent(self)
        self.mapa.crear_mapa(lineas)
        self.layout_grande.addWidget(self.mapa)
        self.setLayout(self.layout_grande)
        self.senal_cerrar_inicio.emit()
        self.show()
        self.temporizador.start()

    def perder_vidas(self):
        if self.mapa.cheatcode_infinito:
            self.vidas -= 1
        if self.vidas <= 0:
            reproductor = QMediaPlayer()
            ruta = path.abspath(path.join("sounds", "gameOver.wav"))
            audio = QMediaContent(QUrl.fromLocalFile(ruta))
            reproductor.setMedia(audio)
            reproductor.play()
            self.box = QDialog()
            self.box.setWindowTitle("PERDISTE")
            layout = QHBoxLayout()
            boton_jugar = QPushButton("Jugar de nuevo")
            boton_jugar.clicked.connect(self.jugar_nueva_partida)
            boton_salir = QPushButton("Salir")
            boton_salir.clicked.connect(exit)
            layout.addWidget(boton_jugar)
            layout.addWidget(boton_salir)
            self.box.setLayout(layout)
            self.box.exec()
        else:
            self.pausar_tiempo()
            self.reiniciar = VentanaJuego()
            self.reiniciar.vidas = self.vidas
            self.reiniciar.time = self.time
            self.reiniciar.nombre = self.nombre
            self.reiniciar.label_vida.setText(f"Vidas: {self.reiniciar.vidas}")
            self.reiniciar.iniciar_mapa_constructor(self.lineas)
            self.reiniciar.mapa.cheatcode_infinito = self.mapa.cheatcode_infinito
            if not self.mapa.cheatcode_infinito:
                self.reiniciar.pausar_tiempo()
                self.reiniciar.label_tiempo.setText(f"Tiempo: {self.reiniciar.time} seg")
            self.reiniciar.show()
            self.hide()

    def jugar_nueva_partida(self):
        self.reiniciar = VentanaJuego()
        self.reiniciar.iniciar_mapa_constructor(self.lineas)
        self.reiniciar.nombre = self.nombre
        if not self.mapa.cheatcode_infinito:
            self.reiniciar.mapa.hack_vidas_infinitas()
        self.box.hide()
        self.hide()

    def acabar_tiempo(self):
        reproductor = QMediaPlayer()
        ruta = path.abspath(path.join("sounds", "gameOver.wav"))
        audio = QMediaContent(QUrl.fromLocalFile(ruta))
        reproductor.setMedia(audio)
        reproductor.play()
        self.box = QDialog()
        self.box.setWindowTitle("PERDISTE")
        layout = QHBoxLayout()
        boton_jugar = QPushButton("Jugar de nuevo")
        boton_jugar.clicked.connect(self.jugar_nueva_partida)
        boton_salir = QPushButton("Salir")
        boton_salir.clicked.connect(exit)
        layout.addWidget(boton_jugar)
        layout.addWidget(boton_salir)
        self.box.setLayout(layout)
        self.box.exec()

    def ganar_partida(self):
        self.pausar_tiempo()
        reproductor = QMediaPlayer()
        ruta = path.abspath(path.join("sounds", "stageClear.wav"))
        audio = QMediaContent(QUrl.fromLocalFile(ruta))
        reproductor.setMedia(audio)
        reproductor.play()
        self.box = QDialog()
        self.box.setWindowTitle("GANASTE")
        layout = QVBoxLayout()
        nombre = QLabel()
        nombre.setText(f"Nombre: {self.nombre}")
        puntaje_final = QLabel()
        if (CANTIDAD_VIDAS - self.vidas) != 0:
            puntaje = str((self.time * MULTIPLICADOR_PUNTAJE) / (CANTIDAD_VIDAS - self.vidas))
        else:
            puntaje = str((self.time * MULTIPLICADOR_PUNTAJE))
        puntaje_final.setText(f"puntaje: {puntaje}")
        boton_jugar = QPushButton("Jugar de nuevo")
        boton_jugar.clicked.connect(self.jugar_nueva_partida)
        boton_salir = QPushButton("Salir")
        boton_salir.clicked.connect(exit)
        layout.addWidget(nombre)
        layout.addWidget(puntaje_final)
        layout.addWidget(boton_jugar)
        layout.addWidget(boton_salir)
        self.box.setLayout(layout)
        self.box.exec()

    def guardar_nombre(self, texto):
        self.nombre = texto


class Mapa(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(200, 200, 352, 512)
        self.setStyleSheet("background-color: black;")
        self.tres_teclas = []
        self.lista_objetos = ["F", "L", "H", "V", "S", "R", "P"]
        self.lista_creados = []
        self.playing = True
        self.cheatcode_infinito = True

        for i in range(11):
            for j in range(16):
                if i == 0 or j == 0 or i == 10 or j == 15:
                    borde = Borde()
                    borde.setParent(self)
                    borde.move(i*32, j*32)

    def crear_mapa(self, txt):
        for objeto in self.lista_objetos:
            for i in range(9):
                for j in range(14):
                    if txt[j][i] == objeto:
                        if objeto == "F":
                            item = Fuego()
                            item.setParent(self)
                            item.move(32 * (i + 1), 32 * (j + 1))
                            self.lista_creados.append(item)
                        elif objeto == "L":
                            self.luigi = Luigi()
                            self.luigi.setParent(self)
                            self.luigi.move(32 * (i + 1), 32 * (j + 1))
                        elif objeto == "H":
                            item = Horizontal()
                            item.setParent(self)
                            item.move(32 * (i + 1), 32 * (j + 1))
                            self.lista_creados.append(item)
                        elif objeto == "V":
                            item = Vertical()
                            item.setParent(self)
                            item.move(32 * (i + 1), 32 * (j + 1))
                            self.lista_creados.append(item)
                        elif objeto == "S":
                            item = Star()
                            item.setParent(self)
                            item.move(32 * (i + 1), 32 * (j + 1))
                            self.lista_creados.append(item)
                        elif objeto == "R":
                            item = Rock()
                            item.setParent(self)
                            item.move(32 * (i + 1), 32 * (j + 1))
                            self.lista_creados.append(item)
                        elif objeto == "P":
                            item = Pared()
                            item.setParent(self)
                            item.move(32 * (i + 1), 32 * (j + 1))
                            self.lista_creados.append(item)

    def cambiar_teclas(self, tecla):
        self.tres_teclas.append(tecla)
        if len(self.tres_teclas) > 3:
            while len(self.tres_teclas) > 3:
                self.tres_teclas.pop(0)
        if self.tres_teclas == ["K", "I", "L"]:
            self.eliminar_villanos()
        elif self.tres_teclas == ["I", "N", "F"]:
            self.hack_vidas_infinitas()

    def press_w(self):
        if self.playing:
            self.luigi.sprites_arriba()
            self.cambiar_teclas("W")

    def press_a(self):
        if self.playing:
            self.luigi.sprites_izquierda()
            self.cambiar_teclas("A")

    def press_s(self):
        if self.playing:
            self.luigi.sprites_abajo()
            self.cambiar_teclas("S")

    def press_d(self):
        if self.playing:
            self.luigi.sprites_derecha()
            self.cambiar_teclas("D")

    def press_p(self):
        self.cambiar_teclas("P")
        self.playing = not self.playing
        for i in self.lista_creados:
            if i.accessibleName() == "horizontal" or i.accessibleName() == "vertical":
                i.pausar()

    def press_g(self):
        if self.childAt(self.luigi.x(), self.luigi.y()).accessibleName() == "star" and self.playing:
            self.cambiar_teclas("G")

    def press_k(self):
        self.cambiar_teclas("K")

    def press_i(self):
        self.cambiar_teclas("I")

    def press_l(self):
        self.cambiar_teclas("L")

    def press_n(self):
        self.cambiar_teclas("N")

    def press_f(self):
        self.cambiar_teclas("F")

    def eliminar_villanos(self):
        for i in self.lista_creados:
            if i.accessibleName() == "horizontal" or i.accessibleName() == "vertical":
                i.hide()

    def hack_vidas_infinitas(self):
        self.parent().pausar_tiempo()
        self.cheatcode_infinito = False
