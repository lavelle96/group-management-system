"""
A client represents an instance of the program running on one machine.
Client's methods are invoked by the launcher when the user enters a command, or by client_comms_rx when a message is
received.
Client holds a dictionary of all the processes created by the user on this machine/node/computer/client
"""

import sys
import threading

from process import Process

_processes = {}


def create_process(process_id):
    """
    Creates a new Process instance with given id, if it doesn't exist error
    :param process_id:
    :return: True, if process was created; False if process already exists
    """
    if process_id in _processes:
        return False
    else:
        _processes[process_id] = Process(process_id)
        return True


def destroy_process(process_id):
    """
    Removes an existing process with a given id from the list of tracked processes by this client, and destroys it
    :param process_id:
    :return: True, if process was destroyed; False, if the process doesn't exist
    """
    if process_id not in _processes:
        return False
    else:
        _processes[process_id]._terminate()
        del _processes[process_id]
        return True

def print_process_state(process_id):
    """
    Provides information about a local process, including all its groups
    :param process_id:
    """
    if process_id not in _processes:
        return False
    else:
        _processes[process_id]._debug()
        return True
def print_all_process_state():
    """
    Provides information about all local processes, including all their groups
    """
    if not bool(_processes):
        print("No processes currently")
        return False
    else:
        print("All processes:")
        for key in _processes.keys():
            _processes[key]._debug()
        return True

def print_all_process_state():
    """
    Provides information about all local processes, including all their groups
    """
    if not bool(_processes):
        print("No processes currently")
        return False
    else:
        print("All processes:")
        for key in _processes.keys():
            _processes[key]._debug()
        return True

def process_create_group(process_id, group_id):
    """
    Instructs a process with a given id to create a group
    :param process_id:
    :param group_id:
    :return: True, if operation was successful; False, if process doesn't exist
    """
    if process_id not in _processes:
        return False
    else:
        _processes[process_id]._create_group(group_id)
        return True


def process_join_group(process_id, group_id):
    """
    Instructs a process with a given id to join a specific group
    :param process_id:
    :param group_id:
    :return: True, if operation was successful; False, if process doesn't exist
    """
    if process_id not in _processes:
        return False
    else:
        _processes[process_id]._join_group(group_id)
        return True


def process_leave_group(process_id, group_id):
    """
    Instructs a process with a given id to leave a specific group
    :param process_id:
    :param group_id:
    :return: True, if operation was successful; False, if process doesn't exist
    """
    if process_id not in _processes:
        return False
    else:
        _processes[process_id]._leave_group(group_id)
        return True


def _process_prepare_update_group(process_id, group_id, group):
    """
    Internal method that tells the client to notify a process to prepare a group membership update. In other words,
    it is a way to reach a process and start the two phase commit process locally
    Called when an update message is received
    A group is represented by a dict with 3 entries:
    - constants.COORD_PID_KEY, which has the coordinator's process id
    - constants.COORD_IP_KEY, which has the coordinator's IP
    - constants.MEMBERS_KEY, which has a list of tuples, each tuple (process_id, ip) represents a member of the group
    :param process_id: the process that needs to prepare the update
    :param group_id: the group related to the update
    :param group: group membership information that the process will prepare to update
    :return: True, if operation was successful; False, if process doesn't exist
    """
    if process_id not in _processes:
        return False
    else:
        _processes[process_id]._prepare_update_group(group_id, group)
        return True


def _process_commit(process_id, group_id):
    """
    Internal method that tells the client to notify a process to prepare a commit a previous update. In other words,
    it is a way to reach a process and complete the two phase commit process locally
    Called when a commit message is received
    :param process_id: the process that needs to carry out the commit
    :param group_id: the group related to the update
    :return: True, if operation was successful; False, if process doesn't exist
    """
    if process_id not in _processes:
        return False
    else:
        _processes[process_id]._commit(group_id)
        return True


def _process_abort(process_id, group_id):
    """
    Internal method that tells the client to notify a process to abort a previous update. In other words,
    it is a way to reach a process and terminate the two phase commit process locally
    Called when an abort message is received
    :param process_id: the process that needs to carry out the abort
    :param group_id: the group related to the update
    :return: True, if operation was successful; False, if process doesn't exist
    """
    if process_id not in _processes:
        return False
    else:
        _processes[process_id]._abort(group_id)
        return True


def _coordinate_process_join_group(coordinator_pid, new_process_id, new_process_ip, group_id):
    """
    Internal method that tells the client to notify a process to act as a coordinator to a join group operation.
    In other words, it is a way to reach a coordinator and start the two phase commit process globally, across all clients
    Called when a join group message is received
    :param coordinator_pid: the process that needs to work as coordinator
    :param group_id: the group related to the join operation
    :param process_id: the process that wants to join the group
    :param process_ip: ip of the process that wants to join the group
    :return: state of group to be returned to new member
    TODO
    """
    if coordinator_pid not in _processes:
        return False
    else:
        return _processes[coordinator_pid]._coord_manage_join(new_process_id, new_process_ip, group_id)
        


def _coordinate_process_leave_group(coordinator_pid, process_id, process_ip, group_id):
    """
    Internal method that tells the client to notify a process to act as a coordinator to a leave group operation.
    In other words, it is a way to reach a coordinator and start the two phase commit process globally, across all clients
    Called when a leave group message is received
    :param coordinator_pid: the process that needs to work as coordinator
    :param group_id: the group related to the leave operation
    :param process_id: the process that wants to leave the group
    :param process_ip: the ip of the process that wants to leave the group
    :return:
    
    """
    if coordinator_pid not in _processes:
        return False
    else:
        _processes[coordinator_pid]._coord_manage_leave(process_id, process_ip, group_id)
        return True


def _check_process(process_id):
    """
    Internal method that tells the client to contact a process and check if it is still running
    Called when a heartbeat message is received
    :param process_id: the process that needs to be checked
    :return: True, if operation was successful; False, if process doesn't exist
    """
    if process_id in _processes:
        return _processes[process_id]._check()
    else:
        return False


def _return_processes_ids():
    return [*_processes]

def _return_process(id):
    if id in _processes:
        return _processes[id]
    else:
        return False

def return_groups_id(process_id):
   return _processes[process_id]._return_groups_id()
    
