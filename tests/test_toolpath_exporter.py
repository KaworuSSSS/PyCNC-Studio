import json

from app.drivers.simulator_driver import CNCSimulator
from app.machine.machine import Machine
from app.job.job_manager import JobManager
from app.export.toolpath_exporter import ToolpathExporter


def test_toolpath_exporter_creates_json():

    driver = CNCSimulator()

    machine = Machine(driver)

    machine.connect()
    machine.home()

    job = JobManager(machine)

    commands = [
        {
            "command": "G0",
            "target": {
                "X": 20,
                "Y": 10,
                "Z": 0
            }
        },
        {
            "command": "G1",
            "target": {
                "X": 50,
                "Y": 10,
                "Z": -5
            }
        },
        {
            "command": "G1",
            "target": {
                "X": 50,
                "Y": 40,
                "Z": -5
            }
        }
    ]

    job.load(commands)

    job.start()

    exporter = ToolpathExporter()

    result = exporter.to_json(
        job.toolpath
    )

    data = json.loads(result)

    assert data == [
        {
            "X": 20,
            "Y": 10,
            "Z": 0
        },
        {
            "X": 50,
            "Y": 10,
            "Z": -5
        },
        {
            "X": 50,
            "Y": 40,
            "Z": -5
        }
    ]
