"""
Represents a communications transmitter. A client only has one communication transmitter in charge of sending messages
Processes use client_comms_tx to send messages as a result of certain actions, such as creating a group
Every message received requires a process_id, so that the client can invoke the appropriate method on the right process
"""

import comms_errors
import constants
import requests
import json
import random
registry_host = "http://" + constants.REGISTRY_IP + ":" + constants.REGISTRY_PORT


def _request_group_coordinator(group_id):
    """
    Contacts the registry server to obtain metadata about a group, such as the coordinator's process id and its IP
    :param group_id: group related to the operation
    :return: True, and metadata if the registry server found information about the group; False, if according to the
    registry server the group doesn't exists. Raises an exception in all other cases in which the registry server's response
    is unsuccessful
    """
    if random.random() <= constants.MESSAGE_PROBAILITY:
        url = registry_host + "/API/groups/" + group_id
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            data = response.json()
            return True, data[constants.COORD_PID_KEY], data[constants.COORD_IP_KEY]
        elif response.status_code == comms_errors.GROUP_DOES_NOT_EXIST.status_code:
            return False, None, None
        else:
            print(response)
            raise CommsError()
    else:
        raise CommsError()
        return False


def _request_create_group(process_id, group_id):
    """
    Contacts the registry server to inform it that a new group should be created

    :param process_id:
    :param group_id:
    :return: True, and metadata if the registry server found information about the group; False, if according to the
    registry server the group doesn't exists. Raises an exception in all other cases in which the registry server's response
    is unsuccessful
    """

    if random.random() <= constants.MESSAGE_PROBAILITY:
        url = registry_host + "/API/groups"
        payload = {constants.GID_KEY: group_id, constants.PID_KEY: process_id}
        response = requests.post(url, params=payload)
        if response.status_code == requests.codes.ok:
            data = response.json()
            return True, data[constants.COORD_PID_KEY], data[constants.COORD_IP_KEY]
        elif response.status_code == comms_errors.GROUP_DOES_NOT_EXIST.status_code:
            return False, None, None
        else:
            print(response)
            raise CommsError()
    else:
        raise CommsError()
        return False


def _request_takeover_group(process_id, group_id, count):
    """
    Contacts the registry server to inform it that a process is trying to become new coordinator

    :param process_id:
    :param group_id:
    :param count, number of members this candidate has visibility over
    :return: True, if the registry server accepted the takeover request; False, if according to the
    registry server the candidate shouldn't take over. Raises an exception in all other cases in which the registry server's response
    is unsuccessful. Metadata is not useful per se, since it is the candidate's PID and IP
    """
    url = registry_host + "/API/groups"
    payload = {constants.GID_KEY: group_id, constants.PID_KEY: process_id}
    response = requests.put(url, params=payload)
    if response.status_code == requests.codes.ok:
        data = response.json()
        return True, data[constants.COORD_PID_KEY], data[constants.COORD_IP_KEY]
    elif response.status_code == comms_errors.GROUP_DOES_NOT_EXIST.status_code:
        return False, None, None
    else:
        print(response)
        raise CommsError()

def _request_join_group(coordinator_process_id, coordinator_ip, process_id, group_id):
    """
    Contacts the coordinator to inform that process with id process_id wants to join group with id group_id
    :param coordinator_process_id: the process that acts as coordinator for the group
    :param coordinator_ip:
    :param process_id: the process that wants to join the group
    :param group_id: the group the process wants to join
    :return group data structure for new group that they have joined or None, depending on result of request
    """
    if random.random() <= constants.MESSAGE_PROBAILITY:
        url = "http://" + coordinator_ip + ":" + constants.CLIENT_PORT + "/API/processes/" + coordinator_process_id + "/coordinate/groups/" + group_id
        payload = {constants.PID_KEY: process_id}
        response = requests.post(url, params=payload)
        if response.status_code == requests.codes.ok:
            return (True, json.loads(response.content.decode()))
        elif response.status_code == comms_errors.GROUP_DOES_NOT_EXIST.status_code:
            return (False, None)
        else:
            print(response)
            raise CommsError()
    else:
        raise CommsError()
        return False
    

def _request_leave_group(coordinator_process_id, coordinator_ip, process_id, group_id):
    """
    Contacts the coordinator to inform that process with id process_id wants to join group with id group_id
    :param coordinator_process_id: the process that acts as coordinator for the group
    :param coordinator_ip:
    :param process_id: the process that wants to leave the group
    :param group_id: the group the process wants to leave
    :return: True/False
    """
    if random.random() <= constants.MESSAGE_PROBAILITY:
        url = "http://" + coordinator_ip + ":" + constants.CLIENT_PORT + "/API/processes/" + coordinator_process_id + "/coordinate/groups/" + group_id
        payload = {constants.PID_KEY: process_id}
        response = requests.delete(url, params=payload)
        if response.status_code == requests.codes.ok:
            return True
        elif response.status_code == comms_errors.GROUP_DOES_NOT_EXIST.status_code:
            return False
        else:
            print(response)
            raise CommsError()
    else:
        raise CommsError()
        return False

def _request_first_stage_update(recipient_process_id, recipient_process_ip, new_group_state, group_id):
    """
    Contacts a given ip to tell them to enter first stage of commit protocol
    :param recipient_process_ip
    :param recipient_process_id
    :param new_group_state
    :param group_id
    """
    url = "http://" + recipient_process_ip + ":" + constants.CLIENT_PORT+ "/API/processes/" + recipient_process_id + "/groups/" + group_id 
    payload = new_group_state
    response = requests.put(url, data=json.dumps(payload), headers=constants.JSON_HEADER)
    if response.status_code == requests.codes.ok:
        return True
    elif response.status_code == comms_errors.PROCESS_NOT_AVAILABLE.status_code:
        return False
    else:
        print(response)
        raise CommsError()

def _request_second_stage_update(recipient_process_id, recipient_process_ip, group_id, operation):
    """
    Contacts a given ip to tell them to commit changes made by first stage
    of the commit protocol
    :param recipient_process_ip
    :param recipient_process_id
    :param group_id
    :param operation (commit or abort)
    """
    if random.random() <= constants.MESSAGE_PROBAILITY:
        url = "http://" + recipient_process_ip + ":" + constants.CLIENT_PORT+ "/API/processes/" + recipient_process_id + "/groups/" + group_id
        payload = {constants.OPERATION_KEY: operation} 
        response = requests.post(url, data=json.dumps(payload), headers=constants.JSON_HEADER)
        if response.status_code == requests.codes.ok:
            return True
        else:
            print(response)
            raise CommsError()
    else:
        raise CommsError()
        return False

def _is_member_online(process_ip,process_id, group_id):
    if random.random() <= constants.MESSAGE_PROBAILITY:
        url = "http://" + process_ip + ":" + constants.CLIENT_PORT+ "/API/processes/" + str(process_id)
        payload = {constants.GID_KEY: group_id}
        response = requests.get(url, data=json.dumps(payload), headers=constants.JSON_HEADER)
        if response.status_code ==  requests.codes.ok:
            return True
        return False
    else:
        raise CommsError()
        return False

def init():
    return


class CommsError(Exception):
    """Base class for any comms exception that deviate from happy path"""
    pass
