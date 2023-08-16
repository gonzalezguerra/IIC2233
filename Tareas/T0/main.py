from os import path
from tablero import imprimir_tablero
from functions import cargar_tablero, guardar_tablero, verificar_valor_bombas 
from functions import verificador_tablero, solucionar_tablero, verificar_tortugas


if __name__ == "__main__":
    print("*** Menú de Inicio ***")
    print("")
    print("Indique el nombre del archivo que desea abrir:")
    nombre_archivo = input()
    if path.exists(f"Archivos/{nombre_archivo}"):
        tablero = cargar_tablero(nombre_archivo)
        print("*** Menú de Acciones ***")
        print("")
        print("[1] Mostrar tablero")
        print("[2] Validar tablero")
        print("[3] Revisar solución")
        print("[4] Solucionar tablero")
        print("[5] Salir del programa")
        print("")
        print("Indique su opción (1, 2, 3, 4 o 5)")
        while True:
            opcion = input()
            if opcion == "1":
                imprimir_tablero(tablero, utf8=True)
            if opcion == "2":
                if verificar_valor_bombas(tablero) > 0 or verificar_tortugas(tablero) > 0:
                    print("El tablero NO es válido")
                else:
                    print("El tablero SI es válido")
            if opcion == "3":
                if verificador_tablero(tablero) > 0 or verificar_tortugas(tablero) > 0:
                    print("El tablero NO es válido")
                else:
                    print("El tablero SI es válido")
            if opcion == "4":
                tablero_solucionado = solucionar_tablero(tablero)
                if tablero_solucionado == None:
                    print("El tablero NO tiene solucion")
                else:
                    imprimir_tablero(tablero_solucionado)
                nombre_archivo_sin_extension, extension = path.splitext(nombre_archivo)
                nombre_archivo_solucionado = nombre_archivo_sin_extension + "_sol" + extension
                guardar_tablero(nombre_archivo_solucionado, tablero_solucionado)
            if opcion == "5":
                break
    else:
        print("No existe el archivo")
