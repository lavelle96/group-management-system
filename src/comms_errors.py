'''
Created on Mar 16, 2019

@author: Gustavo
'''
import constants


class NO_GID_IN_REQ:
    status_code = 417
    msg = "group_id was not included in the request"
    error_code = constants.NO_GID_IN_REQ_ERROR_CODE


class GROUP_ALREADY_EXISTS:
    status_code = 417
    msg = "Group already exists. Use correct endpoint to get the group or to update it"
    error_code = constants.GROUP_ALREADY_EXISTS_ERROR_CODE


class GROUP_DOES_NOT_EXIST:
    status_code = 417
    msg = "Group does not exist. Use correct endpoint to create group"
    error_code = constants.GROUP_DOES_NOT_EXIST_ERROR_CODE


class NO_PID_IN_REQ:
    status_code = 417
    msg = "process_id was not included in the request"
    error_code = constants.NO_PID_IN_REQ_ERROR_CODE


class PROCESS_NOT_AVAILABLE:
    status_code = 417
    msg = "Process does not exist or it is not available"
    error_code = constants.PROCESS_NOT_AVAILABLE_ERROR_CODE

class WRONG_OPERATION_PARAMETER:
    status_code = 417
    msg = "Operation parameter was neither commit nor abort"
    error_code = constants.WRONG_OPERATION_PARAMETER