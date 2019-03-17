'''
Created on Mar 16, 2019

@author: Gustavo
'''


class NO_GID_IN_REQ:
    code = 417
    msg = "'group_id' was not included in the request"
    error_code = constants.NO_GID_IN_REQ_ERROR_CODE


class NO_PID_IN_REQ:
    code = 417
    msg = "'process_id' was not included in the request"
    error_code = constants.NO_PID_IN_REQ_ERROR_CODE
