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
