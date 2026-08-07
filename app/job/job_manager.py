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

        # Job control state
        self.status = "idle"
        self.current_line = 0
        self.progress = 0.0

        # Track the logical machine position used by the planner
        self.current_position = {
            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0
        }

    def load(self, commands):

        self.commands = commands

        self.running = False
        self.status = "idle"
        self.current_line = 0
        self.progress = 0.0

        self.current_position = {
            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0
        }

        return f"Job loaded: {len(commands)} commands"

    def _update_progress(self):

        if not self.commands:
            self.progress = 0.0
            return

        self.progress = (
            self.current_line / len(self.commands)
        ) * 100.0

    def _execute_command(self, command):

        # -------------------------------------------------
        # M0 - Program pause
        # -------------------------------------------------

        if command.get("command") == "M0":

            self.status = "paused"

            return "Job paused"

        # -------------------------------------------------
        # M2 - Program end
        # -------------------------------------------------

        if command.get("command") == "M2":

            self.status = "completed"

            return "Program ended"

        # -------------------------------------------------
        # M3 - Spindle on
        # -------------------------------------------------

        if command.get("command") == "M3":

            return "Spindle started"

        # -------------------------------------------------
        # M5 - Spindle off
        # -------------------------------------------------

        if command.get("command") == "M5":

            return "Spindle stopped"

        # -------------------------------------------------
        # MotionPlanner format
        #
        # {
        #     "command": "G0",
        #     "target": {
        #         "X": 50,
        #         "Y": 0,
        #         "Z": 0
        #     }
        # }
        # -------------------------------------------------

        if "target" in command:

            target = command["target"]

            for axis in ["X", "Y", "Z"]:

                target_value = target.get(
                    axis,
                    self.current_position[axis]
                )

                if target_value != self.current_position[axis]:

                    distance = (
                        target_value
                        - self.current_position[axis]
                    )

                    result = self.machine.jog(
                        axis,
                        distance
                    )

                    self.current_position[axis] = target_value

            return "Movement executed"

        # -------------------------------------------------
        # Compatibility with v0.4
        #
        # {
        #     "axis": "X",
        #     "distance": 50
        # }
        # -------------------------------------------------

        if "axis" in command:

            axis = command["axis"]
            distance = command["distance"]

            result = self.machine.jog(
                axis,
                distance
            )

            self.current_position[axis] += distance

            return result

        # -------------------------------------------------
        # Compatibility with direct G-code parser format
        #
        # {
        #     "parameters": {
        #         "X": 50,
        #         "Y": 25
        #     }
        # }
        # -------------------------------------------------

        if "parameters" in command:

            for axis, value in command["parameters"].items():

                if axis in ["X", "Y", "Z"]:

                    result = self.machine.jog(
                        axis,
                        value
                    )

                    self.current_position[axis] += value

            return "Movement executed"

        return None

    def start(self):

        if not self.commands:

            return "No job loaded"

        # If the job is paused, use resume()
        # instead of restarting it.
        if self.status == "paused":

            return "Job is paused"

        self.running = True
        self.status = "running"

        results = []

        while self.current_line < len(self.commands):

            command = self.commands[self.current_line]

            result = self._execute_command(command)

            # The command has now been processed.
            self.current_line += 1

            self._update_progress()

            if result is not None:

                results.append(result)

            # M0 pauses immediately after its line.
            if self.status == "paused":

                self.running = False

                return results

            # M2 ends the program.
            if self.status == "completed":

                self.running = False
                self.progress = 100.0

                return results

        # Normal end of program
        self.running = False
        self.status = "completed"

        self.current_line = len(self.commands)
        self.progress = 100.0

        return results

    def resume(self):

        if self.status != "paused":

            return "Job is not paused"

        self.running = True
        self.status = "running"

        results = []

        while self.current_line < len(self.commands):

            command = self.commands[self.current_line]

            result = self._execute_command(command)

            self.current_line += 1

            self._update_progress()

            if result is not None:

                results.append(result)

            # Another M0 can pause the job again.
            if self.status == "paused":

                self.running = False

                return results

            # M2 ends the program.
            if self.status == "completed":

                self.running = False
                self.progress = 100.0

                return results

        # Job finished after resume
        self.running = False
        self.status = "completed"

        self.current_line = len(self.commands)
        self.progress = 100.0

        return results

    def stop(self):

        self.running = False
        self.status = "stopped"

        return "Job stopped"
