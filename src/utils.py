import requests
def request_with_failure():
    """
    A wrapper for requests that allows for a random chance of failure to 
    imitate network failure. Also includes a flag in case definite failure is 
    desired.
    """

def check_group_id_in_req(group_id):
    if group_id is None:
        abort(errors.NO_GID_IN_REQ.status_code,
              errmsg=errors.NO_GID_IN_REQ.msg,
              error_code=errors.NO_GID_IN_REQ.error_code)


def check_group_exists(group_id):
    if group_id not in GID_COORD_DICT:
        abort(errors.GROUP_DOES_NOT_EXIST.status_code,
              errmsg=errors.GROUP_DOES_NOT_EXIST.msg,
              error_code=errors.GROUP_DOES_NOT_EXIST.error_code)
    else:
        return True


def check_group_does_not_exist(group_id):
    if group_id in GID_COORD_DICT:
        abort(errors.GROUP_ALREADY_EXISTS.status_code,
              errmsg=errors.GROUP_ALREADY_EXISTS.msg,
              error_code=errors.GROUP_ALREADY_EXISTS.error_code)
    else:
        return True


def check_process_id_in_req(process_id):
    if process_id is None:
        abort(errors.NO_PID_IN_REQ.status_code,
              errmsg=errors.NO_PID_IN_REQ.msg,
              error_code=errors.NO_PID_IN_REQ.error_code)
    else:
        return True