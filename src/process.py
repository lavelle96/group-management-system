import client_comms_tx as tx


class Process:
    def __init__(self, process_id):
        self.process_id = process_id
        self.groups = {}
        self.temp_groups = {}
        self.is_coordinator = False

    def prepare_update_group(self, group_id, group):
        if group_id in self.groups and group_id not in self.temp_groups:
            self.temp_groups[group_id] = group
            return True
        else:
            self.debug()
            return False

    def commit(self, group_id):
        if group_id in self.temp_groups:
            group = deepcopy(self.temp_groups[group_id])
            del self.temp_groups[group_id]
            self.groups[group_id] = group
            return True
        else:
            self.debug()
            return False

    def abort(self, group_id):
        if group_id in self.temp_groups:
            del self.temp_groups[group_id]
            return True
        else:
            self.debug()
            return False

    def check(self):
        return True

    def create_group(self, group_id):
        # get coordinator or create group
        try:
            (result, r_group_id, r_coordinator_ip, r_process_id) = tx.request_group_coordinator(group_id)
            if not result:
                (result, r_group_id, r_coordinator_ip, r_process_id) = tx.request_create_group(group_id,
                                                                                               self.process_id)
                if result:
                    self.groups[r_group_id] = self.create_own_group(r_group_id, r_coordinator_ip, r_process_id)
                else:
                    print(
                        "Inconsistent or timing situation. Registry indicated that group didn't exist, but didn't allow creation of group")
                    return
        except CommsError as ce:
            return

    def join_group(self, group_id):
        # get coordinator or create group
        try:
            (result, r_group_id, r_coordinator_ip, r_process_id) = tx.request_group_coordinator(group_id)
            if result:
                (result, r_group_id, coordinator_ip, r_process_id) = tx.request_join_group(coordinator_ip,
                                                                                           self.process_id,
                                                                                           r_process_id, group_id)
                if not result:
                    print("Inconsistent or timing situation. Coordinator indicated that join operation failed")
                    return
        except CommsError as ce:
            return

    def leave_group(self, group_id):
        return

    def terminate(self):
        for group in self.groups:
            print(group)

    def debug(self):
        print("DEBUG BEGIN")
        print("process_id: " + self.process_id)
        print("groups: " + self.groups)
        print("temp_groups: " + self.temp_groups)
        print("DEBUG END")

    def create_own_group(self, r_group_id, r_coordinator_ip, r_process_id):
        group = {constants.GID_KEY: r_group_id,
                 constants.COORD_IP_KEY: r_coordinator_ip,
                 constants.PID_KEY: r_process_id,
                 constants.MEMBERS_KEY: [
                     {
                         constants.COORD_IP_KEY: r_coordinator_ip,
                         constants.PID_KEY: r_process_id
                     }
                 ]
                 }
        return group
