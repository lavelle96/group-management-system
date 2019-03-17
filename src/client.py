import sys
import threading

from process import Process

processes = {}


def create_process(process_id):
    if process_id in processes:
        return False
    else:
        processes[process_id] = Process(process_id)
        return True


def destroy_process(process_id):
    if process_id not in processes:
        return False
    else:
        processes[process_id].terminate()
        del processes[process_id]
        return True


def process_join_group(process_id, group_id):
    if process_id not in processes:
        return False
    else:
        processes[process_id].join_group(group_id)
        return True


def process_leave_group(process_id, group_id):
    if process_id not in processes:
        return False
    else:
        processes[process_id].leave_group(group_id)
        return True


def process_prepare_update_group(process_id, group_id, group):
    if process_id not in processes:
        return False
    else:
        processes[process_id].prepare_update_group(group_id, group)
        return True


def process_commit(process_id, group_id):
    if process_id not in processes:
        return False
    else:
        processes[process_id].commit(group_id)
        return True


def process_abort(process_id, group_id):
    if process_id not in processes:
        return False
    else:
        processes[process_id].abort(group_id)
        return True


def coordinate_process_join_group(process_id, group_id):
    if process_id not in processes:
        return False
    else:
        processes[process_id].update_group(group_id)
        return True


def coordinate_process_leave_group(process_id, group_id):
    if process_id not in processes:
        return False
    else:
        processes[process_id].update_group(group_id)
        return True


def check_process(process_id):
    if process_id in processes:
        return processes[process_id].check()
    else:
        return False
