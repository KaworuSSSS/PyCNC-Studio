"""
PyCNC Studio
Machine Controller

Control principal de la máquina CNC.
"""


from app.simulator.cnc_simulator import CNCSimulator



class Machine:


    def __init__(self):

        # Driver por defecto
        # Más adelante será intercambiable
        self.driver = CNCSimulator()



    def connect(self):

        return self.driver.connect()



    def disconnect(self):

        return self.driver.disconnect()



    def home(self):

        return self.driver.home()



    def jog(self, axis, distance):

        return self.driver.move(axis, distance)



    def status(self):

        return self.driver.get_status()
