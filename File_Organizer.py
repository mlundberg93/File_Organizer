import PySimpleGUI as sg
from pathlib import Path
import os
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

def refresh_list(window, folder_name, list_key):
    folder = values[folder_name]
    try:
        file_list = os.listdir(folder)
    except:
        file_list = []
    file_name = [f for f in file_list if os.path.isfile(os.path.join(folder, f))]
    window[list_key].update(file_name)

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
    elif event == "-Left Folder-":
        refresh_list(window, "-Left Folder-", "-Left List-")
    elif event == "-Right Folder-":
        refresh_list(window, "-Right Folder-", "-Right List-")
    elif event == "-Swap-":
        sg.popup_ok("Swap")
        refresh_list(window, "-Left Folder-", "-Left List-")
    elif event == "-Move-":
        sg.popup_ok("Move")
        refresh_list(window, "-Left Folder-", "-Left List-")
    elif event == "-Copy-":
        sg.popup_ok("Copy")
        refresh_list(window, "-Left Folder-", "-Left List-")
    elif event == "-Create-":
        sg.popup_ok("Create")
        refresh_list(window, "-Left Folder-", "-Left List-")