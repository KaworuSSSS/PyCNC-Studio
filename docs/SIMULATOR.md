# CNC Simulator


## Objetivo

El simulador permite desarrollar y probar PyCNC Studio sin hardware físico.


## Funciones actuales

- Conexión virtual
- Desconexión
- Home
- Movimiento de ejes
- Consulta de estado


## Ejemplo


```python
cnc.connect()

cnc.move("X",50)

cnc.get_status()
