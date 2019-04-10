import tkinter
from tkinter import *
from tkinter.messagebox import showinfo

import sys
import threading

import client
import client_comms_rx as rx
import client_comms_tx as tx

#----functions---#
def create_process():
    process_id = entry_create_process.get()
    if(client.create_process(process_id)):
        processes_listbox.insert("end",process_id) 
        print("create_process!")
        showinfo(title="", message="Process created!")
    else:
        showinfo(title="", message="Failed!")

def destroy_process(process_id):
    print("destroy_process!")
    client.destroy_process(process_id)
    processes_listbox.delete(processes_listbox.get(0,"end").index(process_id))
    showinfo(title="", message="Process destroyed!")


def create_group(process_id,group_id,listbox):
    print("attempting to create group "+group_id)
    if(client.process_create_group(process_id,group_id)):
        print("create_group!")
        listbox.insert("end",group_id) 
        showinfo(title="", message="Group created!")
    else:
        showinfo(title="", message="Failed!")

def join_group(process_id,group_id,listbox):
    if (client.process_join_group(process_id,group_id)):
        print("join_group!")
        print("attempting to join " + group_id)
        listbox.insert("end",group_id)
        showinfo(title="", message="Group joined!")
    else:
        showinfo(title="", message="Failed!")

def leave_group(process_id,group_id,listbox):
    if (client.process_leave_group(process_id,group_id)):
        print("leave_group!")
        listbox.delete(listbox.get(0,"end").index(group_id))
        showinfo(title="", message="Group left!")
    else:
        showinfo(title="", message="Failed!")
        
def print_process_state(process_id):
    print("print_process_state!")
    client.print_process_state(process_id)

def print_all_process_state():
    print("print_all_process_state!")
    client.print_all_process_state()
    
def simulation():
    print("running simulation test")
    client.create_process("1")
    client.create_process("2")
    client.process_create_group("1","group_1")

def update_process_list():
    process_list = client._return_processes_ids
    processes_listbox.insert("end",*process_list) 


def listbox_select(event):
    process_selected = processes_listbox.get('active')
    print("current process "+process_selected)
    top_process = Toplevel()
    top_process.geometry("624x648")
    top_process.title("Process " + process_selected)
    groups_listbox = Listbox(top_process)
    groups_label = Label(top_process,text= "Groups part of:")
    groups_label.pack()
    
    # leave group that you select
    groups_listbox.pack()
    groups_id_list = client.return_groups_id(process_selected)
    groups_listbox.insert("end", *groups_id_list)
    leave_group_button = Button(top_process, text = "Leave Group", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: leave_group(process_selected,groups_listbox.get('active'),groups_listbox))
    leave_group_button.pack()
    
    # join group
    join_frame = Frame(top_process)
    join_frame.pack()
    label_join_group = Label(join_frame,text="ID:")
    label_join_group.grid(row=0,column=1)
    entry_join_group = Entry(join_frame)
    entry_join_group.grid(row=0,column=2)
    join_group_button= Button(join_frame, text = "Join Group", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: join_group(process_selected,entry_join_group.get(),groups_listbox))
    join_group_button.grid(row=0,column=0)

    # create group
    create_frame= Frame(top_process)
    create_frame.pack()
    label_create_group = Label(create_frame,text="ID:")
    label_create_group.grid(row=0,column=1)
    entry_create_group = Entry(create_frame)
    entry_create_group.grid(row=0,column=2)
    create_group_button= Button(create_frame, text = "Create Group", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: create_group(process_selected,entry_create_group.get(),groups_listbox))
    create_group_button.grid(row=0,column=0)

    # exit button
    exit_button = Button(top_process,text = "Exit",fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", command = top_process.destroy)
    exit_button.pack()
    
### main ####
t = rx.init()
r = tx.init()

# create window
window = tkinter.Tk()
window.title("GUI Launcher")
window.geometry("624x648") 
window.resizable(0, 0)

# process actions
create_process_button = Button(window, text = "Create Process", fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", command = create_process)
create_process_button.grid(row = 1, column = 1, padx = 1, pady = 1)
label_create_process = Label(window,text="ID")
label_create_process.grid(row=0,column=0)
entry_create_process = Entry(window)
entry_create_process.grid(row=0,column=1)

label_processes = Label(window,text="Processes:")
label_processes.grid(row=2,column=0)
processes_listbox = Listbox(window)
processes_listbox.grid(row=3,column=1)
processes_listbox.bind('<Double-1>',listbox_select)
destroy_button= Button(window,text = "Destroy Process",fg = "black", width = 10, height = 3, bd = 0, bg = "#fff", command = lambda: destroy_process(processes_listbox.get('active')))
destroy_button.grid(row=4,column=1)
window.mainloop()
