from abc import ABC, abstractmethod


class CNCDriver(ABC):

    @abstractmethod
    def connect(self):
        pass


    @abstractmethod
    def disconnect(self):
        pass


    @abstractmethod
    def home(self):
        pass


    @abstractmethod
    def move_relative(self, axis, distance):
        pass


    @abstractmethod
    def get_status(self):
        pass
