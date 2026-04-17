from communication_control.SessionControl import NodeSessionControl
import pytest
import requests

URL = 'http://localhost:29083'

SENSOR_NAME = "SENSOR_NAME"

connect_message = {
    'name': 'NODE_1',
    'password': 'node1234',
}

not_auth = {
    'name': 'NOT_AUTH',
    'password': 'password',
}

node_details_message = {
    'location': 'LOCATION',
    'status': 'Online',
    'main_unit': 'MAIN UNIT',
}

sensor_details_message = {
    'name': 'SENSOR',
    'status': 'Online',
    'type': 'TEMPERATURE',
}

data_message = {
    "sensor_name": 'SENSOR',
    "value_type": "TEMPERATURE",
    "value":  20,
    "unit": "C",
    "max": 50,
    "error_message": None,
}

def test_node_communication(capsys):
    session: NodeSessionControl = NodeSessionControl(URL)

    session.connect('/api/nodeLogin', connect_message)

    assert session.isAuth
    assert 'Authorization' in session.headers
    captured = capsys.readouterr()
    assert captured.out == '200\n' 

    control = session.updateNode('/api/updateNode', node_details_message)

    assert control
    captured = capsys.readouterr()
    assert captured.out == '200\n'

    session.send('/api/updateSensors', sensor_details_message)

    captured = capsys.readouterr()
    assert captured.out == '200\n'

    session.send('/api/sendData', data_message)

    captured = capsys.readouterr()
    assert captured.out == '200\n'

def test_not_authenticated(capsys):
    session: NodeSessionControl = NodeSessionControl(URL)

    session.connect('/api/nodeLogin', not_auth)

    assert not session.isAuth
    assert 'Authorization' not in session.headers
    captured = capsys.readouterr()
    assert captured.out == '401\n' 

    response = requests.post(session.server + '/api/updateNode', json=node_details_message, headers=session.headers)

    assert 401 == response.status_code

    response = requests.post(session.server + '/api/updateSensors', json=sensor_details_message, headers=session.headers)

    assert 401 == response.status_code

    response = requests.post(session.server + '/api/sendData', json=data_message, headers=session.headers)

    assert 401 == response.status_code