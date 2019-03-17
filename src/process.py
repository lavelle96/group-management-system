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

    def join_group(self, group_id):
        # get coordinator or create group
        try:
            (result, r_group_id, coordinator_ip, r_process_id) = tx.request_group_coordinator(group_id)
            if not result:
                (result, r_group_id, coordinator_ip, r_process_id) = tx.request_create_group(group_id, self.process_id)
                if not result:
                    print("Inconsistent or timing situation. Registry indicated that group didn't exist, but didn't allow creation of group")
                return
            else:
                (result, r_group_id, coordinator_ip, r_process_id) = tx.request_join_group(coordinator_ip, self.process_id, r_process_id, group_id)
        except CommsError as ce:
            return

    def leave_group(self, group_id):
        return

    def terminate(self):
        for group in self.groups:
            print(group)

    def debug(self):
        print("process_id: " + self.process_id)
        print("groups: " + self.groups)
        print("temp_groups: " + self.temp_groups)
