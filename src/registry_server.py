"""
Registry server initialised before the start of the program

Needs an endpoint for the following:
- processes looking to see what groups are available (Done)
- Processes looking to create a new group (Not required)
- Processes looking to get the address of the coordinator of a group (Done)
- A Process updating the address of the coordinator of a group (Done)
"""
import sys
import src.registry_server_errors as errors
from flask import Flask, request
from flask_restful import Api, Resource, abort,reqparse

APP = Flask(__name__)
API = Api(APP)
GID_COORD_DICT = {}
GID_KEY = 'group_id'

class GetCoordByID(Resource):
    def get(self):
        """
        """
        if not request.is_json:
            parser = reqparse.RequestParser()
            parser.add_argument(GID_KEY, type=int,
                                help='Group ID for for the coordinator')
            data = parser.parse_args()
        else:
            data = request.json

        group_id = data[GID_KEY]
        if group_id is None:
            abort(errors.NO_GID_IN_REQ.code,
                  errmsg=errors.NO_GID_IN_REQ.msg)

        ip_addr = None
        if group_id in GID_COORD_DICT.keys():
            ip_addr = GID_COORD_DICT[group_id]
        
        data_to_return = {group_id:ip_addr}
        return data_to_return

class GetAllCoords(Resource):
    def get(self):
        """
        """
        return GID_COORD_DICT

class SetSelfAsCoord(Resource):
    def post(self):
        """
        """
        if not request.is_json:
            parser = reqparse.RequestParser()
            parser.add_argument(GID_KEY, type=int,
                                help='Group ID for for the coordinator')
            data = parser.parse_args()
        else:
            data = request.json

        group_id = data[GID_KEY]
        if group_id is None:
            abort(errors.NO_GID_IN_REQ.code,
                  errmsg=errors.NO_GID_IN_REQ)

        GID_COORD_DICT[group_id] = request.remote_addr
        ret = {'coordinator_ip':GID_COORD_DICT[group_id]}
        return ret

API.add_resource(GetCoordByID, "/API/groups/getCoordByID")
API.add_resource(GetAllCoords, "/API/groups/getAllCoords")
API.add_resource(SetSelfAsCoord, "/API/groups/setSelfAsCoord")

if __name__ == "__main__":
    server_port = sys.argv[1] # Feed in port on startup
    APP.run("0.0.0.0", server_port)