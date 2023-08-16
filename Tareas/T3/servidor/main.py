from backend import Servidor
from functions import parametro_json
import sys


if __name__ == '__main__':
    port = parametro_json("PORT") if len(sys.argv) < 2 else int(sys.argv[1])
    host = 'localhost' if len(sys.argv) < 3 else sys.argv[2]
    server = Servidor(port, host)
