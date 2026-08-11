from app.drivers.cnc_driver import CNCDriver


class CNCSimulator(CNCDriver):

    def __init__(self):

        self.position = {
            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0
        }

        self.state = "DISCONNECTED"

        self.history = []

        self.toolpath = []


    def connect(self):

        self.state = "IDLE"

        return "Simulator connected"


    def disconnect(self):

        self.state = "DISCONNECTED"

        return "Simulator disconnected"


    def home(self):

        self.position = {
            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0
        }

        self.history.append("HOME")

        self.toolpath.append(
            self.position.copy()
        )

        return "Homing completed"


    def move_relative(self, axis, distance):

        axis = axis.upper()

        if axis not in ("X", "Y", "Z"):

            raise ValueError(
                f"Unsupported axis '{axis}'"
            )

        self.position[axis] += float(distance)

        self.history.append(
            f"{axis} {distance:+}"
        )

        self.toolpath.append(
            self.position.copy()
        )

        return {
            "axis": axis,
            "position": self.position[axis]
        }


    def get_toolpath(self):

        return [
            position.copy()
            for position in self.toolpath
        ]


    def get_status(self):

        return {
            "state": self.state,
            "position": self.position,
            "history": self.history
        }
