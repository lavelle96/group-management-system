'''
Created on Mar 12, 2019

@author: Saad
'''
import sys

from flask_restful import Resource
from src.process_1_base import API,APP

class HelloWorld(Resource):
    def get(self):
        return "Hello World!"


if __name__ == "__main__":
    server_port = sys.argv[1] # Feed in port on startup
    '''
    Add code here
    '''
    API.add_resource(HelloWorld,'/hw')
    APP.run("0.0.0.0", server_port)
