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

        # G21 por defecto (milímetros)
        self.units = "mm"


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


            # Cambiar unidades

            elif gcode == "G20":

                self.units = "inch"
                continue


            elif gcode == "G21":

                self.units = "mm"
                continue



            if "parameters" not in command:

                continue



            for axis, value in command["parameters"].items():


                # Feed Rate

                if axis == "F":

                    self.feed_rate = value
                    continue



                # Ignorar otros parámetros

                if axis not in ["X", "Y", "Z"]:

                    continue



                # Conversión pulgadas -> mm

                if self.units == "inch":

                    value = value * 25.4



                # Movimiento absoluto

                if self.coordinate_mode == "absolute":

                    self.position[axis] = value



                # Movimiento relativo

                else:

                    self.position[axis] += value



            movement = {

                "command": gcode,

                "target": {

                    "X": self.position["X"],

                    "Y": self.position["Y"],

                    "Z": self.position["Z"]

                }

            }



            if self.feed_rate is not None:

                movement["feed_rate"] = self.feed_rate



            movements.append(movement)



        return movements
