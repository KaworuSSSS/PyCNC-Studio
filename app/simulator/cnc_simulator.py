"""
PyCNC Studio
CNC Simulator Module

Simula una máquina CNC básica.
"""


class CNCSimulator:

    def __init__(self):

        self.position = {
            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0
        }

        self.state = "DISCONNECTED"


    def connect(self):

        self.state = "READY"

        return "Simulator connected"


    def disconnect(self):

        self.state = "DISCONNECTED"

        return "Simulator disconnected"


    def home(self):

        self.position["X"] = 0.0
        self.position["Y"] = 0.0
        self.position["Z"] = 0.0

        return "Homing completed"


    def move(self, axis, distance):

        if axis not in self.position:
            return "Invalid axis"


        self.position[axis] += distance

        return {
            "axis": axis,
            "position": self.position[axis]
        }


    def get_status(self):

        return {
            "state": self.state,
            "position": self.position
        }
