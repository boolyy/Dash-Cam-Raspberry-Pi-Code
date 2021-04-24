import time
from datetime import date

import pygame
import PySimpleGUI as sg
import theme

import Sounds
from JsonFiles.JsonFuncs import JsonFuncs
from Sounds.SoundFuncs import SoundFuncs


class ParkingModePage:
    def openParkingModePage(user):
        sg.theme(theme.names[theme.index])

        bigButtonLayout = [
            [sg.Text(text='', size = (10, 10))],
            [sg.Button('Stop Parking Mode', font=['Lucida', 50])]
            ]

        bottomTextLayout = [
            [sg.Text(text='Parking Mode Active', font=['Lucida', 15])]
            ]
        
        #parkingPageLayout = [[sg.Text(text='Parking Mode Active')], [sg.Button('Stop Parking Mode')]]
        parkingPageLayout = [
            [sg.Column(bigButtonLayout, vertical_alignment='center', justification='center')],
            [sg.Column(bottomTextLayout, vertical_alignment='center', justification='center')]
            ]

        parkingPageWindow = sg.Window('Parking Mode', parkingPageLayout,
                                        no_titlebar= False, location=(0,0),
                                        size=(800, 480), finalize= True)

        while True:
            event, values = parkingPageWindow.read()
            if event == sg.WINDOW_CLOSED or event == 'Stop Parking Mode':
                SoundFuncs.playSound('Sounds/menuButtonClick.mp3')
                JsonFuncs.writeUserData(user)
                parkingPageWindow.Close()
                return user
                break
                
