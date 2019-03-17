import constants
import requests

registry_host = constants.REGISTRY_IP + ":" + REGISTRY_PORT


def request_group_coordinator(group_id):
    url = registry_host + "/API/groups/" + group_id
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        data = response.json()
        return (True, data[constants.GID_KEY], data[constants.COORD_IP_KEY], data[constants.PID_KEY])
    elif response.status_code == '417':
        return (False, None, None, None)
    else:
        print(response)
        raise CommsError()


def request_create_group(group_id, process_id):
    url = registry_host + "/API/groups"
    payload = {constants.GID_KEY: group_id, constants.PID_KEY: process_id}
    response = requests.post(url, params=payload)
    if response.status_code == requests.codes.ok:
        data = response.json()
        return (True, data[constants.GID_KEY], data[constants.COORD_IP_KEY], data[constants.PID_KEY])
    elif response.status_code == '417':
        return (False, None, None, None)
    else:
        print(response)
        raise CommsError()


def request_join_group(coordinator_ip, coordinator_process_id, group_id, process_id):
    url = coordinator_ip + ":" + constants.CLIENT_PORT + "/API/processes/" + coordinator_process_id + "coordinate/groups" + group_id
    payload = {constants.PID_KEY: process_id}
    response = requests.post(url, params=payload)
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data[constants.GID_KEY]
    elif response.status_code == '417':
        return (False, None, None, None)
    else:
        print(response)
        raise CommsError()


def init():
    return


class CommsError(Exception):
    """Base class for any comms exception that deviate from happy path"""
    pass
