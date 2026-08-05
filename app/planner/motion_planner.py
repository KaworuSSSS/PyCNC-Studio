"""
PyCNC Studio
Motion Planner

Converts parsed G-code commands
into machine movements.
"""


class MotionPlanner:


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
