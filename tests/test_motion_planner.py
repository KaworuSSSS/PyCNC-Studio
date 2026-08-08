"""
Tests for Motion Planner
"""

from app.planner.motion_planner import MotionPlanner


def test_basic_motion_plan():

    planner = MotionPlanner()

    commands = [
        {
            "command": "G0",
            "parameters": {
                "X": 50
            }
        },
        {
            "command": "G0",
            "parameters": {
                "Y": 25
            }
        },
        {
            "command": "G1",
            "parameters": {
                "Z": -5
            }
        }
    ]

    result = planner.plan(commands)

    assert result == [
        {
            "command": "G0",
            "target": {
                "X": 50,
                "Y": 0.0,
                "Z": 0.0
            }
        },
        {
            "command": "G0",
            "target": {
                "X": 50,
                "Y": 25,
                "Z": 0.0
            }
        },
        {
            "command": "G1",
            "target": {
                "X": 50,
                "Y": 25,
                "Z": -5
            }
        }
    ]


def test_planner_tracks_position():

    planner = MotionPlanner()

    commands = [
        {
            "command": "G0",
            "parameters": {
                "X": 50
            }
        },
        {
            "command": "G0",
            "parameters": {
                "Y": 25
            }
        },
        {
            "command": "G1",
            "parameters": {
                "X": 60
            }
        }
    ]

    planner.plan(commands)

    assert planner.position["X"] == 60
    assert planner.position["Y"] == 25
    assert planner.position["Z"] == 0.0


def test_planner_generates_target_positions():

    planner = MotionPlanner()

    commands = [
        {
            "command": "G0",
            "parameters": {
                "X": 50
            }
        },
        {
            "command": "G0",
            "parameters": {
                "Y": 25
            }
        }
    ]

    result = planner.plan(commands)

    assert result[0]["target"] == {
        "X": 50,
        "Y": 0.0,
        "Z": 0.0
    }

    assert result[1]["target"] == {
        "X": 50,
        "Y": 25,
        "Z": 0.0
    }


def test_g90_absolute_mode():

    planner = MotionPlanner()

    commands = [
        {
            "command": "G90"
        },
        {
            "command": "G0",
            "parameters": {
                "X": 50
            }
        },
        {
            "command": "G0",
            "parameters": {
                "X": 60
            }
        }
    ]

    result = planner.plan(commands)

    assert result[0]["target"]["X"] == 50
    assert result[1]["target"]["X"] == 60


def test_g91_relative_mode():

    planner = MotionPlanner()

    commands = [
        {
            "command": "G91"
        },
        {
            "command": "G0",
            "parameters": {
                "X": 50
            }
        },
        {
            "command": "G0",
            "parameters": {
                "X": 60
            }
        }
    ]

    result = planner.plan(commands)

    assert result[0]["target"]["X"] == 50
    assert result[1]["target"]["X"] == 110


def test_feed_rate_tracking():

    planner = MotionPlanner()

    commands = [
        {
            "command": "G1",
            "parameters": {
                "X": 50,
                "F": 500
            }
        }
    ]

    result = planner.plan(commands)

    assert result[0]["feed_rate"] == 500


def test_g21_millimeter_mode():

    planner = MotionPlanner()

    commands = [
        {
            "command": "G21"
        },
        {
            "command": "G0",
            "parameters": {
                "X": 50
            }
        }
    ]

    result = planner.plan(commands)

    assert result[0]["target"]["X"] == 50


def test_g20_inch_mode():

    planner = MotionPlanner()

    commands = [
        {
            "command": "G20"
        },
        {
            "command": "G0",
            "parameters": {
                "X": 1
            }
        }
    ]

    result = planner.plan(commands)

    assert result[0]["target"]["X"] == 25.4


def test_g92_set_position():

    planner = MotionPlanner()

    commands = [
        {
            "command": "G0",
            "parameters": {
                "X": 50
            }
        },
        {
            "command": "G92",
            "parameters": {
                "X": 0
            }
        }
    ]

    planner.plan(commands)

    assert planner.position["X"] == 0


def test_g92_after_offset_move():

    planner = MotionPlanner()

    commands = [
        {
            "command": "G92",
            "parameters": {
                "X": 100
            }
        },
        {
            "command": "G0",
            "parameters": {
                "X": 110
            }
        }
    ]

    result = planner.plan(commands)

    assert result[0]["target"]["X"] == 110


def test_coordinate_mode_can_change_during_job():

    planner = MotionPlanner()

    commands = [
        {
            "command": "G90"
        },
        {
            "command": "G0",
            "parameters": {
                "X": 50
            }
        },
        {
            "command": "G91"
        },
        {
            "command": "G0",
            "parameters": {
                "X": 10
            }
        },
        {
            "command": "G90"
        },
        {
            "command": "G0",
            "parameters": {
                "X": 100
            }
        }
    ]

    result = planner.plan(commands)

    assert result[0]["target"]["X"] == 50
    assert result[1]["target"]["X"] == 60
    assert result[2]["target"]["X"] == 100


def test_units_can_change_during_job():

    planner = MotionPlanner()

    commands = [
        {
            "command": "G21"
        },
        {
            "command": "G0",
            "parameters": {
                "X": 10
            }
        },
        {
            "command": "G20"
        },
        {
            "command": "G0",
            "parameters": {
                "X": 1
            }
        },
        {
            "command": "G21"
        },
        {
            "command": "G0",
            "parameters": {
                "X": 20
            }
        }
    ]

    result = planner.plan(commands)

    assert result[0]["target"]["X"] == 10
    assert result[1]["target"]["X"] == 25.4
    assert result[2]["target"]["X"] == 20


def test_g92_redefines_coordinate_system():

    planner = MotionPlanner()

    commands = [
        {
            "command": "G0",
            "parameters": {
                "X": 50
            }
        },
        {
            "command": "G92",
            "parameters": {
                "X": 0
            }
        },
        {
            "command": "G0",
            "parameters": {
                "X": 25
            }
        }
    ]

    result = planner.plan(commands)

    assert planner.position["X"] == 25
    assert result[0]["target"]["X"] == 50
    assert result[1]["target"]["X"] == 25

