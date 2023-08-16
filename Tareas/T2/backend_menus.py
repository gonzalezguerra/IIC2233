from PyQt5.QtCore import QObject, pyqtSignal
from parametros import MIN_CARACTERES, MAX_CARACTERES


class Procesar(QObject):

    senal_respuesta = pyqtSignal(str)
    senal_cambiar_ventana = pyqtSignal()
    senal_constructor = pyqtSignal()
    senal_jugar_mapa = pyqtSignal(str)

    def procesar_nombre(self, nombre):
        if nombre.isalpha():
            if len(nombre) >= MIN_CARACTERES and len(nombre) <= MAX_CARACTERES:
                self.senal_cambiar_ventana.emit()
            else:
                self.senal_respuesta.emit("Caracteres")
        else:
            self.senal_respuesta.emit("Alpha")

    def procesar_mapa(self, texto):
        if texto == "modo constructor":
            self.senal_constructor.emit()
        else:
            self.senal_jugar_mapa.emit(texto)
