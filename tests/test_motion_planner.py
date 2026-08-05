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
            "axis": "X",
            "distance": 50
        },

        {
            "axis": "Y",
            "distance": 25
        },

        {
            "axis": "Z",
            "distance": -5
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
    assert planner.position["Z"] == 0
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
        "Y": 0,
        "Z": 0
    }


    assert result[1]["target"] == {
        "X": 50,
        "Y": 25,
        "Z": 0
    }
