import PySimpleGUI as sg

layout = [[sg.Button('Ok')]]

window = sg.Window('Driver Reports', layout, no_titlebar=False, location=(0,0), size = (800,480)) #set no_titlebar to true later

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Ok':
        print("Button Ok pressed")
