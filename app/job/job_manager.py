"""
PyCNC Studio
Job Manager

Executes planned CNC movements.
"""


class JobManager:


    def __init__(self, machine):

        self.machine = machine
        self.commands = []
        self.running = False



    def load(self, commands):

        self.commands = commands

        return f"Job loaded: {len(commands)} commands"



    def start(self):

        if not self.commands:

            return "No job loaded"



        self.running = True

        results = []



        current_position = {

            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0

        }



        for command in self.commands:



            # Nuevo formato MotionPlanner

            if "target" in command:


                target = command["target"]



                for axis in ["X", "Y", "Z"]:


                    if target[axis] != current_position[axis]:


                        distance = (
                            target[axis]
                            -
                            current_position[axis]
                        )


                        result = self.machine.jog(

                            axis,

                            distance

                        )


                        results.append(result)



                        current_position[axis] = target[axis]



            # Compatibilidad v0.4

            elif "axis" in command:


                axis = command["axis"]

                distance = command["distance"]


                result = self.machine.jog(

                    axis,

                    distance

                )


                results.append(result)



            # Compatibilidad directa G-code parser

            elif "parameters" in command:


                for axis, value in command["parameters"].items():


                    if axis in ["X", "Y", "Z"]:


                        result = self.machine.jog(

                            axis,

                            value

                        )


                        results.append(result)



        self.running = False


        return results



    def stop(self):

        self.running = False

        return "Job stopped"
