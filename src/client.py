"""

Code for client class

Need an endpoint to receive heart beat signal from coordinator and to return an ack signal also to let the coord know 
this instance is alive and kicking.

Monitor the time you haven't received a heartbeat from coordinator, if longer than x, assume the coordinator is down and
assign coordinator responsibilities to the machine with the next highest ip.
"""




