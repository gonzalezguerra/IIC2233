from PyQt5.QtWidgets import QApplication
from backend import Cliente
from frontend import VentanaInicio
from functions import parametro_json
import sys

app = QApplication([])

port = parametro_json("PORT") if len(sys.argv) < 2 else int(sys.argv[1])
host = 'localhost' if len(sys.argv) < 3 else sys.argv[2]
window = VentanaInicio()
client = Cliente(port, host)

client.update_lobby.connect(window.crear_jugador)
client.reset_lobby.connect(window.reiniciar_lobby)
client.desconectar.connect(window.desconectar)
client.servidor_off.connect(window.servidor_cerrado)
client.comenzar_on.connect(window.ventana_juego)
client.enviar_dados.connect(window.recibir_dados)
client.enviar_turno.connect(window.actualizar_turno)
client.recibir_anunciar.connect(window.cambiar_anunciar)
client.enviar_vidas.connect(window.actualizar_vidas)
client.senal_tapar.connect(window.tapar_dados)
client.senal_perder.connect(window.perder)
client.senal_ganar.connect(window.ganar)

window.comenzar_signal.connect(client.comenzar_partida)
window.anunciar_valor.connect(client.enviar_anunciar)
window.senal_pasar.connect(client.enviar_pasar)
window.senal_poder.connect(client.enviar_poder)
window.senal_cambiar.connect(client.enviar_cambiar)
window.senal_dudar.connect(client.enviar_dudar)


window.show()
sys.exit(app.exec_())
