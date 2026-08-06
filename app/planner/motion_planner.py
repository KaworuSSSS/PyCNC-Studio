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

            # Actualizar posición según el modo activo
            for axis, value in command["parameters"].items():

                if axis not in ["X", "Y", "Z"]:
                    continue

                if self.coordinate_mode == "absolute":
                    self.position[axis] = value

                else:  # G91
                    self.position[axis] += value

            # Crear movimiento con la posición completa
            movements.append(
                {
                    "command": gcode,
                    "target": {
                        "X": self.position["X"],
                        "Y": self.position["Y"],
                        "Z": self.position["Z"],
                    },
                }
            )

        return movements


        return movements


from app.planner.motion_planner import MotionPlanner


def test_g90_absolute_mode():

    planner = MotionPlanner()

    commands = [
        {"command": "G90"},
        {"command": "G0", "parameters": {"X": 50}},
        {"command": "G0", "parameters": {"X": 60}},
    ]

    result = planner.plan(commands)

    assert result[0]["target"]["X"] == 50
    assert result[1]["target"]["X"] == 60


def test_g91_relative_mode():

    planner = MotionPlanner()

    commands = [
        {"command": "G91"},
        {"command": "G0", "parameters": {"X": 50}},
        {"command": "G0", "parameters": {"X": 60}},
    ]

    result = planner.plan(commands)

    assert result[0]["target"]["X"] == 50
    assert result[1]["target"]["X"] == 110
