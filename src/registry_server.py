"""
Registry server initialised before the start of the program

Needs an endpoint for the following:
- processes looking to see what groups are available (Done)
- Processes looking to create a new group (Not required)
- Processes looking to get the address of the coordinator of a group (Done)
- A Process updating the address of the coordinator of a group (Done)
"""
import sys

import constants
import registry_server_errors as errors
import utils
from flask import Flask, request
from flask_restful import Api, Resource, abort, reqparse

APP = Flask(__name__)
API = Api(APP)
GID_COORD_DICT = {}


class Group(Resource):
    def get(self, group_id=None):
        check_group_id_in_req(group_id)
        group_id = int(group_id)
        check_group_exists(group_id)
        (ip_addr, process_id) = GID_COORD_DICT[group_id]
        response = {constants.GID_KEY: group_id,
                    constants.COORD_IP_KEY: ip_addr,
                    constants.PID_KEY: process_id}
        return response


class Groups(Resource):
    def get(self):
        """
        Returns all groups meta-info
        """
        return GID_COORD_DICT

    def post(self):
        """
        Creates a group meta-info, and sets up coordinator
        """
        if not request.is_json:
            parser = reqparse.RequestParser()
            parser.add_argument(constants.GID_KEY, type=int, help='Group id')
            parser.add_argument(constants.PID_KEY, type=int, help='Process id')
            data = parser.parse_args()
        else:
            data = request.json
        group_id = data[constants.GID_KEY]
        process_id = data[constants.PID_KEY]
        check_group_id_in_req(group_id)
        check_process_id_in_req(process_id)
        check_group_does_not_exist(group_id)
        GID_COORD_DICT[group_id] = (request.remote_addr, process_id)
        response = {constants.GID_KEY: group_id,
                    constants.COORD_IP_KEY: GID_COORD_DICT[group_id][0],
                    constants.PID_KEY: GID_COORD_DICT[group_id][1]}
        return response

    def put(self):
        """
        Updates a group's meta-info
        """
        if not request.is_json:
            parser = reqparse.RequestParser()
            parser.add_argument(constants.GID_KEY, type=int, help='Group id')
            parser.add_argument(constants.PID_KEY, type=int, help='Process id')
            data = parser.parse_args()
        else:
            data = request.json
        group_id = data[constants.GID_KEY]
        process_id = data[constants.PID_KEY]
        check_group_id_in_req(group_id)
        check_process_id_in_req(process_id)
        check_group_exists(group_id)
        GID_COORD_DICT[group_id] = (request.remote_addr, process_id)
        response = {constants.GID_KEY: group_id,
                    constants.COORD_IP_KEY: GID_COORD_DICT[group_id][0],
                    constants.PID_KEY: GID_COORD_DICT[group_id][1]}
        return response


API.add_resource(Group, "/API/groups/<" + constants.GID_KEY + ">")
API.add_resource(Groups, "/API/groups")

if __name__ == "__main__":
    # server_port = sys.argv[1] # Feed in port on startup
    APP.run("0.0.0.0", constants.REGISTRY_PORT)
