"""
Registry server initialised before the start of the program

Needs an endpoint for the following:
- processes looking to see what groups are available (Done)
- Processes looking to create a new group (Not required)
- Processes looking to get the address of the coordinator of a group (Done)
- A Process updating the address of the coordinator of a group (Done)
"""
import sys

import comms_errors as errors
import constants
import utils
from flask import Flask, request
from flask_restful import Api, Resource, abort, reqparse

APP = Flask(__name__)
API = Api(APP)
GID_COORD_DICT = {}


class Group(Resource):
    """
    Message handler for operations particular to a single group: getting group meta-data like PID and IP
    """

    def get(self, group_id=None):
        """
        Handler that returns metadata information about a group
        :return: Information about a group if the group exists, or an error message if not
        """
        utils.check_group_id_in_req(group_id)
        #group_id = int(group_id)
        _check_group_exists(group_id)
        (process_id, ip_addr) = GID_COORD_DICT[group_id]
        response = {constants.COORD_PID_KEY: process_id,
                    constants.COORD_IP_KEY: ip_addr}
        return response


class Groups(Resource):
    """
    Message handler for operations that affect groups, e.g., create new group; or alter group metadata
    """

    def get(self):
        """
        Returns all groups, i.e., group_id, process_id, coordinator_ip, the registry server has information on.
        """
        # TODO: Cannot just return the dict, because it will not include the labels/keys in the response
        return GID_COORD_DICT

    def post(self):
        """
        Creates an entry on the registry server as a result of a request from a client/process
        It first verifies the group the client is trying to create doesn't exist already
        Returns the group meta-information: process_id, coordinator_ip
        """
        if not request.is_json:
            parser = reqparse.RequestParser()
            parser.add_argument(constants.PID_KEY, help='Process id')
            parser.add_argument(constants.GID_KEY, help='Group id')
            data = parser.parse_args()
        else:
            data = request.json
        process_id = data[constants.PID_KEY]
        group_id = data[constants.GID_KEY]
        utils.check_process_id_in_req(process_id)
        utils.check_group_id_in_req(group_id)
        _check_group_does_not_exist(group_id)
        GID_COORD_DICT[group_id] = (process_id, request.remote_addr)
        response = {constants.COORD_PID_KEY: GID_COORD_DICT[group_id][0],
                    constants.COORD_IP_KEY: GID_COORD_DICT[group_id][1]}
        return response

    def put(self):
        """
        Similar to the previous method. Used only to change the group's meta-information, i.e., to change coordinators'
        PID and IP
        It first verifies the group the client is trying to update exists already
        Returns the group meta-information: process_id, coordinator_ip
        """
        if not request.is_json:
            parser = reqparse.RequestParser()
            parser.add_argument(constants.PID_KEY, help='Process id')
            parser.add_argument(constants.GID_KEY, help='Group id')
            data = parser.parse_args()
        else:
            data = request.json
        group_id = data[constants.GID_KEY]
        process_id = data[constants.PID_KEY]
        utils.check_process_id_in_req(process_id)
        utils.check_group_id_in_req(group_id)
        _check_group_exists(group_id)
        GID_COORD_DICT[group_id] = (process_id, request.remote_addr)
        response = {constants.COORD_PID_KEY: GID_COORD_DICT[group_id][0],
                    constants.COORD_IP_KEY: GID_COORD_DICT[group_id][1]}
        return response


def _check_group_exists(group_id):
    if group_id not in GID_COORD_DICT:
        abort(errors.GROUP_DOES_NOT_EXIST.status_code,
              errmsg=errors.GROUP_DOES_NOT_EXIST.msg,
              error_code=errors.GROUP_DOES_NOT_EXIST.error_code)
    else:
        return True


def _check_group_does_not_exist(group_id):
    if group_id in GID_COORD_DICT:
        abort(errors.GROUP_ALREADY_EXISTS.status_code,
              errmsg=errors.GROUP_ALREADY_EXISTS.msg,
              error_code=errors.GROUP_ALREADY_EXISTS.error_code)
    else:
        return True


API.add_resource(Group, "/API/groups/<" + constants.GID_KEY + ">")
API.add_resource(Groups, "/API/groups")

if __name__ == "__main__":
    # server_port = sys.argv[1] # Feed in port on startup
    APP.run("0.0.0.0", constants.REGISTRY_PORT)
