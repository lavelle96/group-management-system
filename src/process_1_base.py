"""

Code for coordinator class
Sets up thread to check all members of the group to see whether or not they are alive. 

Sets up endpoint to accept connections to join the group
Properties:

address (port/ip)

"""
from flask import Flask, request
from flask_restful import Api, Resource, abort

GROUP_MEMBERS = set([])
# GROUP_ID
# IS_COORDINATOR

class Join(Resource):
    def post(self):
        # Get ip+port from request
        # Ask ip+port if they actually want to be part of GID
        GROUP_MEMBERS.add((request.remote_addr))

class Leave(Resource):
    def post(self):
        # Get ip+port from request
        # Ask ip+port if they actually want to leave GID
        if not request.remote_addr in GROUP_MEMBERS:
            abort(420,'It didnt joint in the first place')
        GROUP_MEMBERS.remove(request.remote_addr)

class GetMembers(Resource):
    def get(self):
        return list(GROUP_MEMBERS)

APP = Flask(__name__)
API = Api(APP)
API.add_resource(Join, "/API/join")
API.add_resource(Leave, "/API/leave")
API.add_resource(GetMembers, "/API/getMembers")
