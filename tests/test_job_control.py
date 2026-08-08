```python
"""
Tests for CNC Job Control.
"""

from app.job.job_manager import JobManager
from app.machine.machine import Machine
from app.drivers.simulator_driver import CNCSimulator


def create_machine():

    driver = CNCSimulator()

    machine = Machine(driver)

    machine.connect()
    machine.home()

    return machine


def test_job_initial_status():

    machine = create_machine()

    job = JobManager(machine)

    assert job.status == "idle"
    assert job.current_line == 0
    assert job.progress == 0.0


def test_job_completes():

    machine = create_machine()

    job = JobManager(machine)

    commands = [
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
        }
    ]

    job.load(commands)

    job.start()

    assert job.status == "completed"
    assert job.current_line == 2
    assert job.progress == 100.0


def test_job_pauses_on_m0():

    machine = create_machine()

    job = JobManager(machine)

    commands = [
        {
            "command": "G0",
            "target": {
                "X": 50,
                "Y": 0.0,
                "Z": 0.0
            }
        },
        {
            "command": "M0",
            "action": "pause"
        },
        {
            "command": "G0",
            "target": {
                "X": 100,
                "Y": 0.0,
                "Z": 0.0
            }
        }
    ]

    job.load(commands)

    job.start()

    status = machine.status()

    assert status["position"]["X"] == 50
    assert job.status == "paused"
    assert job.current_line == 2


def test_job_resume_after_m0():

    machine = create_machine()

    job = JobManager(machine)

    commands = [
        {
            "command": "G0",
            "target": {
                "X": 50,
                "Y": 0.0,
                "Z": 0.0
            }
        },
        {
            "command": "M0",
            "action": "pause"
        },
        {
            "command": "G0",
            "target": {
                "X": 100,
                "Y": 0.0,
                "Z": 0.0
            }
        }
    ]

    job.load(commands)

    job.start()

    assert job.status == "paused"

    job.resume()

    status = machine.status()

    assert status["position"]["X"] == 100
    assert job.status == "completed"
    assert job.current_line == 3
    assert job.progress == 100.0


def test_job_stop_while_paused():

    machine = create_machine()

    job = JobManager(machine)

    commands = [
        {
            "command": "G0",
            "target": {
                "X": 50,
                "Y": 0.0,
                "Z": 0.0
            }
        },
        {
            "command": "M0",
            "action": "pause"
        },
        {
            "command": "G0",
            "target": {
                "X": 100,
                "Y": 0.0,
                "Z": 0.0
            }
        }
    ]

    job.load(commands)

    job.start()

    assert job.status == "paused"

    job.stop()

    assert job.status == "stopped"
    assert job.current_line == 2


def test_job_stop_cannot_resume():

    machine = create_machine()

    job = JobManager(machine)

    commands = [
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
                "X": 100,
                "Y": 0.0,
                "Z": 0.0
            }
        }
    ]

    job.load(commands)

    job.start()

    job.stop()

    result = job.resume()

    assert job.status == "stopped"
    assert result == "Job is not paused"


def test_stopped_job_can_load_new_job():

    machine = create_machine()

    job = JobManager(machine)

    first_commands = [
        {
            "command": "G0",
            "target": {
                "X": 50,
                "Y": 0.0,
                "Z": 0.0
            }
        },
        {
            "command": "M0",
            "action": "pause"
        }
    ]

    job.load(first_commands)

    job.start()

    assert job.status == "paused"

    job.stop()

    assert job.status == "stopped"

    second_commands = [
        {
            "command": "G0",
            "target": {
                "X": 100,
                "Y": 0.0,
                "Z": 0.0
            }
        }
    ]

    result = job.load(second_commands)

    assert result == "Job loaded: 1 commands"
    assert job.status == "idle"
    assert job.current_line == 0
    assert job.progress == 0.0


def test_job_records_motion_path():

    machine = create_machine()

    job = JobManager(machine)

    commands = [
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
        }
    ]

    job.load(commands)

    job.start()

    assert job.toolpath == [
        {
            "X": 50,
            "Y": 0.0,
            "Z": 0.0
        },
        {
            "X": 50,
            "Y": 25,
            "Z": 0.0
        }
    ]
```



