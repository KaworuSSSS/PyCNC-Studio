from app.gcode.file_reader import GCodeFileReader
from app.gcode.parser import GCodeParser

from app.drivers.simulator_driver import CNCSimulator
from app.machine.machine import Machine
from app.job.job_manager import JobManager



def test_execute_gcode_file():


    reader = GCodeFileReader()


    lines = reader.load(
        "examples/test.nc"
    )


    parser = GCodeParser()


    commands = parser.parse(lines)



    machine = Machine(
        CNCSimulator()
    )


    machine.connect()

    machine.home()



    job = JobManager(machine)


    job.load(commands)

    job.start()



    status = machine.status()



    assert status["position"]["X"] == 50

    assert status["position"]["Y"] == 25

    assert status["position"]["Z"] == -5
