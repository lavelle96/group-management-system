GID_KEY = 'group_id'
COORD_IP_KEY = 'coordinator_ip'
IP_KEY = 'ip'
PID_KEY = 'process_id'

MEMBERS_KEY = 'members_ips'
ACTION_KEY = 'action'
COMMIT = 'commit'
ABORT = 'abort'

# Registry IP needs to be set with correct registry IP; it shouldn't be localhost
REGISTRY_IP = "0.0.0.0"
REGISTRY_PORT = "5000"
CLIENT_PORT = "5001"

NO_GID_IN_REQ_ERROR_CODE = 1
GROUP_ALREADY_EXISTS_ERROR_CODE = 2
GROUP_DOES_NOT_EXIST_ERROR_CODE = 3
NO_PID_IN_REQ_ERROR_CODE = 4
PROCESS_NOT_AVAILABLE_ERROR_CODE = 5