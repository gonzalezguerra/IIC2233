from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QTimer, pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QWidget, QApplication
from PyQt5.QtGui import QFont, QPixmap, QMouseEvent, QKeyEvent, QIcon
from os import path, listdir
from parametros import MIN_VELOCIDAD, MAX_VELOCIDAD
from random import random, uniform
import sys


class Luigi(QLabel):

    def __init__(self):
        super().__init__()
        foto_luigi = QPixmap(path.join("sprites", "Personajes", "luigi_front.png"))
        self.setPixmap(foto_luigi)
        self.setAccessibleName("luigi")
        self.revisar()

    def sprites_derecha(self):
        adelante = None
        if self.parent() != None:
            if self.parent().childAt(self.x() + 35, self.y()) != None:
                adelante = self.parent().childAt(self.x() + 35, self.y()).accessibleName()
            else:
                adelante = None
        if (self.x() + 11) < 280 and adelante != "pared" and adelante != "roca":
            self.move(self.x() + 11, self.y())
            self.setPixmap(QPixmap(path.join("sprites", "Personajes", "luigi_rigth_1.png")))
            QTimer.singleShot(50, self.sprites_derecha_2)
        elif adelante == "roca":
            if self.parent().childAt(self.x() + 65, self.y()) == None:
                roca = self.parent().childAt(self.x() + 35, self.y())
                roca.move(roca.x() + 32, roca.y())

    def sprites_derecha_2(self):
        self.move(self.x() + 11, self.y())
        self.setPixmap(QPixmap(path.join("sprites", "Personajes", "luigi_rigth_2.png")))
        QTimer.singleShot(50, self.sprites_derecha_3)

    def sprites_derecha_3(self):
        self.move(self.x() + 10, self.y())
        self.setPixmap(QPixmap(path.join("sprites", "Personajes", "luigi_rigth_3.png")))

    def sprites_izquierda(self):
        adelante = None
        if self.parent() != None:
            if self.parent().childAt(self.x() - 30, self.y()) != None:
                adelante = self.parent().childAt(self.x() - 30, self.y()).accessibleName()
            else:
                adelante = None
        if (self.x() - 11) > 32 and adelante != "pared" and adelante != "roca":
            self.move(self.x() - 11, self.y())
            self.setPixmap(QPixmap(path.join("sprites", "Personajes", "luigi_left_1.png")))
            QTimer.singleShot(50, self.sprites_izquierda_2)
        elif adelante == "roca":
            if self.parent().childAt(self.x() - 60, self.y()) == None:
                roca = self.parent().childAt(self.x() - 30, self.y())
                roca.move(roca.x() - 32, roca.y())

    def sprites_izquierda_2(self):
        self.move(self.x() - 11, self.y())
        self.setPixmap(QPixmap(path.join("sprites", "Personajes", "luigi_left_2.png")))
        QTimer.singleShot(50, self.sprites_izquierda_3)

    def sprites_izquierda_3(self):
        self.move(self.x() - 10, self.y())
        self.setPixmap(QPixmap(path.join("sprites", "Personajes", "luigi_left_3.png")))

    def sprites_abajo(self):
        adelante = None
        if self.parent() != None:
            if self.parent().childAt(self.x(), self.y() + 35) != None:
                adelante = self.parent().childAt(self.x(), self.y() + 35).accessibleName()
            else:
                adelante = None
        if (self.y() + 11) < 450 and adelante != "pared" and adelante != "roca":
            self.move(self.x(), self.y() + 11)
            self.setPixmap(QPixmap(path.join("sprites", "Personajes", "luigi_down_1.png")))
            QTimer.singleShot(50, self.sprites_abajo_2)
        elif adelante == "roca":
            if self.parent().childAt(self.x(), self.y() + 65) == None:
                roca = self.parent().childAt(self.x(), self.y() + 35)
                roca.move(roca.x(), roca.y() + 32)

    def sprites_abajo_2(self):
        self.move(self.x(), self.y() + 11)
        self.setPixmap(QPixmap(path.join("sprites", "Personajes", "luigi_down_2.png")))
        QTimer.singleShot(50, self.sprites_abajo_3)

    def sprites_abajo_3(self):
        self.move(self.x(), self.y() + 10)
        self.setPixmap(QPixmap(path.join("sprites", "Personajes", "luigi_down_3.png")))

    def sprites_arriba(self):
        adelante = None
        if self.parent() != None:
            if self.parent().childAt(self.x(), self.y() - 30) != None:
                adelante = self.parent().childAt(self.x(), self.y() - 30).accessibleName()
            else:
                adelante = None
        if (self.y() - 11) > 32 and adelante != "pared" and adelante != "roca":
            self.move(self.x(), self.y() - 11)
            self.setPixmap(QPixmap(path.join("sprites", "Personajes", "luigi_up_1.png")))
            QTimer.singleShot(50, self.sprites_arriba_2)
        elif adelante == "roca":
            if self.parent().childAt(self.x(), self.y() - 40) == None:
                roca = self.parent().childAt(self.x(), self.y() - 30)
                roca.move(roca.x(), roca.y() - 32)

    def sprites_arriba_2(self):
        self.move(self.x(), self.y() - 11)
        self.setPixmap(QPixmap(path.join("sprites", "Personajes", "luigi_up_2.png")))
        QTimer.singleShot(50, self.sprites_arriba_3)

    def sprites_arriba_3(self):
        self.move(self.x(), self.y() - 10)
        self.setPixmap(QPixmap(path.join("sprites", "Personajes", "luigi_up_3.png")))

    def revisar(self):
        if self.parent() != None:
            if self.parent().childAt(self.x(), self.y()) != None:
                nombre = self.parent().childAt(self.x(), self.y()).accessibleName()
                if nombre == "vertical" or nombre == "horizontal":
                    self.parent().parent().perder_vidas()
                else:
                    QTimer.singleShot(100, self.revisar)
            else:
                QTimer.singleShot(100, self.revisar)
        else:
            QTimer.singleShot(100, self.revisar)


class Vertical(QLabel):

    def __init__(self):
        super().__init__()
        foto_vertical = QPixmap(path.join("sprites", "Personajes", "red_ghost_vertical_2.png"))
        self.setPixmap(foto_vertical)
        self.ponderador = uniform(MIN_VELOCIDAD, MAX_VELOCIDAD)
        self.tiempo = int(round(500 / self.ponderador, 1))
        self.setAccessibleName("vertical")
        self.playing = True
        self.sprites_abajo()

    def sprites_abajo(self):
        if self.playing:
            adelante = None
            if self.parent() != None:
                if self.parent().childAt(self.x(), self.y() + 40) != None:
                    adelante = self.parent().childAt(self.x(), self.y() + 40).accessibleName()
                else:
                    adelante = None
            if (self.y() + 11) < 448 and adelante != "pared" and adelante != "roca":
                self.move(self.x(), self.y() + 11)
                relativo = path.join("sprites", "Personajes", "red_ghost_vertical_1.png")
                self.setPixmap(QPixmap(relativo))
                QTimer.singleShot(self.tiempo, self.sprites_abajo_2)
            else:
                QTimer.singleShot(self.tiempo, self.sprites_arriba)
        else:
            QTimer.singleShot(100, self.sprites_abajo)

    def sprites_abajo_2(self):
        self.move(self.x(), self.y() + 11)
        self.setPixmap(QPixmap(path.join("sprites", "Personajes", "red_ghost_vertical_2.png")))
        QTimer.singleShot(self.tiempo, self.sprites_abajo_3)

    def sprites_abajo_3(self):
        self.move(self.x(), self.y() + 10)
        self.setPixmap(QPixmap(path.join("sprites", "Personajes", "red_ghost_vertical_3.png")))
        QTimer.singleShot(self.tiempo, self.sprites_abajo)

    def sprites_arriba(self):
        if self.playing:
            adelante = None
            if self.parent() != None:
                if self.parent().childAt(self.x(), self.y() - 40) != None:
                    adelante = self.parent().childAt(self.x(), self.y() - 40).accessibleName()
                else:
                    adelante = None
            if (self.y() - 11) > 32 and adelante != "pared" and adelante != "roca":
                self.move(self.x(), self.y() - 11)
                relativo = path.join("sprites", "Personajes", "red_ghost_vertical_1.png")
                self.setPixmap(QPixmap(relativo))
                QTimer.singleShot(self.tiempo, self.sprites_arriba_2)
            else:
                QTimer.singleShot(self.tiempo, self.sprites_abajo)
        else:
            QTimer.singleShot(100, self.sprites_arriba)

    def sprites_arriba_2(self):
        self.move(self.x(), self.y() - 11)
        self.setPixmap(QPixmap(path.join("sprites", "Personajes", "red_ghost_vertical_2.png")))
        QTimer.singleShot(self.tiempo, self.sprites_arriba_3)

    def sprites_arriba_3(self):
        self.move(self.x(), self.y() - 10)
        self.setPixmap(QPixmap(path.join("sprites", "Personajes", "red_ghost_vertical_3.png")))
        QTimer.singleShot(self.tiempo, self.sprites_arriba)

    def pausar(self):
        self.playing = not self.playing


class Horizontal(QLabel):

    def __init__(self):
        super().__init__()
        foto_horizontal = QPixmap(path.join("sprites", "Personajes", "white_ghost_rigth_2.png"))
        self.setPixmap(foto_horizontal)
        self.ponderador = uniform(MIN_VELOCIDAD, MAX_VELOCIDAD)
        self.tiempo = int(round(500 / self.ponderador, 1))
        self.setAccessibleName("horizontal")
        self.playing = True
        self.sprites_derecha()

    def sprites_derecha(self):
        if self.playing:
            adelante = None
            if self.parent() != None:
                if self.parent().childAt(self.x() + 40, self.y()) != None:
                    adelante = (self.parent().childAt(self.x() + 40, self.y())).accessibleName()
                else:
                    adelante = None
            if (self.x() + 11) < 280 and adelante != "pared" and adelante != "roca":
                self.move(self.x() + 11, self.y())
                relativo = path.join("sprites", "Personajes", "white_ghost_rigth_1.png")
                self.setPixmap(QPixmap(relativo))
                QTimer.singleShot(self.tiempo, self.sprites_derecha_2)
            else:
                QTimer.singleShot(self.tiempo, self.sprites_izquierda)
        else:
            QTimer.singleShot(100, self.sprites_derecha)

    def sprites_derecha_2(self):
        self.move(self.x() + 11, self.y())
        self.setPixmap(QPixmap(path.join("sprites", "Personajes", "white_ghost_rigth_2.png")))
        QTimer.singleShot(self.tiempo, self.sprites_derecha_3)

    def sprites_derecha_3(self):
        self.move(self.x() + 10, self.y())
        self.setPixmap(QPixmap(path.join("sprites", "Personajes", "white_ghost_rigth_3.png")))
        QTimer.singleShot(self.tiempo, self.sprites_derecha)

    def sprites_izquierda(self):
        if self.playing:
            adelante = None
            if self.parent() != None:
                if self.parent().childAt(self.x() - 40, self.y()) != None:
                    adelante = (self.parent().childAt(self.x() - 40, self.y())).accessibleName()
                else:
                    adelante = None
            if (self.x() - 11) > 32 and adelante != "roca" and adelante != "pared":
                self.move(self.x() - 11, self.y())
                relativo = path.join("sprites", "Personajes", "white_ghost_left_1.png")
                self.setPixmap(QPixmap(relativo))
                QTimer.singleShot(self.tiempo, self.sprites_izquierda_2)
            else:
                QTimer.singleShot(self.tiempo, self.sprites_derecha)
        else:
            QTimer.singleShot(100, self.sprites_izquierda)

    def sprites_izquierda_2(self):
        self.move(self.x() - 11, self.y())
        self.setPixmap(QPixmap(path.join("sprites", "Personajes", "white_ghost_left_2.png")))
        QTimer.singleShot(self.tiempo, self.sprites_izquierda_3)

    def sprites_izquierda_3(self):
        self.move(self.x() - 10, self.y())
        self.setPixmap(QPixmap(path.join("sprites", "Personajes", "white_ghost_left_3.png")))
        QTimer.singleShot(self.tiempo, self.sprites_izquierda)

    def pausar(self):
        self.playing = not self.playing


class Pared(QLabel):

    def __init__(self):
        super().__init__()
        foto_pared = QPixmap(path.join("sprites", "Elementos", "wall.png"))
        self.setPixmap(foto_pared)
        self.setAccessibleName("pared")


class Rock(QLabel):

    def __init__(self):
        super().__init__()
        foto_roca = QPixmap(path.join("sprites", "Elementos", "rock.png"))
        self.setPixmap(foto_roca)
        self.setAccessibleName("roca")


class Fuego(QLabel):

    def __init__(self):
        super().__init__()
        foto_fuego = QPixmap(path.join("sprites", "Elementos", "fire.png"))
        self.setPixmap(foto_fuego)
        self.setAccessibleName("fuego")
        self.revisar()

    def revisar(self):
        if self.parent() != None:
            if self.parent().childAt(self.x(), self.y()) != None:
                nombre = self.parent().childAt(self.x(), self.y()).accessibleName()
                if nombre == "vertical" or nombre == "horizontal":
                    ghost = self.parent().childAt(self.x(), self.y())
                    ghost.hide()
                    QTimer.singleShot(100, self.revisar)
                elif nombre == "luigi":
                    self.parent().parent().perder_vidas()
                else:
                    QTimer.singleShot(100, self.revisar)
            else:
                QTimer.singleShot(100, self.revisar)
        else:
            QTimer.singleShot(100, self.revisar)


class Star(QLabel):

    def __init__(self):
        super().__init__()
        foto_star = QPixmap(path.join("sprites", "Elementos", "osstar.png"))
        self.setPixmap(foto_star.scaled(30, 30, Qt.KeepAspectRatio))
        self.setMaximumSize(30, 30)
        self.setAccessibleName("star")


class Borde(QLabel):

    def __init__(self):
        super().__init__()
        foto_borde = QPixmap(path.join("sprites", "Elementos", "bordermap.png"))
        self.setPixmap(foto_borde.scaled(32, 32, Qt.KeepAspectRatio))
        self.setMaximumSize(32, 32)
        self.setAccessibleName("borde")
