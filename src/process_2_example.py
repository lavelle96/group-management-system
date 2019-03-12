'''
Created on Mar 12, 2019

@author: Saad
'''
from flask_restful import Resource
from src.process_2_base import Process


class HelloWorld1(Resource):
    def get(self):
        return "Hello World1!"

class HelloWorld2(Resource):
    def get(self):
        return "Hello World2!"

p = Process(12345)
p.add_resource(HelloWorld1, '/hw')
p.run()

p = Process(22345)
p.add_resource(HelloWorld2, '/hw')
p.run()