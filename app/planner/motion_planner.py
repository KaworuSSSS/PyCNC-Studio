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
            "Z": 0.0,
        }

        # G90 por defecto
        self.coordinate_mode = "absolute"

        # Feed rate actual
        self.feed_rate = None


    def plan(self, commands):

        movements = []


        for command in commands:

            gcode = command.get("command")


            # Cambiar modo de coordenadas

            if gcode == "G90":

                self.coordinate_mode = "absolute"
                continue


            elif gcode == "G91":

                self.coordinate_mode = "relative"
                continue


            if "parameters" not in command:

                continue



            # Procesar parámetros

            for axis, value in command["parameters"].items():


                # Feed rate

                if axis == "F":

                    self.feed_rate = value
                    continue



                # Ejes CNC

                if axis not in ["X", "Y", "Z"]:

                    continue



                if self.coordinate_mode == "absolute":

                    self.position[axis] = value


                else:

                    # G91 relativo

                    self.position[axis] += value



            movement = {

                "command": gcode,

                "target": {

                    "X": self.position["X"],

                    "Y": self.position["Y"],

                    "Z": self.position["Z"]

                },

                "feed_rate": self.feed_rate

            }


            movements.append(movement)



        return movements
