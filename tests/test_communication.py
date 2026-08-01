"""
Communication tests
"""


from app.comm.communication import Communication



def test_connect():

    comm = Communication()

    result = comm.connect()

    assert result == "Communication ready"



def test_send():

    comm = Communication()

    comm.connect()

    result = comm.send("G0 X10")


    assert result["status"] == "OK"
