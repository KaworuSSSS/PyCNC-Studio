"""
PyCNC Studio
Motion Planner

Converts parsed G-code commands
into machine target positions.
"""


class MotionPlanner:


    def __init__(self):

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


                if axis in ["X", "Y", "Z"]:

                    # Actualizar posición interna

                    self.position[axis] = value



            # Crear movimiento con posición completa

            movements.append(
                {
                    "command": command["command"],

                    "target": {

                        "X": self.position["X"],

                        "Y": self.position["Y"],

                        "Z": self.position["Z"]

                    }
                }
            )


        return movements
