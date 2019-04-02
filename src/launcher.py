"""
Main entry point to thee client side program. Users can issue commands via stdin to perform actions, such as creating
processes, destroying processes, creating groups, joining groups, etc.

Some of the commands we could take:

create_process -p id
destroy_process -p id
create_group -p process_id -g group_id
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
    t = rx.init()
    p1 = "p1"
    p2 = "p2"
    p3 = "p3"
    g1 = "g1"
    g2 = "g2"
    """
    client.create_process(p1)
    client.create_process(p2)
    client.create_process(p3)

    client.process_create_group(p1, g1)
    client.process_join_group(p2, g1)
    client.process_join_group(p3, g1)
    """
    #"print_process_state -p p1"
    while True:


        print("Enter a command. For help, type 'help'")
        command = sys.stdin.readline()
        command_lst = command.strip().split(" ")
        print(threading.current_thread())
        if command_lst[0] == "exit":
            print("exit! closing thread")
            
            break
        if command_lst[0] == "help":
            print("help!")
            help_text = "create_process -p id \n" \
                        "destroy_process -p id \n" \
                        "create_group -p process_id -g group_id \n" \
                        "join_group -p process_id -g group_id \n" \
                        "leave_group -p process_id -g group_id \n" \
                        "print_all_process_state \n" \
                        "print_process_state -p process_id \n" \
                        "print_group_state -p process_id -g group_id \n"
            print(help_text)
        elif command_lst[0] == "create_process" and command_lst[1] == "-p":
            print("create_process!")
            client.create_process(command_lst[2])
        elif command_lst[0] == "destroy_process" and command_lst[1] == "-p":
            print("destroy_process!")
            client.destroy_process(command_lst[2])
        elif command_lst[0] == "create_group" and command_lst[1] == "-p" and command_lst[3] == "-g":
            print("create_group!")
            client.process_create_group(command_lst[2], command_lst[4])
        elif command_lst[0] == "join_group" and command_lst[1] == "-p" and command_lst[3] == "-g":
            print("join_group!")
            client.process_join_group(command_lst[2], command_lst[4])
        elif command_lst[0] == "leave_group" and command_lst[1] == "-p" and command_lst[3] == "-g":
            print("leave_group!")
            client.process_leave_group(command_lst[2], command_lst[4])
        elif command_lst[0] == "print_process_state" and command_lst[1] == "-p":
            print("print_process_state!")
            client.print_process_state(command_lst[2])
        elif command_lst[0] == "print_all_process_state":
            print("print_all_process_state!")
            client.print_all_process_state()
        elif command_lst[0] == "test":
            print("running simulation test")
            client.create_process("1")
            client.create_process("2")
            client.process_create_group("1","group_1")
        else:
            print("Command not recognized. Use 'help' to get list of supported commands")
        
    return


if __name__ == "__main__":
    main()
