# Communication Layer


## Objetivo

Crear una capa independiente para comunicarse con diferentes controladores CNC.


## Funciones

Actualmente:

- Conexión
- Desconexión
- Envío de comandos
- Recepción de mensajes


## Futuro


Se agregarán:

- Puerto Serial USB
- Arduino
- GRBL
- ESP32


## Ejemplo


```python
comm = Communication()

comm.connect()

comm.send("G0 X10")
