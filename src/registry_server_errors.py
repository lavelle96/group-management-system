'''
Created on Mar 11, 2019

@author: Saad
'''

class NO_GID_IN_REQ:
    code = 417
    msg = "'group_id' parameter does not exist in GET request"

class GID_EXISTS_USE_UPDATE:
    code = 418
    msg = " Coordinator for the specified GID already exists."\
            " Use UPDATE endpoint to update coordinaor IP"
