import client_comms_tx as tx
import constants
from client_comms_tx import CommsError
from copy import deepcopy

class Process:
    """
    Represents one process created/running on a client/machine/node/computer
    """

    def __init__(self, process_id):
        """
        _groups represent committed groups this process has visibility on
        _temp_groups represent group updates or changes that have been received but not yet committed
        :param process_id:
        """
        self.process_id = process_id
        self._groups = {}
        self._temp_groups = {}

    def _prepare_update_group(self, group_id, group):
        """
        Initiate the two phase commit protocol for this process
        :param group_id: group whose information is going to be updated
        :param group: new group info
        :return: True, if changes were saved; False, if the group doesn't exist
        """
        if group_id in self._groups and group_id not in self._temp_groups:
            group[constants.GID_KEY] = group_id
            self._temp_groups[group_id] = group
            
            return True
        else:
            print("Prepare update group failed debug: ")
            self._debug()
            return False

    def _commit(self, group_id):
        """
        Moves changes from _temp_groups to _groups, effectively committing the changes
        :param group_id: the group on which changes should be committed
        :return: True, if changes were committed; False, if the group doesn't exist
        """
        if group_id in self._temp_groups:
            group = deepcopy(self._temp_groups[group_id])
            del self._temp_groups[group_id]
            self._groups[group_id] = group
            return True
        else:
            print("Commit failed")
            self._debug()
            return False

    def _abort(self, group_id):
        """
        Discard changes from _temp_groups, effectively aborting the changes
        :param group_id: the group on which changes should be aborted
        :return: True, if changes were aborted; False, if the group doesn't exist
        """
        if group_id in self._temp_groups:
            del self._temp_groups[group_id]
            return True
        else:
            self._debug()
            return False

    def _check(self):
        """
        Performs checks on the process, and indicates the process' condition
        :return: Always, true at the moment
        """
        return True

    def _create_group(self, group_id):
        """
        Attempts to create a new group, by contacting the registry server, and initializing internal data structures
        :param group_id:
        :return:
        """
        try:
            # Check with registry server if the group already is registered
            (result, r_process_id, r_coordinator_ip) = tx._request_group_coordinator(group_id)
            if result:
                # The registry server is already tracking a group with such id; thus, the operations fails
                return False
            else:
                # Ask the registry server to update the list of groups with the new group
                (result, r_process_id, r_ip) = tx._request_create_group(self.process_id, group_id)
                if result:
                    # Since the group has just been created, initialize a data structure that represents the new group,
                    # which is ok, because the first proceess is the coordinator by default
                    self._groups[group_id] = self._create_own_group(group_id, r_process_id, r_ip)
                else:
                    print(
                        "Inconsistent or timing situation. Registry indicated that group didn't exist, but didn't allow creation of group")
                    return True
        except CommsError as ce:
            # Querying the registry server didn't work, so the operation cannot continue; thus, it failed
            return False

    def _create_own_group(self, r_group_id, r_process_id, r_ip):
        """
        Internal methods that creates the dict that represents a newly created group
        :param r_group_id:
        :param r_process_id: the process id of the process that is the one creating the group, and thus, also, the coordinator
        :param r_ip: the ip of the client where the above-mentioned process exists
        :return:
        """
        group = {constants.GID_KEY: r_group_id,
                 constants.COORD_PID_KEY: r_process_id,
                 constants.COORD_IP_KEY: r_ip,
                 constants.MEMBERS_KEY: [
                     {
                         constants.PID_KEY: r_process_id,
                         constants.IP_KEY: r_ip,
                     }
                 ]
                 }
        return group

    def _join_group(self, group_id):
        # get coordinator or create group
        try:
            (result, r_process_id, r_coordinator_ip) = tx._request_group_coordinator(group_id)
            if result:
                (result, new_group) = tx._request_join_group(r_process_id, r_coordinator_ip,
                                                self.process_id,
                                                group_id)
                if result:
                    self._groups[group_id] = new_group
                if not result:
                    print("Inconsistent or timing situation. Coordinator indicated that join operation failed")
                    return
        except CommsError as ce:
            return

    def _leave_group(self, group_id):
        """
        Function to manage controlled exits from group
        :param group_id
        """
        try:
            coord_pid = self._groups[group_id][constants.COORD_PID_KEY]
            coord_ip = self._groups[group_id][constants.COORD_IP_KEY]
            
            result = tx._request_leave_group(coord_pid, coord_ip,
                                            self.process_id,
                                            group_id)
            if result:
                del self._groups[group_id] 
            if not result:
                print("Inconsistent or timing situation. Coordinator indicated that leave operation failed")
                return
        except CommsError as ce:
            return

    def _coord_manage_join(self, new_process_id, new_process_ip, group_id):
        """
        Called by coordinator after someone requests to join the group,
        Manages join by contacting everyone in the group telling them to enter
        first stage of 2-phase commit protol, if all respond with ack's, a second message
        is sent out to all members of the group telling them to commit changes (second
        stage of protocol)
        :param new_process_id process id of process that requested to join the group
        :param new_process_ip process ip of process that requested to join the group
        :param group_id group id of the group the process is trying to join
        :returns:
        """
        new_member = {
            constants.PID_KEY: new_process_id,
            constants.IP_KEY: new_process_ip
        }
        new_group = deepcopy(self._groups[group_id])
        new_group[constants.MEMBERS_KEY].append(new_member)
        request_status = constants.COMMIT
        old_group = deepcopy(self._groups[group_id])
        # Request members to enter first stage of commit protocol
        # The following code should be threaded in theory
        for members_dict in old_group[constants.MEMBERS_KEY]:
            try:
                result = tx._request_first_stage_update(members_dict[constants.PID_KEY], members_dict[constants.IP_KEY], new_group, group_id)
                if not result:
                    request_status = constants.ABORT
                    break
            except CommsError as ce:
                # Handle unsuccessfull transmissions
                pass

        # Inform members of result of protocol
        for members_dict in old_group[constants.MEMBERS_KEY]:
            try: 
                result = tx._request_second_stage_update(members_dict[constants.PID_KEY], members_dict[constants.IP_KEY], group_id, request_status)
            except CommsError as ce:
                # Handle unsuccessful transmissions 
                pass

        if request_status == constants.COMMIT:
            return new_group   
        else:
            return False
        print("Result of request: ", request_status)
        

    def _coord_manage_leave(self, process_id, process_ip, group_id):
        """
        Called by coordinator after someone requests to leave the group,
        Manages leave by contacting everyone in the group telling them to enter
        first stage of 2-phase commit protol, if all respond with ack's, a second message
        is sent out to all members of the group telling them to commit changes (second
        stage of protocol)
        :param process_id process id of process that requested to leave the group
        :param process_ip process ip of process that requested to leave the group
        :param group_id group id of the group the process is trying to leave
        :returns:
        """
        
        new_group = deepcopy(self._groups[group_id])
        new_group[constants.MEMBERS_KEY][:] = [member for member in new_group[constants.MEMBERS_KEY] if not ((member.get(constants.PID_KEY) == process_id) and (member.get(constants.IP_KEY) == process_ip))]
        request_status = constants.COMMIT
        # Request members to enter first stage of commit protocol
        # The following code should be threaded in theory
        for members_dict in new_group[constants.MEMBERS_KEY]:
            try:
                result = tx._request_first_stage_update(members_dict[constants.PID_KEY], members_dict[constants.IP_KEY], new_group, group_id)
                if not result:
                    request_status = constants.ABORT
                    break
            except CommsError as ce:
                # Handle unsuccessfull transmissions
                pass

        # Inform members of result of protocol
        for members_dict in new_group[constants.MEMBERS_KEY]:
            try: 
                result = tx._request_second_stage_update(members_dict[constants.PID_KEY], members_dict[constants.IP_KEY], group_id, request_status)
            except CommsError as ce:
                # Handle unsuccessful transmissions 
                pass

        if request_status == constants.COMMIT:
            return new_group   
        else:
            return False
        print("Result of request: ", request_status)

    def _terminate(self):
        print("Terminating process")
        for group in self._groups:
            print(group)
        return




    def _debug(self):
        print("DEBUG BEGIN")
        print("process_id: " + self.process_id)
        print("groups: " , self._groups)
        print("temp_groups: ", self._temp_groups)
        print("DEBUG END")
