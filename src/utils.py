import requests
def request_with_failure():
    """
    A wrapper for requests that allows for a random chance of failure to 
    imitate network failure. Also includes a flag in case definite failure is 
    desired.
    """