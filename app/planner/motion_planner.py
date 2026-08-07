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

        self.coordinate_mode = "absolute"

        self.feed_rate = None

        self.units = "mm"

        # G92 offsets
        self.offset = {
            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0,
        }


    def plan(self, commands):

        movements = []


        for command in commands:

            gcode = command.get("command")


            if gcode == "G90":

                self.coordinate_mode = "absolute"
                continue


            elif gcode == "G91":

                self.coordinate_mode = "relative"
                continue


            elif gcode == "G20":

                self.units = "inch"
                continue


            elif gcode == "G21":

                self.units = "mm"
                continue


            elif gcode == "G92":

                for axis, value in command["parameters"].items():

                    if axis in ["X", "Y", "Z"]:

                        self.offset[axis] = (
                            self.position[axis] - value
                        )

                continue



            if "parameters" not in command:

                continue



            for axis, value in command["parameters"].items():


                if axis == "F":

                    self.feed_rate = value
                    continue



                if axis not in ["X", "Y", "Z"]:

                    continue



                if self.units == "inch":

                    value = value * 25.4



                if self.coordinate_mode == "absolute":

                    self.position[axis] = (
                        value + self.offset[axis]
                    )

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
