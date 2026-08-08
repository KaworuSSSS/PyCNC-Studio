from app.drivers.cnc_simulator import CNCSimulator
from app.visualization.cnc_view import CNCView


simulator = CNCSimulator()

simulator.connect()

simulator.move_absolute(
    x=10,
    y=10,
    z=15,
)

simulator.move_absolute(
    x=80,
    y=10,
    z=15,
)

simulator.move_absolute(
    x=80,
    y=45,
    z=15,
)

simulator.move_absolute(
    x=10,
    y=45,
    z=15,
)

simulator.move_absolute(
    x=10,
    y=10,
    z=15,
)


viewer = CNCView(simulator)

viewer.show()
