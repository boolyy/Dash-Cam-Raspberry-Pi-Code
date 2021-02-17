import PySimpleGUI as sg
import pygame
import voiceAlerts

#maybe change theme based on time of day
sg.theme('DarkAmber')


layout = [[sg.Button('Start Recording')],
            [sg.Button('Settings')],
            [sg.Button('View Driver Reports')],
            [sg.Button('Play Sound')]]

window = sg.Window('Home', layout, no_titlebar=False, location=(0,0), size = (800,480)) #seet no_titlebar to true later

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window, end program
        break
    if event == 'Play Sound':
        pygame.mixer.init()
        pygame.mixer.music.load("voiceAlerts/ranStopSign.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
