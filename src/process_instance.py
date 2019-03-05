"""
Entry point of the program, this is the python file you run to get a machine online
First thing they do is contact the registry to tell them whether or not they want

Could be an issue having a process being able to switch from being a client to being a coordinator.
"""

if __name__ == '__main__':
    # Do you want to join existing group or create new group

    while(1):
        pref_1 = input("Do you want to join existing group (1), create new group (2) or exit (3)")
        if pref_1 == '1':
            # Ask registry for list of existing groups, and attempt to join one
            pass
        elif pref_1 == '2':
            # Create new group
            pass
        elif pref_1 == '3':
            break
