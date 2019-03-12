"""
Base class for a process.
A process has a Flask app in which you can add multiple endpoints.
Additionally, it has some resources common to our Distributed Systems assignment
A process can be a Coordinator or simply a slave
"""
import threading
from flask import Flask, request
from flask_restful import Api, Resource, abort

class Process:
    def __init__(self,port):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.group_members = set([])
        self.port = port
        self.is_coord = False

        '''
        Returns the health status of the process
        class IsHealthy:
            pass
        '''

        class Join(Resource):
            '''
            When process is a coordinator, this endpoint will be used
            to join the group
            '''
            def post(self):
                self.proc.group_members.add(request.remote_addr)

        class Leave(Resource):
            '''
            When process is a coordinator, this endpoint will be used
            to leave the group
            '''
            def post(self):
                if not request.remote_addr in self.proc.group_members:
                    abort(420,"Wasn't a part of the group in the first place")
                self.proc.group_members.remove(request.remote_addr)

        class GetMembers(Resource):
            '''
            When process is a coordinator, this endpoint will be used
            to get all members of the group
            '''
            def get(self):
                return list(self.proc.group_members)

        Join.proc = self
        Leave.proc = self
        GetMembers.proc = self
        self.add_resource(Join,'/API/join')
        self.add_resource(Leave,'/API/leave')
        self.add_resource(GetMembers,'/API/getMembers')

    def add_resource(self,c,p):
        self.api.add_resource(c,p)

    def run(self):
        self.thread = threading.Thread(target=self.app.run,
                                       args=("0.0.0.0", self.port,))
        self.thread.start()
