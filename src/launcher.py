"""
Main entry point to thee client side program. Users can issue commands via stdin to perform actions, such as creating
processes, destroying processes, creating groups, joining groups, etc.

Some of the commands we could take:

create_process -p id
destroy_process -p id
join_group -p process_id -g group_id
leave_group -p process_id -g group_id
print_all_process_state
print_process_state -p process_id
print_group_state -p process_id -g group_id
help
exit
"""

import sys
import threading

import client
import client_comms_rx as rx


def main():
    rx.init()
    while True:
        print("Enter a command. For help, type 'help'")
        command = sys.stdin.readline()
        command_lst = command.strip().split(" ")
        print(threading.current_thread())
        if command_lst[0] == "exit":
            print("exit!")
            break
        if command_lst[0] == "help":
            print("help!")
            help_text = "create_process -p id" \
                        "destroy_process -p id" \
                        "join_group -p process_id -g group_id" \
                        "leave_group -p process_id -g group_id" \
                        "print_all_process_state" \
                        "print_process_state -p process_id" \
                        "print_group_state -p process_id -g group_id"
            print(help_text)
        elif command_lst[0] == "create_process" and command_lst[1] == "-p":
            print("create_process!")
            client.create_process(int(command_lst[2]))
        elif command_lst[0] == "destroy_process" and command_lst[1] == "-p":
            print("destroy_process!")
            client.destroy_process(int(command_lst[2]))
        elif command_lst[0] == "join_group" and command_lst[1] == "-p" and command_lst[3] == "-g":
            print("join_group!")
            client.process_join_group(int(command_lst[2]), int(command_lst[4]))
        elif command_lst[0] == "leave_group" and command_lst[1] == "-p" and command_lst[3] == "-g":
            print("leave_group!")
            client.process_leave_group(int(command_lst[2]), int(command_lst[4]))
        else:
            print("Command not recognized. Use 'help' to get list of supported commands")
    return


if __name__ == "__main__":
    main()
