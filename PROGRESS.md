# PyCNC Studio — Estado del proyecto

## Versión actual

**v0.4 - Core CNC simulation working**

Release creado en GitHub:

* Tag: `v0.4`
* Estado: estable y probado

---

# Objetivo del proyecto

Crear un software de control CNC escrito en Python utilizando Arduino como hardware de control.

La idea general:

```
Python CNC Studio
        |
        |
   Comunicación
        |
        |
     Arduino
        |
        |
 Drivers / Motores CNC
```

Durante el desarrollo inicial se creó una arquitectura modular que permite probar el software sin hardware real usando un simulador CNC.

---

# Lo que ya está funcionando

## 1. Arquitectura base

Estructura creada:

```
app/
|
├── drivers/
│   ├── cnc_driver.py
│   └── simulator_driver.py
│
├── machine/
│   └── machine.py
│
├── job/
│   ├── __init__.py
│   └── job_manager.py
│
├── gcode/
│
├── comm/
│
├── core/
│
└── gui/
```

---

# Módulos implementados

## CNC Driver

Define la interfaz del controlador CNC.

Permite cambiar entre:

* Simulador
* Arduino real

sin cambiar la lógica principal.

---

## Simulator Driver

Simulador de máquina CNC.

Actualmente permite:

* Conectar
* Home
* Movimiento X/Y/Z
* Reportar posición
* Guardar historial de movimientos

Ejemplo:

```
HOME
X +50
Y +25
Z -5
```

---

## Machine Layer

Capa intermedia entre el software y el hardware.

Responsabilidades:

* Conectar máquina
* Ejecutar home
* Enviar movimientos
* Obtener estado

Flujo:

```
JobManager
     |
     v
 Machine
     |
     v
 Driver
```

---

## Job Manager v0.1

Primer sistema de ejecución de trabajos.

Funciones actuales:

* Cargar lista de movimientos
* Ejecutar secuencia
* Detener trabajo

Ejemplo:

Entrada:

```python
[
 {"axis":"X","distance":50},
 {"axis":"Y","distance":25},
 {"axis":"Z","distance":-5}
]
```

Salida:

```
X +50
Y +25
Z -5
```

---

# Pruebas realizadas

## Prueba local en Colab

Resultado:

```
Simulator connected
Homing completed
Job loaded: 3 commands

[
 {'axis': 'X', 'position': 50.0},
 {'axis': 'Y', 'position': 25.0},
 {'axis': 'Z', 'position': -5.0}
]

Estado:
X = 50
Y = 25
Z = -5
```

---

# Validación importante

Se realizó una prueba desde cero:

1. Clonar repositorio desde GitHub.
2. Abrir en Google Colab.
3. Importar módulos.
4. Ejecutar máquina simulada.

Resultado:

✅ Proyecto recuperable desde GitHub
✅ Sin depender de archivos temporales de Colab
✅ Arquitectura funcionando

---

# Próximo objetivo

## v0.5 — Basic G-code Parser

Crear flujo:

```
Archivo .nc
     |
     v
G-code Parser
     |
     v
Job Manager
     |
     v
Machine
     |
     v
CNC
```

Primeros comandos soportados:

```
G0 X50
G0 Y25
G1 Z-5
```

Convertirlos a movimientos:

```python
[
 {"axis":"X","distance":50},
 {"axis":"Y","distance":25},
 {"axis":"Z","distance":-5}
]
```

---

# Próximas mejoras futuras

* Parser G-code completo
* Control de velocidad
* Pausa / continuar trabajos
* Comunicación serial con Arduino
* Interfaz gráfica
* Visualizador 3D de trayectorias
* Control real de motores paso a paso

---

# Último estado conocido

Proyecto detenido en:

**v0.4 estable**

Listo para comenzar:


## v0.5 - Basic G-code Parser

Status: Completed

Implemented:

- G-code file reader
- Basic G-code parser
- Support for G0 and G1 commands
- Conversion from G-code to machine commands
- Execution through JobManager
- Simulator execution from .nc files
- Integration tests

Validated program:

```gcode
; PyCNC Studio test program

G0 X50
G0 Y25
G1 Z-5


Simulation result:

X = 50
Y = 25
Z = -5

Tests:

8 passed

PyCNC Studio — Estado del proyecto

Repositorio:
GitHub: https://github.com/KaworuSSSS/PyCNC-Studio

Forma de trabajo:
- Desarrollo desde GitHub usando navegador.
- Pruebas ejecutadas en Google Colab clonando el repositorio.
- Cada cambio se prueba con pytest antes de continuar.

Estado actual:
v0.6.x — Motion Planner integrado con JobManager

Última prueba realizada:

============================== 11 passed ==============================

Arquitectura actual:

Archivo .nc
    |
    v
GCodeFileReader
    |
    v
GCodeParser
    |
    v
MotionPlanner
    |
    v
JobManager
    |
    v
Machine
    |
    v
CNCSimulator


Estructura actual:

app/
|
├── drivers/
│   ├── cnc_driver.py
│   └── simulator_driver.py
│
├── machine/
│   └── machine.py
│
├── job/
│   ├── __init__.py
│   └── job_manager.py
│
├── gcode/
│   ├── parser.py
│   └── file_reader.py
│
├── planner/
│   ├── motion_planner.py
│   └── __init__.py
│
├── comm/
│   └── communication.py
│
├── core/
│
├── simulator/
│
└── gui/


Funcionamiento actual:

1) GCodeParser

Convierte:

G0 X50

en:

{
 "command":"G0",
 "parameters":{
    "X":50
 }
}


2) MotionPlanner

Mantiene posición interna:

{
 "X":0,
 "Y":0,
 "Z":0
}

Convierte comandos en posiciones objetivo:

{
 "command":"G0",
 "target":{
    "X":50,
    "Y":0,
    "Z":0
 }
}


Ejemplo:

Entrada:

G0 X50
G0 Y25
G1 Z-5

Salida:

[
{
 "command":"G0",
 "target":{
    "X":50,
    "Y":0,
    "Z":0
 }
},
{
 "command":"G0",
 "target":{
    "X":50,
    "Y":25,
    "Z":0
 }
},
{
 "command":"G1",
 "target":{
    "X":50,
    "Y":25,
    "Z":-5
 }
}
]


3) JobManager

Ahora recibe movimientos del MotionPlanner.

Convierte posiciones objetivo en movimientos relativos:

Ejemplo:

Posición actual:

X0 Y0 Z0

Target:

X50 Y25 Z0

Ejecuta:

machine.jog("X",50)
machine.jog("Y",25)


4) Machine

Capa intermedia:

JobManager
     |
     v
Machine
     |
     v
Driver


5) CNCSimulator

Actualmente funciona:

- connect()
- disconnect()
- home()
- move_relative()
- get_status()

Ejemplo:

HOME

X +50

Y +25

Z -5


Tests actuales:

tests/
├── test_communication.py
├── test_gcode.py
├── test_gcode_job.py
├── test_machine.py
├── test_motion_planner.py
└── test_simulator.py


Todos pasan:

11 tests OK


Último cambio importante:

feat: integrate motion planner with job manager


Próximo objetivo pendiente:

v0.6.4 — Implementar modos CNC G90/G91

Objetivo:

G90 = coordenadas absolutas

Ejemplo:

G90
G0 X50
G0 X60

Resultado:

X50
X60


G91 = coordenadas relativas

Ejemplo:

G91
G0 X50
G0 X60

Resultado:

X50
X110


Plan para continuar:

1. Crear tests nuevos en:
tests/test_motion_planner.py

2. Hacer fallar los tests.

3. Modificar:
app/planner/motion_planner.py

4. Ejecutar:

pytest

5. Mantener todos los tests verdes.


Último punto exacto donde continuar:

Abrir:

tests/test_motion_planner.py

y comenzar implementación de G90/G91.
