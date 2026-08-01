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

**v0.5 — G-code Parser**
