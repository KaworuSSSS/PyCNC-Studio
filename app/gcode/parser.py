"""
PyCNC Studio
G-Code Parser

Interpreta comandos CNC básicos.
"""


class GCodeParser:

    def parse(self, lines):

        commands = []

        for line in lines:

            result = self.parse_line(line)

            if result is not None:

                commands.append(result)

        return commands

    def parse_line(self, line):

        line = line.strip()

        if line == "":
            return None

        if line.startswith(";"):
            return None

        # Remove inline comments.
        if ";" in line:

            line = line.split(";", 1)[0].strip()

        if line == "":
            return None

        parts = line.split()

        command = parts[0]

        parameters = {}

        for item in parts[1:]:

            axis = item[0]

            if axis not in ["X", "Y", "Z", "F", "S"]:

                raise ValueError(
                    f"Unsupported parameter '{axis}'"
                )

            try:

                value = float(item[1:])

            except ValueError:

                raise ValueError(
                    f"Invalid value for parameter '{axis}'"
                )

            parameters[axis] = value

        return {
            "command": command,
            "parameters": parameters
        }
