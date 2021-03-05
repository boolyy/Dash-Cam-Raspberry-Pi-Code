import datetime
import time

import pygame
import PySimpleGUI as sg

import Sounds
from DriverReportsPage import DriverReportsPage
from JsonFiles.JsonFuncs import JsonFuncs
from RecordingPage import RecordingPage
from SettingsPage import SettingsPage
from ParkingModePage import ParkingModePage
from Sounds.SoundFuncs import SoundFuncs


class HomePage:
    def openHomePage():  #user object will be passed in
        user = JsonFuncs.loadUserData()

        #maybe change theme based on time of day
        sg.theme('DarkAmber')
        homeLayout = [
            [sg.Button('Start Recording', size=(10, 10))],
            [sg.Text(text=datetime.datetime.now().strftime('%m/%d/%Y'), key='-DATE-')],
            [sg.Text(text=time.strftime('%H:%M'), key='-TIME-')],
            [sg.Button('Settings')], [sg.Button('View Driver Reports')], 
            [sg.Button('Power Off')], [sg.Button('Parking Mode')]
        ]

        homePageWindow = sg.Window(
            'Home',
            homeLayout,
            no_titlebar=False,
            location=(0, 0),
            size=(800, 480),
            finalize=True)  #set no_titleb ar to true later
        #homePageWindow.Maximize()


        while True:
            event, values = homePageWindow.read()
            if event == sg.WIN_CLOSED or event == 'Power Off':  # if user closes window, end program
                SoundFuncs.playSound('Sounds/menuButtonClick.mp3')
                homePageWindow.Close()
                break

            if event == 'Start Recording':
                print("Clicked Start Recording")
                SoundFuncs.playSound("Sounds/menuButtonClick.mp3")
                user = RecordingPage.openRecordingPage(homePageWindow, user)

            if event == 'View Driver Reports':  #and not driverReportPage_active:
                SoundFuncs.playSound('Sounds/menuButtonClick.mp3') #play button click sound
                user = DriverReportsPage.openDriverReportsPage(
                    homePageWindow, user)

            if event == 'Settings':
                print('Settings')
                SoundFuncs.playSound("Sounds/menuButtonClick.mp3")
                user = SettingsPage.openSettingsPage(user)

            if event == 'Parking Mode':
                print("Parking mode")
                SoundFuncs.playSound("Sounds/menuButtonClick.mp3")
                user = ParkingModePage.openParkingModePage(user)

            #update time
            homePageWindow['-TIME-'].update(time.strftime('%H:%M'))

            #update date
            homePageWindow['-DATE-'].update(
                datetime.datetime.now().strftime('%m/%d/%Y'))
            homePageWindow.finalize()
        