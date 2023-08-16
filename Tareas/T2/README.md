# Tarea 2: DCCazafantasmas 👻🧱🔥


## Consideraciones generales :octocat:

El juego funciona y cumple con lo solicitado, se realiza un unico bonus que es el de volver a jugar (no se realiza follower villain y drag and drop), se asume que el jugador tiene una resolucion acorde.

### Cosas implementadas y no implementadas :white_check_mark: :x:


#### Ventanas: 27 pts (27%)
##### ✅ Ventana de Inicio
- Se realizo la ventana de inicio pidiendo el nombre al usuario, que seleccione un mapa o el modo constructor y despues de eso tiene dos botones con los cuales puede hacer login o salir del programa.
##### ✅ Ventana de Juego
- La parte del constructor se realizo en una ventana previa que al darle a comenzar deriva a la ventana de juegop. Se creo una ventana de juego en la cual aparece en el lado izquierdo el tiempo restante y las vidas restantes, y en el lado derecho el mapa de 16 x 11 en el cual se puede jugar.
#### Mecánicas de juego: 47 pts (47%)
##### ✅ Luigi
- Se realizo el movimiento discreto continuo de Luigi, y se conectaron las animaciones con las teclas WASD para animar su movimiento. Se asumio que el movimiento de luigi se hace como dice el enunciado (un click una casilla), no se puede mantener presionado.
##### ✅ Fantasmas
- Se genero el movimiento discreto continuo de los fantasmas y ademas se asumio que el rango aleatorio de movimiento de cada fantasma se calcula aleatoriamente en su init (por lo cual la velocidad no es uniforme para todos los fantasmas).
##### ✅ Modo Constructor
- En el modo constructor se le agrega un numero en cada boton del selector que muestra la cantidad maxima de ese tipo de personaje o objeto puede haber en el mapa.
##### ✅ Fin de ronda
- Al finalizar la ronda, si es que pierde el jugador aparece una ventana pop up (que dice "PERDISTE") en la cual se le pregunta si quiere salir o volver a jugar, si es que gana sale un pop up en la cual el titulo es "GANASTE" y se muestra el nombre y puntaje obtenido (ademas de dar la opcion de volver a jugar o salir del programa)
#### Interacción con el usuario: 14 pts (14%)
##### ✅ Clicks
- Se configuro el click para seleccionar la lista de mapas y apretar botones de login, salir, cambiar las entidades que salen en el menu y en especial el modo constructor, y el resto de cosas de movimiento y cheatcodes con el click de botones en el teclado
##### ✅ Animaciones
- Se realizaron los sprites de los personajes creando un bucle de 3 animaciones que se van actualizando cada cierto tiempo (uno definido para luigi para que se vea bien y uno aleatorio para los fantamas)
#### Funcionalidades con el teclado: 8 pts (8%)
##### ✅ Pausa
- Se configuro la pausa con la tecla P ademas del boton de pausa que se puede clickear directamente para pausar y resumir el tiempo de la partida (tambien se configuro para que si se activa el cheatcode de vidas infinitas el tiempo no disminuya)
##### ✅ K + I + L
- Se realizo el cheatcode de eliminar villanos (fantasmas) se supuso que se activaria una vez y que se activaria presionando esas teclas en ese mismo orden y no pulsandolas al mismo tiempo. Se asume que el cheatcode cada vez que se pierde una vida o se reinicia el mapa tiene que volver a activarse
##### ✅ I + N + F
- Se realizo el cheatcode de vidas infinitas se supuso que se activaria una vez y que se activaria presionando esas teclas en ese mismo orden y no pulsandolas al mismo tiempo (detiene el tiempo y hace que desde ese punto las vidas de luigi no puedan disminuir). Se asume que el cheatcode queda activado para siempre se pierda vidas o se seleccione volver a jugar.
#### Archivos: 4 pts (4%)
##### ✅ Sprites
- El archivo de sprites, sonidos y mapas se agrego al gitignore como dice el enunciado
##### ✅ Parametros.py
- Se creo un archivo parametros.py en el cual se pueden cambiar los valores de los stats importantes como puede ser el tiempo, vidas, ponderadores, y maximo y minimos de personajes o largo de nombres.
#### Bonus: 8 décimas máximo
##### ✅ Volver a Jugar
- Se realizo la opcion de volver a jugar despues de que uno termina una partida (se gane o se pierda), se genera una ventana pop up en la cual tiene dos botones (volver a jugar o salir del programa)
##### ❌ Follower Villain
##### ❌ Drag and Drop

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```sprites``` la cual debe contener los sprites de los elementos graficos
2. ```mapas``` la cual debe contener los mapas precargados que se pueden jugar
3. ```sonidos``` la cual debe contener el sonido final de victoria o derrota


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5```: ```QtCore``` , ```QtWidgets```, ```QtGui```, ```QtMultimedia```
2. ```os```: ```path``` , ```listdir```
3. ```random```: ```random``` , ```uniform```
4. ```sys```

PD: La libreria PyQt5 al tener una gran cantidad de funciones solamente se nombro los modulos de la libreria que se importo (cada modulo tiene funciones especificas que se importaron)

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```backend```: Contiene a ```Luigi```, ```Vertical```, ```Horizontal```, ```Pared```, ```Rock```, ```Fuego```, ```Star```, ```Borde```.
2. ```backend_menus```: Hecha para revisar el nombre y el mapa que se selecciona en la ventana de inicio
3. ```frontend```: Contiene a ```VentanaInicio```, ```VentanaConstructor```.
4. ```frontend_juego```: Contiene a ```VentanaJuego```, ```Mapa```.
5. ```parametros```: Contiene a los parametros variables del programa.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Se asume que el tiempo MIN_VELOCIDAD Y MAX_VELOCIDAD asociado al movimiento de los fantasmas va a ser un tiempo cercano a 1 (aunque puede ser diferente) pero podría afectar a la visualizacion de las sprites de los fantasmas
2. Se asume que cuando uno selecciona algo en el modo constructor para agregar puede agregar todos los elementos seguidos sin necesidad de volver a presionar el mismo objeto de nuevo (si se quiere poner menos del total puede cambiar seleccionando otro elemento o comenzar la partida)
3. Se asume que en el modo constructor cuando se selecciona limpiar, se limpia toda la grid "volviendo a empezar" la construccion del juego
4. Se asume que hay algunos tipos de acciones que es mas conveniente hacer directamente en el frontend sin perder obviamente la escencia de que principalmente se trabajan elementos graficos
5. Se asume que el usuario del juego va a tener una resolucion pertinente para el juego y que las ventanas no van a ser modificadas en dimension debido a que puede afectar la visualizacion

PD: Se asume que durante el juego se va a apretar un boton a la vez y no manteniendo presionado, como en los juegos antiguos


-------

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).