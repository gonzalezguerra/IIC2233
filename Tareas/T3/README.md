# Tarea 3: DCCachos :school_satchel:

## Consideraciones generales :octocat:

Se realizo el juego solicitado, funciona todo como corresponde. lo unico que a veces falla (es el unico error que me encontre) es que a veces en algunas salas donde se presentan bots, despues de algunos turnos se queda congelado y nadie puede jugar (es raro que suceda), lo otro que hay que tener cuidado es que para utilizar el poder se creo un Qlineedit abajo de este para que se escriba el nombre de a quien va dirigido (hay que tener cuidado con los espacios). Por ultimo la resolucion y geometry que ocupe para el programa al igual que la distribucion de labels la deje asi por la resolucion de mi pantalla (espero que se vea bien). Tambien le puse algunos msleep para que no se traslapen los prints (y funciones) y que sea mas entendible lo que pasa. A veces cuando un jugador pierde no se actualiza el layout de la status bar pero al jugar el siguiente jugador (que es el que debe jugar) vuelve todo a la normalidad.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Networking: 18 pts (16%)
##### ✅ Protocolo
- utilizo el protocolo socket.AF_INET, socket.SOCK_STREAM para hacer uso del TCP/IP
##### ✅ Correcto uso de sockets
- Se aceptan los sockets y se utilizan para el correcto envio de información (bytes) y para instanciar los respectivos threads
##### ✅ Conexión
- Pueden haber varios jugadores conectados al mismo tiempo al servidor y hacer envio de señales simultaneamete gracias a multiples threads
##### ✅ Manejo de Clientes
- Se maneja 4 clientes con nombres (importados desde el json) y si es que esta la sala llena (lobby) se les envia una QMessageBOX para que cierren el programa, si es que la partida esta en juego tambien se le informa de la misma manera (especificando siempre la razon)
##### ✅ Desconexión Repentina
- Cuando un cliente se desconecta se retira su conexion sin afectar el resto de clientes, cuando el servidor se desconecta se le avisa a todos los clientes con un MessageBox para cerrar el programa
#### Arquitectura Cliente - Servidor: 18 pts (16%)
##### ✅ Roles
- Se separaron las labores del Cliente y Servidor logrando que el servidor maneje todo el proceso del juego, manteniendo actualizado a todos los clientes en todo momento
##### ✅ Consistencia
- Se respeta lo solicitado en el enunciado, coordinando en todo momento los clientes y no hacer acciones de mas en el cliente
##### ✅ Logs
- Se realizan los Logs solicitados en el enunciado, para cada accion de juego
#### Manejo de Bytes: 26 pts (22%)
##### ✅ Codificación
- Se codifica segun lo especificado, se creo una funcion codificar que realiza lo pedido (la funcion se encuentra en functions.py)
##### ✅ Decodificación
- Se decodifica segun lo especificado, se creo una funcion decodificar que decodifica lo que retorna la funcion codificar (la funcion se encuentra en functions.py)
##### ✅ Encriptación
- La funcion encriptar se encuentra en cripto.py (se saco de la carpeta scripts.py para poder importarla correctamente)
##### ✅ Desencriptación
- La funcion desencriptar se encuentra en cripto.py (se saco de la carpeta scripts.py para poder importarla correctamente)
##### ✅ Integración
- Se integro la encriptacion y la codificacion en todo el programa para el envio mediante metodo send y para la recepcion de mensajes entre sockets mediante el metodo recibir_mensajes
#### Interfaz Gráfica: 22 pts (19%)
##### ✅ Ventana de Inicio
- La ventana de inicio incluye lo pedido, el titulo sala de espera, con los jugadores apareciendo y desapareciendo dependiendo de su conexion con el servidor, y dos botones para comenzar la partida o salir del programa
##### ✅ Ventana de juego
- La ventana de Juego incluye lo solicitado, funcionan todos los botones, jugando los turnos en antihorario, actualizando la barra superior mostrando los datos de la partida
#### Reglas de DCCachos: 22 pts (19%)
##### ✅ Inicio del juego
- Se designa aleatoriamente la persona que parte la partida, y despues de esto se asigna un orden para el resto de turnos, ademas se le envian los dados a los jugadores siendo los numeros de estos designados de forma aleatoria mediante un randint
##### ✅ Bots
- Los bots cumplen lo pedido, se definieron dos funciones para que los bots funcionaran, la primera jugar_bot que cumple hace que juegue  un bot segun las instrucciones pedidas, y la segunda verificar_bot() que revisa si a la persona que le toca jugar esta desconectada para que el bot juegue por ella
##### ✅ Ronda
- Se cumple la regla de anunciar un valor mas alto, se puede pasar conservando el valor, se puede dudar cumpliendo las reglas y disminuyendo una vida, tambien solo se pueden usar poderes si uno tiene los valores pedidos (1,2 y 1,3)
##### ✅ Termino del juego
- Durante el transcurso del juego a los jugadores con 0 vidas se les informa que perdieron y cuando queda un unico jugador con vidas se le informa que gano
#### Archivos: 10 pts (9%)
##### ✅ Parámetros (JSON)
- Se utiliza todo los parametros desde un archivo JSON por lo cual se define una funcion (parametro_json) en functions.py que entrega el valor del argumento entregado a la funcion
##### ✅ main.py
- Se configura el main para que se le pueda pasar el puerto mediante consola en la apertura del programa o tambien para que si no se le entrega ejecute los programas en el port 5050 de defeault
##### ✅ Cripto.py
- Se utiliza el archivo cripto.py que se encuentra en la respectiva carpeta de cliente, servidor respetando la individualidad, el archivo cripto incluye ambas funciones solicitadas que son utilizadas durante la comunicacion de los sockets
#### Bonus: 4 décimas máximo
##### ❌ Cheatcodes
##### ❌ Turno con tiempo

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```frontend.py```, ```backend.py```, ```functions.py```, ```cripto.py```, ```Sprites```  en ```cliente```
2. ```backend.py```, ```functions.py```, ```cripto.py``` en ```servidor```

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```socket```, ```threading```, ```sys```
2. ```os```: ```path```
3. ```pickle```: ```loads```, ```dumps```
4. ```random```: ```randint```, ```choice```, ```random```
5. ```PyQt5```: ```QtWidgets```, ```QtGui```, ```QtCore```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```functions```: Contiene a ```parametro_json```, ```desencriptar```, ```encriptar```

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Supuse que si algun cliente se desconectaba no podria reconectarse
2. Supuse que solamente se le tiene que otorgar un nombre a cuatro clientes que son los potenciales jugadores del dccachos
3. Supuse que una vez iniciado el juego es necesario reiniciar el servidor para que vuelvan a conectarse personas a la sala de espera
4. Supuse que cada vez que el servidor no le permite conectarse al cliente (por sala llena, o partida empezada, o que el mismo servidor este caido) el cliente al ver la advertencia cierra el programa por su cuenta inmediatamente
5. Supuse que hay algunos errores que se displayean en la terminal que no afectan al uso del programa por lo cual son ignorados
6. Supuse que si se desconectan todos mientras se esta jugando, los bots siguen jugando (se puede ver por los print de la terminal del servidor)
7. Supuse que si un jugador pierde se desconectara inmediatamente (el manualmente lo hara) despues de ver la QMessageBox

PD: Leer consideraciones generales por favor (primera parte)
-------
## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. Ayudantia 10
2. Experiencia 6


## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
