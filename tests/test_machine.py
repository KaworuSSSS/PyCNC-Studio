"""
Tests for Machine Controller
"""


from app.machine.machine import Machine
from app.drivers.simulator_driver import CNCSimulator



def test_machine_connection():

    machine = Machine(
        CNCSimulator()
    )

    result = machine.connect()

    assert result == "Simulator connected"



def test_machine_jog():

    machine = Machine(
        CNCSimulator()
    )

    machine.connect()

    machine.jog("Y",25)

    status = machine.status()

    assert status["position"]["Y"] == 25
