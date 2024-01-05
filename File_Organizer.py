import PySimpleGUI as sg
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

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
