"""
Registry server initialised before the start of the program

Needs an endpoint for the following:
- processes looking to see what groups are available
- Processes looking to create a new group
- Processes looking to get the address of the coordinator of a group
- A Process updating the address of the coordinator of a group
"""

from flask import Flask, request, jsonify
from flask_restful import Api, Resource, abort
import json
import sys

app = Flask(__name__)
api = Api(app)

class group_api(Resource):
    def get(self):
        """
        Params: (group id/group name)
        Returns: the ip of the coordinator of the group given.
        """
        if(not request.is_json):
            abort(400)
        data = request.json
        group_id = data["group_id"]
        # Get address of coordinator associated with given group_id and return it
        # e.g.
        address = "3.4.5.6:4000"
        data_to_return = {
            "group_id": group_id,
            "coordinator_address": address
        }
        return jsonify(data_to_return)
        
    
    def post(self):
        """
        Used for creating new group
        Load: ip of new coordinator, name of new group
        Returns: group id of new group created
        """
        if(not request.is_json):
            abort(400)
        data = request.json
        group_name = data["group_name"]
        new_coordinator = data["coordinator_ip"]
        # Add new group to data structure
        # Assign new group id and return it
        return None
    def put(self):
        """
        Used to set coordinator of group to new address
        Load: id/ip of new coordinator, group id of group. Sent when old coordinator crashes and new coordinator starts up
        Returns: N/A
        """
        if(not request.is_json):
            abort(400)
        data = request.json
        group_id = data["group_id"]
        old_coordinator = data["old_coordinator"]
        new_coordinator = data["new_coordinator"]
        # Change coordinator of group given
        return None

class groups_api(Resource):
    def get(self):
        """
        Params: none
        Returns: The groups that are active atm (used for process on startup to decide whether to join or create a new group)
        """
        # Get info on current group states and return it in json
        # Using the "jsonify" function from flask
        return None

api.add_resource(group_api, "/api/group")
api.add_resource(groups_api, "/api/groups")

if __name__ == "__main__":
    server_port = sys.argv[1] # Feed in port on startup
    app.run("0.0.0.0", server_port)