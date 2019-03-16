'''
Created on Mar 11, 2019

@author: Saad
'''

class NO_GID_IN_REQ:
    code = 417
    msg = "'group_id' was not included in the request"

class GROUP_ALREADY_EXISTS:
    code = 418
    msg = "Group already exists. Use correct endpoint to get the group or to update it"

class GROUP_DOES_NOT_EXIST:
    code = 418
    msg = "Group does not exist. Use correct endpoint to create group"
