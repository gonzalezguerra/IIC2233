# Tarea 1: DCCavaCava 🏖⛏


## Consideraciones generales :octocat:

- El juego funciona y cumple lo pedido, se puede simular el dia donde todos los excavadores disponibles (que no esten descansando) van a excavar, tambien van a intentar encontrar un item, posteriormente se revisa si hubo algun evento (como terremoto, derrumbe o lluvia).

- Cuando hay algun evento o se abre un tesoro que pueda cambiar el tipo de arena se realiza el cambio y se puede visualizar cuando se simule el dia siguiente.

- Cuando se seleccionan los excavadores iniciales, o se agregan mas excavadores podrian haber excavadores con el mismo nombre, se asume que es un alcance de nombre ya que son **independientes** debido a que sus estadisticas y acciones funcionan de forma independiente.


#### Programación Orientada a Objetos: 42 pts (35%)
##### ✅  Diagrama
- Se subio el diagrama de clases con nombre Diagrama_de_clases.pdf, en el cual Items compone a Arena, y los excavadores y la arena componen a la clase Torneo.
##### ✅ Definición de clases, atributos, métodos y properties
- Se crearon 4 clases principales (Arena, Excavador, Item y Torneo), Excavador es una clase abstracta la cual tiene 2 sub clases (Tareo y Docencio) las cuales son Padres de Hibrido (Todas las clases tienen los metodos solicitados y en los casos que tenian que volver a definirse como el cavar() de Docencio tambien se realizo), las clases que tienen parametros que puedan salirse de lo pedido se les definio properties (setters) que mantuvieran dentro del rango (por ejemplo: fuerza entre 1 y 10)

##### ✅ Relaciones entre clases
- Se relacionaron las clases de los tipos de Excavadores en distribucion tipo diamante y tambien se relacionaron en metodos (la clase cavar usa de parametro la Arena para saber sus dificultades y tipo) o parametros (la clase Torneo tiene un equipo que es una lista de excavadores y tambien tiene self.arena que es un objeto de clase Arena)

#### Preparación programa: 11 pts (9%)
##### ✅ Creación de partidas
- Funciona la creación de Torneos que esta ubicada en el menu inicial del programa
#### Entidades: 22 pts (18%)
##### ✅ Excavador
- Se creo la entidad excavador que es ABC debido a que nunca se llama directamente y solamente se ocupan sus 3 clases hijas (2 directas) dependiendo del tipo de excavador 
##### ✅ Arena
- Se creo la clase Arena que tiene un self.tipo que especifica el tipo de arena para que despues se puedan realizar los respectivos cambios de arena y verificar cuanto tienen que cavar los excavadores debido a las diferencias de dificultades de los tipos.
##### ✅ Torneo
- Se creo la clase Torneo donde se ejecuta la gran parte del programa y es donde se desarrolla el codigo, es una clase que no depende del resto pero si tiene parametros que incluyen el resto de clases para funcionar
#### Flujo del programa: 31 pts (26%)
##### ✅ Menú de Inicio
- El menu de inicio fue creado y funciona con tres opciones Nueva partida, cargar partida o salir
##### ✅ Menú Principal
- En este menu se desarrolla el juego y ademas se le suma la opcion de volver para poder volver al menu inicial si es que se desea
##### ✅ Simulación día Torneo
- Se creo un metodo en la clase torneo donde se siguio en orden el flujo solicitado, que los excavadores caven, buscar items, gasten energia, se vayan a descansar los excavadores con 0 energia y ademas se revisa si ocurrio un evento y sus efectos.
##### ✅ Mostrar estado torneo
- Se muestra el estado actual del torneo entre ellos el dia actual, tipo de arena, metros / metros totales, y el estado de todos los excavadores del equipo
##### ✅ Menú Ítems
- Muestra el nombre, tipo y descripcion de los items de la mochila, si es que la mochila esta sin items solamente da la opcion de volver o salir
##### ✅ Guardar partida
- Guarda la partida en el archivo de texto, DCCavaCava.txt (Si es que ya hay una partida guardada, la va a sobreescribir para guardar la ultima solicitada)
##### ✅ Robustez
- El flujo no se cierra hasta que se seleccione salir, y no se cae aunque ingreses cualquier input
#### Manejo de archivos: 14 pts (12%)
##### ✅ Archivos CSV 
##### ✅ Archivos TXT
##### ✅ parametros.py
#### Bonus: 3 décimas máximo
##### ❌ Guardar Partida

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```tesoros.csv```
2. ```consumibles.csv```
3. ```arenas.csv```
4. ```excavadores.csv```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```copy```: ```deepcopy```
2. ```random```: ```choices```, ```random```, ```randint```
3. ```abc```: ```ABC```
4. ```os``` : ```path```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```entidades```: Contiene a ```Torneo```
2. ```entidades_2```: Contiene a ```Arena```, ```Excavador```, ```Tareo```, ```Docencio```, ```Hibrido```, ```Item```, ```Consumible```, ```Tesoro```
3. ```listas.py```: Hecha para crear listas de excavadores y arenas que se utilizan en entidades
4. ```parametros.py```: Hecha para guardar los parametros que se utilizaran para jugar el juego

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Supuse que siempre se van a ejecutar los archivos en una ubicacion donde se le entregue consumibles.csv, tesoros.csv, excavadores.csv y arenas.csv
2. Supuse que no va a existir otro archivo DCCavaCava.txt que no sea el de partidas guardadas
3. Supuse que no era necesario hacer subclases a la arena debido a que no tienen metódos diferentes y realmente las diferencias son casi mínimas
4. Supuse que los metros cavados pueden ser negativos si es que ocurre un derrumbe debido a que pueden formarse montañas de tierra
5. Asumi que si hay algun cambio de arena ya sea por objetos o por eventos adversos y uno se encuentra en el mismo tipo de arena uno la mantiene con sus estadisticas porque no se cambia de arena realmente
6. Asumi que una vez que se determinan los dias de descanso de un excavador, estos van a descansar hasta que terminen estos dias (por mucho que un item les recupere la energia)
7. Supuse que pueden haber varios excavadores con los mismos nombres y estadisticas en un mismo equipo (repetirse desde el archivo csv) debido a que se pueden representar como tipos de excavadores 

-------
## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
