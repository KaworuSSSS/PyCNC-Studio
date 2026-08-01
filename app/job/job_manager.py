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

        for command in self.commands:

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
