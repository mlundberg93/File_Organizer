import PySimpleGUI as sg
from pathlib import Path
import os
import shutil
import logging
from datetime import date
sg.theme("Reds")

if not os.path.exists("./loggs/"):
    os.makedirs("./loggs/")
logging.basicConfig(filename = "./loggs/log-" + str(date.today()) + ".txt", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Started Program")

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

def create_dir(base_path):
    answer = sg.popup_yes_no("Do you want to create more than one folder?")
    if answer == "Yes":
        location = sg.popup_get_folder("Choose the location you want to create the folders:")
        if location:
            num_folders = sg.popup_get_text("How many folders do you want to create?")
            try:
                num_folders = int(num_folders)
                for i in range(num_folders):
                    folder_name = sg.popup_get_text(f"Enter the name for the folders {i+1}:", default_text = f"Folder_{i+1}")
                    if folder_name:
                        folder_path = os.path.join(location, folder_name)
                        os.makedirs(folder_path)
                        logging.info(f"Created {folder_name}.")
                        sg.popup_ok(f"Folder {folder_name} has been successfully created!") 
            except ValueError:
                sg.popup_error("Invalid input for the number of folders, try again!")                             
           
    elif answer == "No":
        location = sg.popup_get_folder("Choose the location you want to create the folder:")
        if location:
                folder_name = sg.popup_get_text("Enter the name for the folder:", default_text = "Folder")
                if folder_name:
                    folder_path = os.path.join(location, folder_name)
                    os.makedirs(folder_path)
                    logging.info(f"Created {folder_name}.")
                    sg.popup_ok(f"Folder {folder_name} has successfully been created!")

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
                    logging.info("Moved %s -> %s", file, destination)
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
                logging.info("Copied %s -> %s", file, destination)
                sg.popup_ok("The file was successfully copied!")
            else:
                sg.popup_error("The file already exist in this folder!")
        except (IndexError) as idx_exc:
            sg.popup_error("Please select a file you wish to copy!")
        refresh_list(window, "-Left Folder-", "-Left List-")
        refresh_list(window, "-Right Folder-", "-Right List-")

    elif event == "-Create-":
        create_dir(values["-Left Folder-"] if target_direction == "Right" else values["-Right Folder-"])
        refresh_list(window, "-Left Folder-", "-Left List-")
        refresh_list(window, "-Right Folder-", "-Right List-")
        