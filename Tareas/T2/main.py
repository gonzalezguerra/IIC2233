from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication
from frontend import VentanaInicio, VentanaConstructor
from backend_menus import Procesar
from frontend_juego import Mapa, VentanaJuego
from backend import Luigi
import sys


app = QApplication([])
ventana_inicio = VentanaInicio()
ventana_constructor = VentanaConstructor()
ventana_juego = VentanaJuego()
procesador = Procesar()

# Nombre
ventana_inicio.senal_nombre.connect(procesador.procesar_nombre)
procesador.senal_respuesta.connect(ventana_inicio.mostrar_pop_up)

# Mapas
procesador.senal_cambiar_ventana.connect(ventana_inicio.revisar_mapa)
ventana_inicio.senal_modo.connect(procesador.procesar_mapa)
procesador.senal_constructor.connect(ventana_constructor.abrir_constructor)
ventana_constructor.senal_cerrar_inicio.connect(ventana_inicio.cerrar_inicio)
procesador.senal_jugar_mapa.connect(ventana_juego.iniciar_mapa)
ventana_juego.senal_cerrar_inicio.connect(ventana_inicio.cerrar_inicio)
ventana_constructor.senal_comenzar.connect(ventana_juego.iniciar_mapa_constructor)

# Nombre
ventana_inicio.enviar_nombre.connect(ventana_constructor.guardar_nombre)
ventana_inicio.enviar_nombre.connect(ventana_juego.guardar_nombre)
ventana_constructor.enviar_nombre.connect(ventana_juego.guardar_nombre)

form = ventana_inicio
form.show()
sys.exit(app.exec())
