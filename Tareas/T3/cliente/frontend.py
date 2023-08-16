from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout, QMessageBox, QLineEdit, QSpacerItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from functions import parametro_json
from os import path


class VentanaInicio(QMainWindow):

    comenzar_signal = pyqtSignal()
    anunciar_valor = pyqtSignal(str)
    senal_pasar = pyqtSignal()
    senal_poder = pyqtSignal(str)
    senal_cambiar = pyqtSignal()
    senal_dudar = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 900, 900)
        self.setWindowTitle("DCCachos")
        self.background = QLabel()
        self.background.setScaledContents(True)
        self.setCentralWidget(self.background)
        self.numero_anunciado = 0
        fondo = path.join(*parametro_json("FONDO_INICIO"))
        self.setStyleSheet(
            "QMainWindow {"
            f"   background-image: url({fondo});"
            "   background-position: center;"
            "}"
        )
        self.iniciar_ventana()

    def iniciar_ventana(self):

        self.sala_espera = QLabel("SALA DE ESPERA", self)
        self.sala_espera.setAlignment(Qt.AlignCenter)
        self.sala_espera.setStyleSheet("font-size: 24px;font-weight: bold")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.sala_espera)

        self.layout_jugadores = QHBoxLayout()

        self.comenzar = QPushButton("Comenzar", self)
        self.comenzar.clicked.connect(self.boton_comenzar)
        self.salir = QPushButton("Salir", self)
        self.salir.clicked.connect(exit)

        self.layout.addLayout(self.layout_jugadores)
        self.layout.addWidget(self.comenzar)
        self.layout.addWidget(self.salir)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        self.show()

    def crear_jugador(self, nombre):
        icono_jugador = QLabel(self)
        caja = QVBoxLayout()
        foto = path.join(*parametro_json("USER_PROFILE"))
        icono_jugador.setPixmap(QPixmap(foto).scaled(150, 150))
        caja.addWidget(icono_jugador)
        name_box = QLabel(nombre, self)
        caja.addWidget(name_box)
        self.layout_jugadores.addLayout(caja)
        self.layout_jugadores.update()

    def reiniciar_lobby(self):
        print("reiniciar")
        self.iniciar_ventana()

    def desconectar(self, msg):
        self.box = QMessageBox()
        if msg == "sala":
            print("sala llena")
            text = "En este momento la sala esta llena, intentelo mas tarde"
            self.box.setText(text)
        elif msg == "juego":
            print("partida en juego")
            text = "En este momento hay una partida en juego, intentelo mas tarde"
            self.box.setText(text)
        self.box.exec()

    def ventana_juego(self, lista):
        self.setGeometry(0, 0, 1270, 720)
        datos = lista.copy()
        vidas = datos.pop()
        fondo = path.join(*parametro_json("FONDO_JUEGO"))
        self.setStyleSheet(
            "QMainWindow {"
            f"   background-image: url({fondo});"
            "   background-position: center;"
            "}"
        )
        # dados
        self.icono = QPixmap(path.join(*parametro_json("USER_PROFILE"))).scaled(100, 100)
        self.dados_default = QPixmap(path.join(*parametro_json("DICE_LOGO"))).scaled(50, 50)
        self.dado_1 = QPixmap(path.join(*parametro_json("DICE_1"))).scaled(50, 50)
        self.dado_2 = QPixmap(path.join(*parametro_json("DICE_2"))).scaled(50, 50)
        self.dado_3 = QPixmap(path.join(*parametro_json("DICE_3"))).scaled(50, 50)
        self.dado_4 = QPixmap(path.join(*parametro_json("DICE_4"))).scaled(50, 50)
        self.dado_5 = QPixmap(path.join(*parametro_json("DICE_5"))).scaled(50, 50)
        self.dado_6 = QPixmap(path.join(*parametro_json("DICE_6"))).scaled(50, 50)
        extra = [self.dado_4, self.dado_5, self.dado_6]
        self.pixmap_dados = [self.dado_1, self.dado_2, self.dado_3]
        self.pixmap_dados.extend(extra)
        # status bar
        self.borrar_layout(self.layout)
        self.mayor_anunciado = QLabel("Numero mayor anunciado: 0")
        self.turno_anterior = QLabel("Turno anterior fue de Nadie")
        self.turno_actual = QLabel("Turno de Jugador")
        self.numero_turno = QLabel("Numero de Turno: 0")
        self.layout_status_bar = QHBoxLayout()
        self.turno = QVBoxLayout()
        self.turno.addWidget(self.turno_actual)
        self.turno.addWidget(self.turno_anterior)
        self.turno.setAlignment(Qt.AlignCenter)
        self.layout_status_bar.addWidget(self.mayor_anunciado)
        self.layout_status_bar.addLayout(self.turno)
        self.layout_status_bar.addWidget(self.numero_turno)
        self.layout_status_bar.setAlignment(Qt.AlignTop)

        # central widget
        self.layout_jugador_2 = QHBoxLayout()
        self.layout_h_jugador_2 = QHBoxLayout()
        self.layout_v_jugador_2 = QVBoxLayout()
        self.vidas_jugador_2 = QLabel(text=vidas)
        self.nombre_jugador_2 = QLabel(text=datos[1])
        self.nombre_jugador_2.setAlignment(Qt.AlignCenter)
        self.user_profile_2 = QLabel()
        self.user_profile_2.setPixmap(self.icono)
        self.layout_dados_2 = QVBoxLayout()
        self.dado_1_jugador_2 = QLabel()
        self.dado_2_jugador_2 = QLabel()
        self.dado_1_jugador_2.setPixmap(self.dados_default)
        self.dado_2_jugador_2.setPixmap(self.dados_default)
        self.layout_h_jugador_2.addWidget(self.vidas_jugador_2)
        self.layout_h_jugador_2.addWidget(self.user_profile_2)
        self.layout_v_jugador_2.addLayout(self.layout_h_jugador_2)
        self.layout_v_jugador_2.addWidget(self.nombre_jugador_2)
        self.layout_dados_2.addWidget(self.dado_1_jugador_2)
        self.layout_dados_2.addWidget(self.dado_2_jugador_2)
        self.layout_jugador_2.addLayout(self.layout_v_jugador_2)
        self.layout_jugador_2.addLayout(self.layout_dados_2)

        self.layout_jugador_1 = QHBoxLayout()
        self.layout_h_jugador_1 = QHBoxLayout()
        self.layout_v_jugador_1 = QVBoxLayout()
        self.vidas_jugador_1 = QLabel(text=vidas)
        self.nombre_jugador_1 = QLabel(text=datos[0])
        self.nombre_jugador_1.setAlignment(Qt.AlignCenter)
        self.user_profile_1 = QLabel()
        self.user_profile_1.setPixmap(self.icono)
        self.layout_dados_1 = QVBoxLayout()
        self.dado_1_jugador_1 = QLabel()
        self.dado_2_jugador_1 = QLabel()
        self.dado_1_jugador_1.setPixmap(self.dados_default)
        self.dado_2_jugador_1.setPixmap(self.dados_default)
        self.layout_h_jugador_1.addWidget(self.vidas_jugador_1)
        self.layout_h_jugador_1.addWidget(self.user_profile_1)
        self.layout_v_jugador_1.addLayout(self.layout_h_jugador_1)
        self.layout_v_jugador_1.addWidget(self.nombre_jugador_1)
        self.layout_dados_1.addWidget(self.dado_1_jugador_1)
        self.layout_dados_1.addWidget(self.dado_2_jugador_1)
        self.layout_jugador_1.addLayout(self.layout_v_jugador_1)
        self.layout_jugador_1.addLayout(self.layout_dados_1)
        self.layout_jugador_1.setAlignment(Qt.AlignCenter)

        self.layout_jugador_3 = QHBoxLayout()
        self.layout_h_jugador_3 = QHBoxLayout()
        self.layout_v_jugador_3 = QVBoxLayout()
        self.vidas_jugador_3 = QLabel(text=vidas)
        self.nombre_jugador_3 = QLabel(text=datos[2])
        self.nombre_jugador_3.setAlignment(Qt.AlignCenter)
        self.user_profile_3 = QLabel()
        self.user_profile_3.setPixmap(self.icono)
        self.layout_dados_3 = QVBoxLayout()
        self.dado_1_jugador_3 = QLabel()
        self.dado_2_jugador_3 = QLabel()
        self.dado_1_jugador_3.setPixmap(self.dados_default)
        self.dado_2_jugador_3.setPixmap(self.dados_default)
        self.layout_h_jugador_3.addWidget(self.vidas_jugador_3)
        self.layout_h_jugador_3.addWidget(self.user_profile_3)
        self.layout_v_jugador_3.addLayout(self.layout_h_jugador_3)
        self.layout_v_jugador_3.addWidget(self.nombre_jugador_3)
        self.layout_dados_3.addWidget(self.dado_1_jugador_3)
        self.layout_dados_3.addWidget(self.dado_2_jugador_3)
        self.layout_jugador_3.addLayout(self.layout_v_jugador_3)
        self.layout_jugador_3.addLayout(self.layout_dados_3)
        self.layout_jugador_3.setAlignment(Qt.AlignCenter)

        self.layout_jugador_4 = QHBoxLayout()
        self.layout_jugador_4.setSpacing(0)
        self.layout_h_jugador_4 = QHBoxLayout()
        self.layout_v_jugador_4 = QVBoxLayout()
        self.vidas_jugador_4 = QLabel(text=vidas)
        self.nombre_jugador_4 = QLabel(text=datos[3])
        self.nombre_jugador_4.setAlignment(Qt.AlignCenter)
        self.user_profile_4 = QLabel()
        self.user_profile_4.setPixmap(self.icono)
        self.layout_dados_4 = QVBoxLayout()
        self.dado_1_jugador_4 = QLabel()
        self.dado_2_jugador_4 = QLabel()
        self.dado_1_jugador_4.setPixmap(self.dados_default)
        self.dado_2_jugador_4.setPixmap(self.dados_default)
        self.layout_h_jugador_4.addWidget(self.user_profile_4)
        self.layout_h_jugador_4.addWidget(self.vidas_jugador_4)
        self.layout_v_jugador_4.addLayout(self.layout_h_jugador_4)
        self.layout_v_jugador_4.addWidget(self.nombre_jugador_4)
        self.layout_dados_4.addWidget(self.dado_1_jugador_4)
        self.layout_dados_4.addWidget(self.dado_2_jugador_4)
        self.layout_jugador_4.addLayout(self.layout_dados_4)
        self.layout_jugador_4.addLayout(self.layout_v_jugador_4)

        self.layout_jugadores_2_4 = QHBoxLayout()
        self.layout_jugadores_2_4.addLayout(self.layout_jugador_2)
        self.layout_jugadores_2_4.addStretch()
        self.layout_jugadores_2_4.addLayout(self.layout_jugador_4)

        self.layout_jugador_1_botones = QHBoxLayout()
        self.espacio = QSpacerItem(520, 50)
        self.layout_jugador_1_botones.addItem(self.espacio)
        self.layout_jugador_1_botones.addLayout(self.layout_jugador_1)

        self.boton_anunciar = QPushButton("Anunciar Valor", self)
        self.boton_anunciar.clicked.connect(self.anunciar)
        self.anunciar_texto = QLineEdit(self)
        self.anunciar_texto.setPlaceholderText("Ingresar valor aqui")
        self.boton_pasar = QPushButton("Pasar Turno", self)
        self.boton_pasar.clicked.connect(self.senal_pasar)
        self.boton_poder = QPushButton("Usar Poder", self)
        self.boton_poder.clicked.connect(self.poder)
        self.boton_cambiar = QPushButton("Cambiar Dados", self)
        self.boton_cambiar.clicked.connect(self.senal_cambiar)
        self.boton_dudar = QPushButton("Dudar", self)
        self.boton_dudar.clicked.connect(self.senal_dudar)
        self.dirigir_poder = QLineEdit(self)
        self.dirigir_poder.setPlaceholderText("Destinatario Poder")

        self.box_botones = QHBoxLayout()
        self.columna_1 = QVBoxLayout()
        self.columna_1.addWidget(self.boton_anunciar)
        self.columna_1.addWidget(self.boton_pasar)
        self.columna_1.addWidget(self.boton_poder)
        self.columna_1.addWidget(self.dirigir_poder)
        self.columna_1.setSpacing(0)
        self.columna_2 = QVBoxLayout()
        self.columna_2.addWidget(self.anunciar_texto)
        self.columna_2.addWidget(self.boton_cambiar)
        self.columna_2.addWidget(self.boton_dudar)
        self.columna_2.setSpacing(0)
        self.box_botones.addLayout(self.columna_1)
        self.box_botones.addLayout(self.columna_2)
        self.box_botones.setSpacing(0)
        self.layout_jugador_1_botones.addStretch()
        self.layout_jugador_1_botones.addLayout(self.box_botones)

        self.layout.addLayout(self.layout_status_bar)
        self.layout.addLayout(self.layout_jugador_3)
        self.layout.addLayout(self.layout_jugadores_2_4)
        self.layout.addLayout(self.layout_jugador_1_botones)

    def boton_comenzar(self):
        self.comenzar_signal.emit()

    def anunciar(self):
        numero = self.anunciar_texto.text()
        if numero.isnumeric() and len(numero) > 0:
            if int(numero) > self.numero_anunciado:
                self.anunciar_valor.emit(self.anunciar_texto.text())

    def poder(self):
        destinatario = self.dirigir_poder.text()
        print(destinatario)
        self.senal_poder.emit(destinatario)

    def servidor_cerrado(self):
        self.box = QMessageBox()
        text = "La conexion con el servidor se ha perdido, cierre el programa por favor"
        self.box.setText(text)
        self.box.exec()

    def borrar_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            sublayout = item.layout()
            if widget:
                widget.deleteLater()
            elif sublayout:
                self.borrar_layout(sublayout)
                sublayout.deleteLater()

    def recibir_dados(self, dados):
        nombre = dados[0]
        if self.nombre_jugador_1.text() == nombre:
            self.dado_1_jugador_1.setPixmap(self.pixmap_dados[dados[1]-1])
            self.dado_2_jugador_1.setPixmap(self.pixmap_dados[dados[2]-1])
            self.layout_jugador_1.update()
        elif self.nombre_jugador_2.text() == nombre:
            self.dado_1_jugador_2.setPixmap(self.pixmap_dados[dados[1]-1])
            self.dado_2_jugador_2.setPixmap(self.pixmap_dados[dados[2]-1])
            self.layout_jugador_2.update()
        elif self.nombre_jugador_3.text() == nombre:
            self.dado_1_jugador_3.setPixmap(self.pixmap_dados[dados[1]-1])
            self.dado_2_jugador_3.setPixmap(self.pixmap_dados[dados[2]-1])
            self.layout_jugador_3.update()
        elif self.nombre_jugador_4.text() == nombre:
            self.dado_1_jugador_4.setPixmap(self.pixmap_dados[dados[1]-1])
            self.dado_2_jugador_4.setPixmap(self.pixmap_dados[dados[2]-1])
            self.layout_jugador_4.update()

    def actualizar_turno(self, nombre):
        anterior = self.turno_actual.text()
        lista = anterior.split(" ")
        self.turno_nombre = " ".join(lista[-2:])
        self.turno_anterior.setText(f"Turno anterior fue de {self.turno_nombre}")
        self.turno_actual.setText(f"Turno de {nombre}")
        numero = self.numero_turno.text().split(" ")[-1]
        numero = int(numero) + 1
        self.numero_turno.setText(f"Numero de Turno: {numero}")
        self.layout_status_bar.update()

    def cambiar_anunciar(self, anunciado):
        self.mayor_anunciado.setText(f"Numero mayor anunciado: {anunciado}")
        self.numero_anunciado = int(anunciado)

    def actualizar_vidas(self, lista):
        nombre = lista[0]
        if self.nombre_jugador_1.text() == nombre:
            self.vidas_jugador_1.setText(str(lista[1]))
            self.layout_jugador_1.update()
        elif self.nombre_jugador_2.text() == nombre:
            self.vidas_jugador_2.setText(str(lista[1]))
            self.layout_jugador_2.update()
        elif self.nombre_jugador_3.text() == nombre:
            self.vidas_jugador_3.setText(str(lista[1]))
            self.layout_jugador_3.update()
        elif self.nombre_jugador_4.text() == nombre:
            self.vidas_jugador_4.setText(str(lista[1]))
            self.layout_jugador_4.update()

    def tapar_dados(self):
        self.dado_1_jugador_1.setPixmap(self.dados_default)
        self.dado_2_jugador_1.setPixmap(self.dados_default)
        self.dado_1_jugador_2.setPixmap(self.dados_default)
        self.dado_2_jugador_2.setPixmap(self.dados_default)
        self.dado_1_jugador_3.setPixmap(self.dados_default)
        self.dado_2_jugador_3.setPixmap(self.dados_default)
        self.dado_1_jugador_4.setPixmap(self.dados_default)
        self.dado_2_jugador_4.setPixmap(self.dados_default)

    def perder(self):
        self.box = QMessageBox()
        text = "PERDISTE LA PARTIDA, POR FAVOR CIERRA EL PROGRAMA"
        self.box.setText(text)
        self.box.exec()

    def ganar(self):
        self.box = QMessageBox()
        text = "GANASTE LA PARTIDA, POR FAVOR CIERRA EL PROGRAMA"
        self.box.setText(text)
        self.box.exec()
