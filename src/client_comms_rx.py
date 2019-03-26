"""
Represents a communications receiver. A client only has one communication receiver listening in a single port
Every message received requires a process_id, so that the client can invoke the appropriate method on the right process
"""

import threading
import json

import client
import comms_errors as errors
import constants
import process
import utils

from flask import Flask, request
from flask_restful import Api, Resource, abort, reqparse

"""
TODO
Need an endpoint to receive heart beat signal from coordinator and to return an ack signal also to let the coord know
this instance is alive and kicking.

Monitor the time you haven't received a heartbeat from coordinator, if longer than x, assume the coordinator is down and
assign coordinator responsibilities to the machine with the next highest ip.
"""


class ProcessRes(Resource):
    """
    Message handler for operations particular to a single process: heartbeat
    """

    def get(self, process_id=None):
        """
        Handler that forwards the check action to the client when a heartbeat message is received
        :param process_id: the process that needs to be checked
        :return: If successful, it returns empty dict; if it fails, it returns an error message
        """
        #process_id = int(process_id)
        if client._check_process(process_id):
            return {}
        else:
            abort(errors.PROCESS_NOT_AVAILABLE.status_code, errmsg=errors.PROCESS_NOT_AVAILABLE.msg,
                  error_code=errors.PROCESS_NOT_AVAILABLE.error_code)


class GroupMembershipRes(Resource):
    """
    Message handler for operations particular to a specific process and a specific group: group membership update, commit,
    and abort
    """

    def put(self, process_id=None, group_id=None):
        """
        Handler that listens for group membership updates, which inform of group state changes such as process joining,
        or leaving
        A group is represented by a dict with 3 entries:
        - constants.COORD_PID_KEY, which has the coordinator's process id
        - constants.COORD_IP_KEY, which has the coordinator's IP
        - constants.MEMBERS_KEY, which has a list of tuples, each tuple (process_id, ip) represents a member of the group
        :param process_id: the process that needs to prepare the update
        :param group_id: the group related to the update
        :return: If successful, it returns empty dict; if it fails, it returns an error message
        """
        
        #process_id = int(process_id)
        #group_id = int(group_id)
        if not request.is_json:
            parser = reqparse.RequestParser()
            parser.add_argument(constants.COORD_PID_KEY, type=str, help='Coordinator PID')
            parser.add_argument(constants.COORD_IP_KEY, type=str, help='Coordinator IP')
            parser.add_argument(constants.MEMBERS_KEY, type=list,
                                help='List of tuples (process_id, ip), including the coordinator')
            data = parser.parse_args()
        else:
            data = request.json
        if client._process_prepare_update_group(process_id, group_id, data):
            return {}
        else:
            abort(errors.PROCESS_NOT_AVAILABLE.status_code, errmsg=errors.PROCESS_NOT_AVAILABLE.msg,
                  error_code=errors.PROCESS_NOT_AVAILABLE.error_code)

    def post(self, process_id=None, group_id=None):
        """
        Handler that listens for commit or abort messages related to group membership updates received before
        A parameter within the message called operation indicates if the operation is commit or abort
        :param process_id: the process that needs to carry out the commit or abort
        :param group_id: the group related to the operation
        :return: If successful, it returns empty dict; if it fails, it returns an error message, either because the
        operation was not recognized, or the commmit or abort operation failed
        """
        #process_id = int(process_id)
        #group_id = int(group_id)
        if not request.is_json:
            parser = reqparse.RequestParser()
            parser.add_argument(constants.OPERATION_KEY, type=str, help='Indicates whether it is a commit or abort')
            data = parser.parse_args()
        else:
            data = request.json
        operation = data[constants.OPERATION_KEY]
        if operation == constants.COMMIT:
            if client._process_commit(process_id, group_id):
                return {}
            else:
                abort(errors.PROCESS_NOT_AVAILABLE.status_code, errmsg=errors.PROCESS_NOT_AVAILABLE.msg,
                      error_code=errors.PROCESS_NOT_AVAILABLE.error_code)
        elif operation == constants.ABORT:
            if client._process_abort(process_id, group_id):
                return {}
            else:
                abort(errors.PROCESS_NOT_AVAILABLE.status_code, errmsg=errors.PROCESS_NOT_AVAILABLE.msg,
                      error_code=errors.PROCESS_NOT_AVAILABLE.error_code)
        else:
            abort(errors.WRONG_OPERATION_PARAMETER.status_code, errmsg=errors.WRONG_OPERATION_PARAMETER.msg,
                  error_code=errors.WRONG_OPERATION_PARAMETER.error_code)


class CoordinatorRes(Resource):
    """
    Message handler for coordinator operations particular to a specific process and a specific group: join group, and
    leave group
    """

    def post(self, process_id=None, group_id=None):
        """
        Handler that listens for join group messages.
        
        :param process_id: process id of coordinator (self in this case)
        :param group_id: group id of the group the process is trying to join
        body of request:
        {
            contants.PID_KEY: process id of the process making the request to join
        }
        :return:
        """
        new_process_ip = request.remote_addr
        if not request.is_json:
            parser = reqparse.RequestParser()
            parser.add_argument(constants.PID_KEY, type=str, help='Process id of process attempting to join the group')
            data = parser.parse_args()
        else:
            data = request.json
        result = client._coordinate_process_join_group(process_id, data[constants.PID_KEY], new_process_ip, group_id)
        if result:
            return result
        else:
            """ TODO create new error codes for here"""
            abort(errors.PROCESS_NOT_AVAILABLE.status_code, errmsg=errors.PROCESS_NOT_AVAILABLE.msg,
                  error_code=errors.PROCESS_NOT_AVAILABLE.error_code)

    def delete(self, process_id=None, group_id=None, ):
        """
        Handler that listens for leave group messages.
        
        :param process_id: process id of coordinator (self in this case)
        :param group_id: group id of the group the process is trying to leave
        body of request:
        {
            contants.PID_KEY: process id of the process making the request to leave
        }
        :return:
        """
        
        if not request.is_json:
            parser = reqparse.RequestParser()
            parser.add_argument(constants.PID_KEY, type=str, help='Process id of process attempting to join the group')
            data = parser.parse_args()
        else:
            data = request.json
        result = client._coordinate_process_leave_group(process_id, data[constants.PID_KEY], request.remote_addr, group_id)
        if result:
            return {}
        else:
            """ TODO create new error codes for here"""
            abort(errors.PROCESS_NOT_AVAILABLE.status_code, errmsg=errors.PROCESS_NOT_AVAILABLE.msg,
                  error_code=errors.PROCESS_NOT_AVAILABLE.error_code)


def init():
    """
    Instantiates Flask and registers message handlers for 3 different endpoints. Then, it starts Flask on an independent
    thread
    """

    print("client_comms_rx init")
    print(threading.current_thread())
    app = Flask(__name__)
    app.debug = False
    app.use_reloader = False
    api = Api(app)
    api.add_resource(ProcessRes, "/API/processes/<" + constants.PID_KEY + ">")
    api.add_resource(GroupMembershipRes,
                     "/API/processes/<" + constants.PID_KEY + ">" + "/groups/<" + constants.GID_KEY + ">")
    api.add_resource(CoordinatorRes,
                     "/API/processes/<" + constants.PID_KEY + ">/coordinate/groups/<" + constants.GID_KEY + ">")
    # server_port = sys.argv[1]  # Feed in port on startup
    t = threading.Thread(target=app.run, args=("0.0.0.0", constants.CLIENT_PORT))
    t.daemon = True
    t.start()
    return t
