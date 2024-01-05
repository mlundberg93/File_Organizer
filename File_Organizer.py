import PySimpleGUI as sg
from pathlib import Path
import os
import shutil
import logging

sg.theme("Reds")

left_side = [
    [
        sg.Text("Left folder"),
        sg.In(size = (25,1), enable_events = True, key = "-Left Folder-"),
        sg.FolderBrowse(),
    ],
    [       
        sg.Listbox(values = [], enable_events = True, size = (40,20), key = "-Left List-")
    ]
]
right_side = [
    [
        sg.Text("Right Folder"),
        sg.In(size=(25,1), enable_events=True, key="-Right Folder-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(values=[], enable_events=True, size=(40,20), key="-Right List-")
    ]
]
button_size = (10,3)
middle_menu = [
        [
            sg.Button("-->", enable_events = True, key = "-Swap-", size = button_size)
        ],
        [
            sg.Button("Move", enable_events = True, key = "-Move-", size = button_size),
        ], 
        [
            sg.Button("Copy", enable_events = True, key = "-Copy-", size = button_size),
        ], 
        [
            sg.Button("Create folder", enable_events = True, key = "-Create-", size = button_size),
        ], 
        [
            sg.Exit(button_color="tomato", size = (10,5))
        ]  
]
layout = [[sg.Column(left_side), sg.Column(middle_menu), sg.Column(right_side)]]
window = sg.Window("File Organizer", layout, finalize = True, use_custom_titlebar = True)

def refresh_list(window, folder_key, list_key):     #Updates the items in the list, so the user can see what
                                                    #is in the list currently
    folder = values[folder_key]
    try:
        file_list = os.listdir(folder)
    except:
        file_list = []
    file_name = [f for f in file_list if os.path.isfile(os.path.join(folder, f))]
    window[list_key].update(file_name)

def get_valid_path(file_path):  #Checks if the path is correct
    if file_path and Path(file_path).exists():
        return True
    sg.popup_error("Your path is not correct!")
    return False

def swap_direction():   #Helping the swap-feature to be able to switch which way you can move/copy items
    if target_direction == "Right":
        file = os.path.join(values["-Left Folder-"], values["-Left List-"][0])
        destination = values["-Right Folder-"]
    else:
        file = os.path.join(values["-Right Folder-"], values["-Right List-"][0])
        destination = values["-Left Folder-"]
    return file, destination

target_direction = "Right"

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
    elif event == "-Left Folder-":
        refresh_list(window, "-Left Folder-", "-Left List-")

    elif event == "-Right Folder-":
        refresh_list(window, "-Right Folder-", "-Right List-")

    elif event == "-Swap-":
        if target_direction == "Right":
            target_direction = "Left"
            window["-Swap-"].update("<--")
        else:
            target_direction = "Right"
            window["-Swap-"].update("-->")
        refresh_list(window, "-Left Folder-", "-Left List-")
        refresh_list(window, "-Right Folder-", "-Right List-")

    elif event == "-Move-":
        if (get_valid_path(values["-Left Folder-"])) and (get_valid_path(values["-Right Folder-"])):
            try:
                file, destination = swap_direction()
                check_list = values["-Left List-" if target_direction == "Right" else "-Right List-"]
                check = os.path.join(destination, check_list[0]) if check_list else None
                if not os.path.exists(check):
                    shutil.move(file, destination)
                    sg.popup_ok("Successfully moved the file!")
                else:
                    sg.popup_error("The file already exists in this folder!")
            except (IndexError) as idxExc:
                sg.popup_error("Please select a file to move!")
        refresh_list(window, "-Left Folder-", "-Left List-")
        refresh_list(window, "-Right Folder-", "-Right List-")

    elif event == "-Copy-":
        try:
            file, destination = swap_direction()
            check_list = values["-Left List-" if target_direction == "Right" else "-Right List-"]
            check = os.path.join(destination, check_list[0]) if check_list else None
            if not os.path.exists(check):
                shutil.copy(file, destination)
                sg.popup_ok("The file was successfully copied!")
            else:
                sg.popup_error("The file already exist in this folder!")
        except (IndexError) as idx_exc:
            sg.popup_error("Please select a file you wish to copy!")
        refresh_list(window, "-Left Folder-", "-Left List-")
        refresh_list(window, "-Right Folder-", "-Right List-")

    elif event == "-Create-":
        sg.popup_ok("Create")
        refresh_list(window, "-Left Folder-", "-Left List-")
        refresh_list(window, "-Right Folder-", "-Right List-")