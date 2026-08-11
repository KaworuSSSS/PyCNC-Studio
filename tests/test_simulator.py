"""
Tests for CNC Simulator
"""


from app.drivers.simulator_driver import CNCSimulator



def test_connection():

    cnc = CNCSimulator()

    result = cnc.connect()

    assert result == "Simulator connected"



def test_move():

    cnc = CNCSimulator()

    cnc.connect()

    cnc.move_relative("X", 50)

    status = cnc.get_status()

    assert status["position"]["X"] == 50
def test_simulator_records_toolpath():

    cnc = CNCSimulator()

    cnc.connect()

    cnc.move_relative("X", 50)
    cnc.move_relative("Y", 25)
    cnc.move_relative("Z", -5)

    toolpath = cnc.get_toolpath()

    assert toolpath == [
        {
            "X": 50.0,
            "Y": 0.0,
            "Z": 0.0
        },
        {
            "X": 50.0,
            "Y": 25.0,
            "Z": 0.0
        },
        {
            "X": 50.0,
            "Y": 25.0,
            "Z": -5.0
        }
    ]
