from src.client import create_process, process_create_group, process_join_group, _processes

def create_test_group():
    create_process("1")
    create_process("2")
    create_process("3")
    process_create_group("1","1")
    process_join_group("3","1")
    print(_processes)

"""
def test_initial_coordinator():
    create_test_group()
"""

if __name__=="__main__":
    create_test_group()
    #result=test_group_view()
    #print("Group View Functionality Test Passed: "+str(result))
