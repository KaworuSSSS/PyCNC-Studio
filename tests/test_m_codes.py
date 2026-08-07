"""
Tests for CNC M-Codes
"""

from app.planner.motion_planner import MotionPlanner



def test_m0_pause():

    planner = MotionPlanner()

    commands = [
        {
            "command": "M0"
        }
    ]

    result = planner.plan(commands)

    assert result[0]["command"] == "M0"
    assert result[0]["action"] == "pause"



def test_m2_program_end():

    planner = MotionPlanner()

    commands = [
        {
            "command": "M2"
        }
    ]

    result = planner.plan(commands)

    assert result[0]["command"] == "M2"
    assert result[0]["action"] == "program_end"



def test_m3_spindle_on():

    planner = MotionPlanner()

    commands = [
        {
            "command": "M3",
            "parameters": {
                "S": 1000
            }
        }
    ]

    result = planner.plan(commands)

    assert result[0]["command"] == "M3"
    assert result[0]["spindle_speed"] == 1000



def test_m5_spindle_off():

    planner = MotionPlanner()

    commands = [
        {
            "command": "M5"
        }
    ]

    result = planner.plan(commands)

    assert result[0]["command"] == "M5"
    assert result[0]["action"] == "spindle_stop"
