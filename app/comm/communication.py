"""
PyCNC Studio
Communication Layer

Maneja la comunicación entre el software
y los controladores CNC.
"""


class Communication:


    def __init__(self):

        self.connected = False
        self.messages = []



    def connect(self):

        self.connected = True

        return "Communication ready"



    def disconnect(self):

        self.connected = False

        return "Communication closed"



    def send(self, command):

        if not self.connected:

            return "Not connected"


        self.messages.append(command)

        return {
            "sent": command,
            "status": "OK"
        }



    def receive(self):

        if len(self.messages) == 0:

            return None


        return self.messages.pop(0)
