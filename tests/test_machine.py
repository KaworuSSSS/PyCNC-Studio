"""
Tests for Machine Controller
"""


from app.machine.machine import Machine



def test_machine_connection():

    machine = Machine()

    result = machine.connect()

    assert result == "Simulator connected"



def test_machine_jog():

    machine = Machine()

    machine.connect()

    machine.jog("Y",25)

    status = machine.status()

    assert status["position"]["Y"] == 25
