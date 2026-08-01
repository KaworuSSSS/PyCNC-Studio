# Driver Architecture


PyCNC Studio separates machine logic from hardware implementation.


Architecture:


Machine

↓

CNCDriver

↓

SimulatorDriver / ArduinoDriver


Current drivers:

- SimulatorDriver

Future drivers:

- Arduino
- GRBL
- ESP32
