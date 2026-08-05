"""
PyCNC Studio
Motion Planner

Converts parsed G-code commands
into machine movements.
"""


class MotionPlanner:

    def __init__(self):

        # Posición actual de la máquina
        self.position = {
            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0
        }

    def plan(self, commands):

        movements = []

        for command in commands:

            if "parameters" not in command:
                continue

            for axis, value in command["parameters"].items():

                # Solo procesamos ejes CNC
                if axis not in ["X", "Y", "Z"]:
                    continue

                # Actualizar posición interna
                self.position[axis] = value

                # Generar movimiento
                movements.append(
                    {
                        "axis": axis,
                        "distance": value
                    }
                )

        return movements
