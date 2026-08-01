"""
Tests for CNC Simulator
"""


from app.simulator.cnc_simulator import CNCSimulator



def test_connection():

    cnc = CNCSimulator()

    result = cnc.connect()

    assert result == "Simulator connected"



def test_move():

    cnc = CNCSimulator()

    cnc.connect()

    cnc.move("X", 50)

    status = cnc.get_status()

    assert status["position"]["X"] == 50
