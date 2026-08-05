class JobManager:


    def __init__(self, machine, planner=None):
    
        self.machine = machine
        self.planner = planner
    
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


        for command in self.commands:


            # Formato nuevo proveniente del G-Code Parser
            #
            # Ejemplo:
            # {
            #   "command": "G1",
            #   "parameters": {
            #       "X":50,
            #       "Y":25
            #   }
            # }

            if "parameters" in command:


                for axis, distance in command["parameters"].items():


                    # Solo ejecutar movimientos CNC

                    if axis in ["X", "Y", "Z"]:


                        result = self.machine.jog(
                            axis,
                            distance
                        )


                        results.append(result)



            # Formato antiguo v0.4
            #
            # Ejemplo:
            # {
            #   "axis":"X",
            #   "distance":50
            # }

            else:


                axis = command["axis"]

                distance = command["distance"]


                result = self.machine.jog(
                    axis,
                    distance
                )


                results.append(result)



        self.running = False


        return results



    def stop(self):

        self.running = False

        return "Job stopped"
