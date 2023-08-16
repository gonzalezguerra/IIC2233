from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QPushButton, QGridLayout
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from os import path, listdir
from parametros import ANCHO_GRILLA, LARGO_GRILLA, MIN_CARACTERES, MAX_CARACTERES
from parametros import TIEMPO_CUENTA_REGRESIVA, CANTIDAD_VIDAS
from parametros import MAXIMO_FANTASMAS_HORIZONTAL, MAXIMO_FANTASMAS_VERTICAL
from parametros import MAXIMO_PARED, MAXIMO_FUEGO, MAXIMO_ROCA
from backend import Luigi, Vertical, Horizontal, Fuego, Pared, Rock, Star
from frontend_juego import Mapa


class VentanaInicio(QWidget):
    senal_modo = pyqtSignal(str)
    senal_nombre = pyqtSignal(str)
    enviar_nombre = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(200, 200, 200, 300)
        self.setWindowTitle("Ventana de Inicio")
        self.background = QLabel(self)
        path_fondo = path.join('sprites', "Fondos", 'fondo_inicio.png')
        self.background.setPixmap(QPixmap(path_fondo).scaled(420, 480))
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap(path.join('sprites', "Elementos", 'logo.png')).scaled(365, 70))
        self.setStyleSheet("background-color: black;")

        self.selector_modo = QComboBox(self)
        self.selector_modo.setStyleSheet("border: 3px solid grey;")
        lista_mapas = listdir("mapas")
        lista_mapas.append("modo constructor")
        self.selector_modo.addItems(lista_mapas)

        self.boton_ingresar = QPushButton("Login", self)
        self.boton_ingresar.setStyleSheet("border: 3px solid grey;")
        self.nombre_usuario = QLineEdit("", self)
        self.nombre_usuario.setPlaceholderText("Nombre de usuario")
        self.nombre_usuario.setStyleSheet("border: 3px solid grey;")
        self.boton_salir = QPushButton("Salir", self)
        self.boton_salir.clicked.connect(exit)
        self.boton_salir.setStyleSheet("border: 3px solid grey;")

        self.background.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.logo.setAttribute(Qt.WA_TransparentForMouseEvents)

        # Creamos el layout de nuestra ventana y agregamos los elementos
        self.logo.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.logo)
        layout.addWidget(self.background)
        layout.addWidget(self.nombre_usuario)
        layout.addWidget(self.selector_modo)
        layout.addWidget(self.boton_ingresar)
        layout.addWidget(self.boton_salir)
        self.setLayout(layout)

        # Conectamos las señales de los elementos
        self.boton_ingresar.clicked.connect(self.revisar)

        self.show()

    def revisar(self) -> None:
        nombre = self.nombre_usuario.text()
        self.senal_nombre.emit(nombre)

    def revisar_mapa(self):
        modo = self.selector_modo.currentText()
        self.enviar_nombre.emit(self.nombre_usuario.text())
        self.senal_modo.emit(modo)

    def mostrar_pop_up(self, texto):
        mensaje = QMessageBox()
        mensaje.setWindowTitle("Error")
        if texto == "Alpha":
            mensaje.setText("El nombre tiene que contener solo caracteres alfanumericos")
        elif texto == "Caracteres":
            mensaje.setText(f"El nombre tiene que tener entre {MIN_CARACTERES} y {MAX_CARACTERES}")
        ventana = mensaje.exec()

    def cerrar_inicio(self):
        self.hide()


class VentanaConstructor(QWidget):

    senal_cerrar_inicio = pyqtSignal()
    senal_seleccionado = pyqtSignal(str)
    senal_boton_grid = pyqtSignal(int, int)
    senal_comenzar = pyqtSignal(list)
    enviar_nombre = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(200, 200, 500, 600)
        self.setWindowTitle("Constructor")
        self.ultimo_boton = ""
        self.luigis = 1
        self.vertical = MAXIMO_FANTASMAS_VERTICAL
        self.horizontal = MAXIMO_FANTASMAS_HORIZONTAL
        self.pared = MAXIMO_PARED
        self.roca = MAXIMO_ROCA
        self.fuego = MAXIMO_FUEGO
        self.star = 1
        self.mapa_txt = self.crear_mapa_txt()

        # Creación de botones
        foto_luigi = QPixmap(path.join("sprites", "Personajes", "luigi_front.png"))
        self.boton_luigi = QPushButton("(1)", self)
        icono = QIcon(foto_luigi)
        self.boton_luigi.setIcon(icono)
        self.boton_luigi.setIconSize(foto_luigi.size())
        self.boton_luigi.setStyleSheet("border: 3px solid grey;")
        self.boton_luigi.setFixedSize(80, 50)
        self.boton_luigi.clicked.connect(self.ultimo_boton_luigi)

        foto_fantasmav = QPixmap(path.join("sprites", "Personajes", "red_ghost_vertical_2.png"))
        self.boton_fantasmav = QPushButton(f"({MAXIMO_FANTASMAS_VERTICAL})", self)
        icono = QIcon(foto_fantasmav)
        self.boton_fantasmav.setIcon(icono)
        self.boton_fantasmav.setIconSize(foto_luigi.size())
        self.boton_fantasmav.setStyleSheet("border: 3px solid grey;")
        self.boton_fantasmav.setFixedSize(80, 50)
        self.boton_fantasmav.clicked.connect(self.ultimo_boton_vertical)

        foto_fantasmah = QPixmap(path.join("sprites", "Personajes", "white_ghost_rigth_2.png"))
        self.boton_fantasmah = QPushButton(f"({MAXIMO_FANTASMAS_HORIZONTAL})", self)
        icono = QIcon(foto_fantasmah)
        self.boton_fantasmah.setIcon(icono)
        self.boton_fantasmah.setIconSize(foto_fantasmah.size())
        self.boton_fantasmah.setStyleSheet("border: 3px solid grey;")
        self.boton_fantasmah.setFixedSize(80, 50)
        self.boton_fantasmah.clicked.connect(self.ultimo_boton_horizontal)

        foto_pared = QPixmap(path.join("sprites", "Elementos", "wall.png"))
        self.boton_pared = QPushButton(f"({MAXIMO_PARED})", self)
        icono = QIcon(foto_pared)
        self.boton_pared.setIcon(icono)
        self.boton_pared.setIconSize(foto_pared.size())
        self.boton_pared.setStyleSheet("border: 3px solid grey;")
        self.boton_pared.setFixedSize(80, 50)
        self.boton_pared.clicked.connect(self.ultimo_boton_pared)

        foto_roca = QPixmap(path.join("sprites", "Elementos", "rock.png"))
        self.boton_roca = QPushButton(f"({MAXIMO_ROCA})", self)
        icono = QIcon(foto_roca)
        self.boton_roca.setIcon(icono)
        self.boton_roca.setIconSize(foto_roca.size())
        self.boton_roca.setStyleSheet("border: 3px solid grey;")
        self.boton_roca.setFixedSize(80, 50)
        self.boton_roca.clicked.connect(self.ultimo_boton_roca)

        foto_fuego = QPixmap(path.join("sprites", "Elementos", "fire.png"))
        self.boton_fuego = QPushButton(f"({MAXIMO_FUEGO})", self)
        icono = QIcon(foto_fuego)
        self.boton_fuego.setIcon(icono)
        self.boton_fuego.setIconSize(foto_fuego.size())
        self.boton_fuego.setStyleSheet("border: 3px solid grey;")
        self.boton_fuego.setFixedSize(80, 50)
        self.boton_fuego.clicked.connect(self.ultimo_boton_fuego)

        foto_star = QPixmap(path.join("sprites", "Elementos", "osstar.png"))
        foto_star = foto_star.scaled(30, 30, Qt.KeepAspectRatio)
        self.boton_star = QPushButton("(1)", self)
        icono = QIcon(foto_star)
        self.boton_star.setIcon(icono)
        self.boton_star.setIconSize(foto_star.size())
        self.boton_star.setStyleSheet("border: 3px solid grey;")
        self.boton_star.setFixedSize(80, 50)
        self.boton_star.clicked.connect(self.ultimo_boton_star)

        self.selector_tipos = QComboBox(self)
        self.selector_tipos.addItems(["Todos", "Entidades", "Bloques"])
        self.selector_tipos.currentTextChanged.connect(self.cambiar_lista_objetos)
        self.senal_boton_grid.connect(self.cambiar_grid)

        self.boton_limpiar = QPushButton("Limpiar", self)
        self.boton_salir = QPushButton("Salir", self)
        self.boton_comenzar = QPushButton("Comenzar", self)

        self.boton_limpiar.clicked.connect(self.limpiar_mapa)
        self.boton_salir.clicked.connect(exit)
        self.boton_comenzar.clicked.connect(self.comenzar)

        layout_grande = QHBoxLayout()

        layout_botones = QVBoxLayout()
        layout_botones.addWidget(self.selector_tipos)
        layout_botones.addWidget(self.boton_luigi)
        layout_botones.addWidget(self.boton_fantasmav)
        layout_botones.addWidget(self.boton_fantasmah)
        layout_botones.addWidget(self.boton_pared)
        layout_botones.addWidget(self.boton_roca)
        layout_botones.addWidget(self.boton_fuego)
        layout_botones.addWidget(self.boton_star)
        layout_botones.addStretch(1)
        layout_botones.addWidget(self.boton_limpiar)
        layout_botones.addWidget(self.boton_comenzar)
        layout_botones.addWidget(self.boton_salir)

        layout_grande.addLayout(layout_botones)

        self.grid = QGridLayout()
        self.grid.setSpacing(1)
        self.grid.setContentsMargins(0, 0, 0, 0)

        for i in range(ANCHO_GRILLA):
            for j in range(LARGO_GRILLA):
                if i == 0 or i == 10 or j == 0 or j == 15:
                    foto_borde = QLabel()
                    relativo = path.join("sprites", "Elementos", "bordermap.png")
                    foto_borde.setPixmap(QPixmap(relativo))
                    foto_borde.setAlignment(Qt.AlignCenter)
                    self.grid.addWidget(foto_borde, j, i)
                else:
                    boton = QPushButton()
                    boton.setMinimumSize(45, 45)
                    boton.setMaximumSize(45, 45)
                    boton.clicked.connect(self.cambiar_grid)
                    self.grid.addWidget(boton, j, i)

        layout_grande.addLayout(self.grid)
        self.setLayout(layout_grande)

    def cambiar_lista_objetos(self):
        if self.selector_tipos.currentText() == "Entidades":
            self.boton_luigi.show()
            self.boton_fantasmav.show()
            self.boton_fantasmah.show()
            self.boton_pared.hide()
            self.boton_roca.hide()
            self.boton_fuego.hide()
            self.boton_star.hide()
        elif self.selector_tipos.currentText() == "Bloques":
            self.boton_luigi.hide()
            self.boton_fantasmav.hide()
            self.boton_fantasmah.hide()
            self.boton_pared.show()
            self.boton_roca.show()
            self.boton_fuego.show()
            self.boton_star.show()
        elif self.selector_tipos.currentText() == "Todos":
            self.boton_luigi.show()
            self.boton_fantasmav.show()
            self.boton_fantasmah.show()
            self.boton_pared.show()
            self.boton_roca.show()
            self.boton_fuego.show()
            self.boton_star.show()

    def abrir_constructor(self):
        self.show()
        self.senal_cerrar_inicio.emit()

    def cerrar_constructor(self):
        self.hide()

    def ultimo_boton_luigi(self):
        self.ultimo_boton = "L"

    def ultimo_boton_vertical(self):
        self.ultimo_boton = "V"

    def ultimo_boton_horizontal(self):
        self.ultimo_boton = "H"

    def ultimo_boton_pared(self):
        self.ultimo_boton = "P"

    def ultimo_boton_fuego(self):
        self.ultimo_boton = "F"

    def ultimo_boton_roca(self):
        self.ultimo_boton = "R"

    def ultimo_boton_star(self):
        self.ultimo_boton = "S"

    def crear_mapa_txt(self):
        txt_mapa = []
        for i in range(14):
            fila = []
            for j in range(9):
                fila.append("-")
            txt_mapa.append(fila)
        return txt_mapa

    def cambiar_grid(self):
        boton = self.sender()
        ubicacion = self.grid.indexOf(boton)
        i = ubicacion // 16
        j = ubicacion - (16 * i)
        if self.ultimo_boton == "":
            return
        elif self.ultimo_boton == "L" and self.luigis > 0:
            self.grid.addWidget(Luigi(), j, i)
            self.luigis -= 1
            self.mapa_txt[j - 1][i - 1] = "L"
        elif self.ultimo_boton == "V" and self.vertical > 0:
            self.grid.addWidget(Vertical(), j, i)
            self.vertical -= 1
            self.mapa_txt[j - 1][i - 1] = "V"
        elif self.ultimo_boton == "H" and self.horizontal > 0:
            self.grid.addWidget(Horizontal(), j, i)
            self.horizontal -= 1
            self.mapa_txt[j - 1][i - 1] = "H"
        elif self.ultimo_boton == "P" and self.pared > 0:
            self.grid.addWidget(Pared(), j, i)
            self.pared -= 1
            self.mapa_txt[j - 1][i - 1] = "P"
        elif self.ultimo_boton == "R" and self.roca > 0:
            self.grid.addWidget(Rock(), j, i)
            self.roca -= 1
            self.mapa_txt[j - 1][i - 1] = "R"
        elif self.ultimo_boton == "F" and self.fuego > 0:
            self.grid.addWidget(Fuego(), j, i)
            self.fuego -= 1
            self.mapa_txt[j - 1][i - 1] = "F"
        elif self.ultimo_boton == "S" and self.star > 0:
            self.grid.addWidget(Star(), j, i)
            self.star -= 1
            self.mapa_txt[j - 1][i - 1] = "S"

    def limpiar_mapa(self):
        self.nueva_ventana = VentanaConstructor()
        self.nueva_ventana.show()
        self.nueva_ventana.nombre = self.nombre
        self.hide()

    def comenzar(self):
        if self.luigis == 0 and self.star == 0:
            lineas = ["".join(fila) for fila in self.mapa_txt]
            self.senal_comenzar.emit(lineas)
            self.enviar_nombre.emit(self.nombre)
            self.hide()
        else:
            self.mostrar_pop_up()

    def mostrar_pop_up(self):
        mensaje = QMessageBox()
        mensaje.setWindowTitle("Error")
        mensaje.setText(f"Para comenzar la partida tienes que tener minimo un Luigi y una Star")
        ventana = mensaje.exec()

    def guardar_nombre(self, texto):
        self.nombre = texto
