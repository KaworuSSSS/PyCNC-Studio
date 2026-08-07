"""
G-Code Parser Tests
"""

from app.gcode.parser import GCodeParser


def test_gcode_move():

    parser = GCodeParser()

    result = parser.parse_line(
        "G1 X50 Y20 F800"
    )

    assert result["command"] == "G1"
    assert result["parameters"]["X"] == 50
    assert result["parameters"]["Y"] == 20
    assert result["parameters"]["F"] == 800


def test_gcode_comment():

    parser = GCodeParser()

    result = parser.parse_line("; This is a comment")

    assert result is None


def test_empty_line():

    parser = GCodeParser()

    result = parser.parse_line("")

    assert result is None


def test_feed_rate_parameter():

    parser = GCodeParser()

    result = parser.parse_line("G1 X10 F500")

    assert result["command"] == "G1"
    assert result["parameters"]["X"] == 10
    assert result["parameters"]["F"] == 500
