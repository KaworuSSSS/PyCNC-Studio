%%writefile PyCNC_Studio/app/machine/machine.py


class Machine:


    def __init__(self, driver):

        self.driver = driver



    def connect(self):

        return self.driver.connect()



    def home(self):

        return self.driver.home()



    def jog(self, axis, distance):

        return self.driver.move_relative(
            axis,
            distance
        )



    def status(self):

        return self.driver.get_status()
