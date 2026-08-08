class CNCSimulator:

    def __init__(self):

        self.connected = False

        self.position = {
            "x": 0.0,
            "y": 0.0,
            "z": 0.0,
        }

        self.toolpath = []

    def connect(self):

        self.connected = True

        return True

    def disconnect(self):

        self.connected = False

        return True

    def move_absolute(self, x, y, z):

        self.position = {
            "x": float(x),
            "y": float(y),
            "z": float(z),
        }

        self.toolpath.append(
            self.position.copy()
        )

        return True

    def move_relative(self, axis, distance):

        axis = axis.lower()

        if axis not in ("x", "y", "z"):

            raise ValueError(
                f"Unsupported axis '{axis}'"
            )

        self.position[axis] += float(distance)

        self.toolpath.append(
            self.position.copy()
        )

        return True

    def get_status(self):

        return {
            "connected": self.connected,
            "position": self.position.copy(),
        }

    def get_toolpath(self):

        return list(self.toolpath)
