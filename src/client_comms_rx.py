import threading

import client
import comms_errors as errors
import constants
import process
import utils
from flask import Flask, request
from flask_restful import Api, Resource, abort, reqparse

"""

Code for client class

Need an endpoint to receive heart beat signal from coordinator and to return an ack signal also to let the coord know 
this instance is alive and kicking.

Monitor the time you haven't received a heartbeat from coordinator, if longer than x, assume the coordinator is down and
assign coordinator responsibilities to the machine with the next highest ip.
"""


class ProcessRes(Resource):
    def get(self, process_id=None):
        """
        Heartbeat handler
        """
        process_id = int(process_id)
        if client.check_process(process_id):
            return {}
        else:
            abort(errors.PROCESS_NOT_AVAILABLE.status_code, errmsg=errors.PROCESS_NOT_AVAILABLE.msg,
                  error_code=errors.PROCESS_NOT_AVAILABLE.error_code)


class CoordinatorRes(Resource):
    def post(self, process_id=None, group_id=None):
        client.coordinate_process_join_group(process_id, group_id)

    def delete(self, process_id=None, group_id=None, ):
        client.coordinate_process_leave_group(process_id, group_id)


class GroupMembershipRes(Resource):

    def put(self, process_id=None, group_id=None):
        """
        Handler that listens for events informing of group state changes
        """
        process_id = int(process_id)
        group_id = int(group_id)
        if not request.is_json:
            parser = reqparse.RequestParser()
            parser.add_argument(constants.COORD_IP_KEY, type=String, help='Coordinator IP')
            parser.add_argument(constants.MEMBERS_IPS_KEY, type=list,
                                help='List of IPs of the members, including the coordinator')
            data = parser.parse_args()
        else:
            data = request.json
        client.process_prepare_update_group(process_id, group_id, data)
        return {'group_id': group_id}

    def post(self, process_id=None, group_id=None):
        """
        Handler to commit or abort the group changes broadcasted before
        """
        process_id = int(process_id)
        group_id = int(group_id)
        if not request.is_json:
            parser = reqparse.RequestParser()
            parser.add_argument(constants.ACTION_KEY, type=String, help='Commit or abort parameter')
            data = parser.parse_args()
        else:
            data = request.json
        action = data[ACTION_KEY]
        if action == constants.COMMIT:
            client.process.commit(process_id, group_id)
        elif action == constants.ABORT:
            client.process_abort(process_id, group_id)
        else:
            # wrong action
            abort(errors.NO_GID_IN_REQ.status_code, errmsg=errors.NO_GID_IN_REQ.msg,
                  error_code=errors.NO_GID_IN_REQ.error_code)


def init():
    print("client_comms init")
    print(threading.current_thread())
    app = Flask(__name__)
    app.debug = False
    app.use_reloader = False
    api = Api(app)
    api.add_resource(ProcessRes, "/API/processes/<" + constants.PID_KEY + ">")
    api.add_resource(CoordinatorRes,
                     "/API/processes/<" + constants.PID_KEY + ">/coordinate/groups/<" + constants.GID_KEY + ">")
    api.add_resource(GroupMembershipRes,
                     "/API/processes/<" + constants.PID_KEY + ">" + "/groups/<" + constants.GID_KEY + ">")
    # server_port = sys.argv[1]  # Feed in port on startup
    threading.Thread(target=app.run, args=("0.0.0.0", constants.CLIENT_PORT)).start()