import time
from datetime import date

import pygame
import PySimpleGUI as sg

import Sounds
from JsonFiles.JsonFuncs import JsonFuncs
from Sounds.SoundFuncs import SoundFuncs


class ParkingModePage:
    def openParkingModePage(user):

        parkingPageLayout = [[sg.Text(text='Parking Mode Active')], [sg.Button('Stop Parking Mode')]]

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
                