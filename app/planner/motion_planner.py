"""
PyCNC Studio
Motion Planner

Converts parsed G-code commands
into machine movements.
"""


class MotionPlanner:

    def __init__(self):

        # Posición actual de la máquina
        # Se utilizará en futuras versiones
        # para soportar G90, G91 y trayectorias.
        self.position = {
            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0
        }

    def plan(self, commands):

        movements = []


        for command in commands:

            if "parameters" in command:


                for axis, distance in command["parameters"].items():


                    if axis in ["X", "Y", "Z"]:

                        movements.append(
                            {
                                "axis": axis,
                                "distance": distance
                            }
                        )


        return movements
