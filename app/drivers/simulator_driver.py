%%writefile PyCNC_Studio/app/drivers/simulator_driver.py

from app.drivers.cnc_driver import CNCDriver


class CNCSimulator(CNCDriver):

    def __init__(self):

        self.position = {
            "X":0.0,
            "Y":0.0,
            "Z":0.0
        }

        self.state = "DISCONNECTED"

        self.history = []


    def connect(self):

        self.state = "IDLE"

        return "Simulator connected"


    def disconnect(self):

        self.state = "DISCONNECTED"

        return "Simulator disconnected"


    def home(self):

        self.position = {
            "X":0.0,
            "Y":0.0,
            "Z":0.0
        }

        self.history.append("HOME")

        return "Homing completed"


    def move_relative(self, axis, distance):

        self.position[axis] += distance

        self.history.append(
            f"{axis} {distance:+}"
        )

        return {
            "axis":axis,
            "position":self.position[axis]
        }


    def get_status(self):

        return {
            "state":self.state,
            "position":self.position,
            "history":self.history
        }
