"""
G-Code file reader
"""


class GCodeFileReader:


    def load(self, filename):

        with open(filename,"r") as file:

            lines = file.readlines()


        return lines
