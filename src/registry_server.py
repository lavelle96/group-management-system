"""
Registry server initialised before the start of the program

Needs an endpoint for the following:
- processes looking to see what groups are available (Done)
- Processes looking to create a new group (Not required)
- Processes looking to get the address of the coordinator of a group (Done)
- A Process updating the address of the coordinator of a group (Done)
"""
import sys
import registry_server_errors as errors
from flask import Flask, request
from flask_restful import Api, Resource, abort,reqparse

APP = Flask(__name__)
API = Api(APP)
GID_COORD_DICT = {}
GID_KEY = 'group_id'

class Group(Resource):
    def get(self, group_id=None):
        if group_id is None:
            abort(errors.NO_GID_IN_REQ.code,
                  errmsg=errors.NO_GID_IN_REQ.msg)
        group_id = int(group_id)
        if group_id not in GID_COORD_DICT:
            abort(errors.GROUP_DOES_NOT_EXIST.code,
                  errmsg=errors.GROUP_DOES_NOT_EXIST.msg)
        ip_addr = GID_COORD_DICT[group_id]
        response = {'group_id': group_id,
                    'coordinator_ip': ip_addr}
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
            parser.add_argument(GID_KEY, type=int, help='Group id')
            data = parser.parse_args()
        else:
            data = request.json
        group_id = data[GID_KEY]
        if group_id is None:
            abort(errors.NO_GID_IN_REQ.code,
                  errmsg=errors.NO_GID_IN_REQ.msg)
        if group_id not in GID_COORD_DICT:
            GID_COORD_DICT[group_id] = request.remote_addr
            response = {'group_id': group_id,
                        'coordinator_ip': GID_COORD_DICT[group_id]}
            return response
        else:
            abort(errors.GROUP_ALREADY_EXISTS.code,
                  errmsg=errors.GROUP_ALREADY_EXISTS.msg)

    def put(self):
        """
        Updates a group's meta-info
        """
        if not request.is_json:
            parser = reqparse.RequestParser()
            parser.add_argument(GID_KEY, type=int, help='Group name')
            data = parser.parse_args()
        else:
            data = request.json
        group_id = data[GID_KEY]
        if group_id is None:
            abort(errors.NO_GID_IN_REQ.code,
                  errmsg=errors.NO_GID_IN_REQ.msg)
        if group_id not in GID_COORD_DICT:
            abort(errors.GROUP_DOES_NOT_EXIST.code,
                  errmsg=errors.GROUP_DOES_NOT_EXIST.msg)
        else:
            GID_COORD_DICT[group_id] = request.remote_addr
            response = {'group_id': group_id,
                        'coordinator_ip': GID_COORD_DICT[group_id]}
            return response


API.add_resource(Group, "/API/groups/<" + GID_KEY + ">")
API.add_resource(Groups, "/API/groups")

if __name__ == "__main__":
    server_port = sys.argv[1] # Feed in port on startup
    APP.run("0.0.0.0", server_port)