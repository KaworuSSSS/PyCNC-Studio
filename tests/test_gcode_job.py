"""
Tests for G-code Job execution
"""


from app.gcode.file_reader import GCodeFileReader
from app.gcode.parser import GCodeParser
from app.planner.motion_planner import MotionPlanner
from app.job.job_manager import JobManager
from app.machine.machine import Machine
from app.drivers.simulator_driver import CNCSimulator



def test_gcode_job_execution():


    # Crear máquina simulada

    driver = CNCSimulator()

    machine = Machine(driver)


    machine.connect()

    machine.home()



    # Leer archivo G-code

    reader = GCodeFileReader()

    lines = reader.load(
        "examples/test.nc"
    )



    # Parsear G-code

    parser = GCodeParser()

    commands = parser.parse(lines)



    # Planificar movimientos

    planner = MotionPlanner()

    movements = planner.plan(commands)



    # Ejecutar Job

    job = JobManager(machine)


    result = job.load(movements)


    assert result == "Job loaded: 3 commands"



    output = job.start()



    status = machine.status()



    assert status["position"]["X"] == 50

    assert status["position"]["Y"] == 25

    assert status["position"]["Z"] == -5
