import pytest

from app.drivers.cnc_simulator import CNCSimulator


def test_simulator_starts_disconnected():

    simulator = CNCSimulator()

    status = simulator.get_status()

    assert status["connected"] is False


def test_simulator_connects():

    simulator = CNCSimulator()

    result = simulator.connect()

    assert result is True

    status = simulator.get_status()

    assert status["connected"] is True


def test_simulator_disconnects():

    simulator = CNCSimulator()

    simulator.connect()

    result = simulator.disconnect()

    assert result is True

    status = simulator.get_status()

    assert status["connected"] is False


def test_simulator_starts_at_origin():

    simulator = CNCSimulator()

    status = simulator.get_status()

    assert status["position"] == {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0,
    }


def test_simulator_moves_to_absolute_position():

    simulator = CNCSimulator()

    simulator.connect()

    result = simulator.move_absolute(
        x=50.0,
        y=20.0,
        z=-2.0,
    )

    assert result is True

    status = simulator.get_status()

    assert status["position"] == {
        "x": 50.0,
        "y": 20.0,
        "z": -2.0,
    }


def test_simulator_moves_relative():

    simulator = CNCSimulator()

    simulator.connect()

    simulator.move_absolute(
        x=10.0,
        y=20.0,
        z=5.0,
    )

    result = simulator.move_relative(
        axis="X",
        distance=5.0,
    )

    assert result is True

    status = simulator.get_status()

    assert status["position"] == {
        "x": 15.0,
        "y": 20.0,
        "z": 5.0,
    }


def test_simulator_records_toolpath():

    simulator = CNCSimulator()

    simulator.connect()

    simulator.move_absolute(
        x=10.0,
        y=20.0,
        z=5.0,
    )

    simulator.move_absolute(
        x=50.0,
        y=20.0,
        z=5.0,
    )

    toolpath = simulator.get_toolpath()

    assert len(toolpath) == 2
