import PySimpleGUI as sg


#maybe change theme based on time of day
sg.theme('DarkAmber')

#
layout = [[sg.Button('Start Recording')],
            [sg.Button('Settings')],
            [sg.Button('View Driver Reports')]]

window = sg.Window('Home', layout, no_titlebar=False, location=(0,0), size = (800,480)) #seet no_titlebar to true later

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window, end program
        break