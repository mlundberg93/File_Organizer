import PySimpleGUI as sg
sg.theme("Reds")

left_side = [
    [
        sg.Text("Left folder"),
        sg.Input(size=(20,5), key="-Left Folder-"),
        sg.FolderBrowse()
    ],
    [
        sg.Text("Folder List"),
        sg.Listbox(values=[], size=(40,20), key="-Left List-")
    ]
]
right_side = [
        [sg.Text("Right Folder"),
        sg.Input(size=(20,5), key="-Right Folder-"),
        sg.FolderBrowse()
    ],
    [
        sg.Text("Folder List"),
        sg.Listbox(values=[], size=(40,20), key="-Right List-")
    ]
]
bottom_menu = [
    [    
        sg.Button("Move"), 
        sg.Button("Copy"), 
        sg.Button("Create folder"), 
        sg.Exit(button_color="tomato", s=15)
    ]
]
layout = [
    [
        sg.Column(left_side),
        sg.VSeperator(),
        sg.Column(right_side),
    ],
    [sg.HSeparator()],
    [sg.Column(bottom_menu, justification="r")]
]
window = sg.Window("File Organizer", layout, use_custom_titlebar=True)

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
