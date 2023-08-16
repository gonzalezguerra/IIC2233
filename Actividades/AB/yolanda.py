import api
import re
import requests
import time


class Yolanda:

    def __init__(self, host, port):
        self.base = f"http://{host}:{port}"
        self.regex_validador_fechas = r"\d{1,2}(\s)(de)(\s)([a-zA-Z])+\sde\s((19|20)?\d{2})$"
        self.regex_extractor_signo = r"((LAS|las)|(los|LOS))(\s*)(.+)((NAS|nas)|(nos|NOS))(\s+)pueden(.+)(\.)$"

    def saludar(self) -> dict:
        # TODO: Completar
        solicitud = requests.get(self.base)
        json = solicitud.json()
        return {"status-code": solicitud.status_code, "saludo": json["result"]}

    def verificar_horoscopo(self, signo: str) -> bool:
        # TODO: Completar
        solicitud = requests.get(self.base+"/signos")
        json = solicitud.json()
        if signo in json["result"]:
            return True
        else:
            return False

    def dar_horoscopo(self, signo: str) -> dict:
        # TODO: Completar
        base = self.base
        parametros = {"signo": signo}
        endpoint = "/horoscopo"
        solicitud = requests.get(base + endpoint, params=parametros)
        dicc = solicitud.json()
        status = solicitud.status_code
        return {"status-code": status, "mensaje": dicc["result"]}

    def dar_horoscopo_aleatorio(self) -> dict:
        # TODO: Completar
        base = self.base
        endpoint = "/aleatorio"
        solicitud = requests.get(base + endpoint)
        dicc = solicitud.json()
        status = solicitud.status_code
        if int(status) == 200:
            url = dicc["result"]
            solicitud2 = requests.get(url)
            dicc2 = solicitud2.json()
            status2 = solicitud2.status_code
            return {"status-code": status2, "mensaje": dicc2["result"]}
        else:
            return {"status-code": status, "mensaje": dicc["result"]}

    def agregar_horoscopo(self, signo: str, mensaje: str, access_token: str) -> str:
        # TODO: Completar+
        base = self.base
        endpoint = "/update"
        my_headers = {
            "Authorization": access_token
        }
        data = {
            'signo': signo,
            'mensaje': mensaje
        }
        response = requests.post(base + endpoint, headers=my_headers, data=data)
        dicc = response.json()
        if response.status_code == 401:
            return "Agregar horoscopo no autorizado"
        elif response.status_code == 400:
            return dicc["result"]
        else:
            return "La base de YolandaAPI ha sido actualizada"

    def actualizar_horoscopo(self, signo: str, mensaje: str, access_token: str) -> str:
        # TODO: Completar
        base = self.base
        endpoint = "/update"
        my_headers = {
            "Authorization": access_token
        }
        data = {
            'signo': signo,
            'mensaje': mensaje
        }
        response = requests.put(base + endpoint, headers=my_headers, data=data)
        dicc = response.json()
        if response.status_code == 401:
            return "Editar horoscopo no autorizado"
        elif response.status_code == 400:
            return dicc["result"]
        else:
            return "La base de YolandaAPI ha sido actualizada"

    def eliminar_signo(self, signo: str, access_token: str) -> str:
        # TODO: Completar
        base = self.base
        endpoint = "/remove"
        my_headers = {
            "Authorization": access_token
        }
        data = {
            'signo': signo
        }
        response = requests.delete(base + endpoint, headers=my_headers, data=data)
        dicc = response.json()
        if response.status_code == 401:
            return "Eliminar signo no autorizado"
        elif response.status_code == 400:
            return dicc["result"]
        else:
            return "La base de YolandaAPI ha sido actualizada"


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4444
    DATABASE = {
        "acuario": "Hoy será un hermoso día",
        "leo": "No salgas de casa.... te lo recomiendo",
    }
    thread = api.Server(HOST, PORT, DATABASE)
    thread.start()

    yolanda = Yolanda(HOST, PORT)
    print(yolanda.saludar())
    print(yolanda.dar_horoscopo_aleatorio())
    print(yolanda.verificar_horoscopo("acuario"))
    print(yolanda.verificar_horoscopo("pokemon"))
    print(yolanda.dar_horoscopo("acuario"))
    print(yolanda.dar_horoscopo("pokemon"))
    print(yolanda.agregar_horoscopo("a", "aaaaa", "pepaiic2233"))
    print(yolanda.dar_horoscopo("a"))
