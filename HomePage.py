import datetime
import time

import pygame
import PySimpleGUI as sg

import Sounds
from DriverReportsPage import DriverReportsPage
from JsonFiles.JsonFuncs import JsonFuncs
from ParkingModePage import ParkingModePage
from RecordingPage import RecordingPage
from SettingsPage import SettingsPage
from Sounds.SoundFuncs import SoundFuncs

class HomePage:
    def openHomePage():  #user object will be passed in
        user = JsonFuncs.loadUserData()

        #maybe change theme based on time of day
        sg.theme('DarkAmber')
        
        rightAligned = [
            [sg.Button('Power Off')],
            [sg.Button('Settings')]
            ]
        centerAlignedText = [
            [sg.Text(text='', size = (10, 3))],
            [sg.Text(text=datetime.datetime.now().strftime('%m/%d/%Y'), key='-DATE-', font=['Lucida', 24]),
            sg.Text(text=time.strftime('%H:%M'), key='-TIME-', font=['Lucida', 24])],
            [sg.Text(text='Score: ' + str(user['aveScore']), key= '-SCORE-', font=['Lucida', 15])],
            [sg.Text(text='', size = (10, 2))]
            ]
        centerAligned = [
            [sg.Button('Parking Mode', size=(15, 3), font=['Lucida', 18]),
            sg.Text(text='', size = (1, 2)),
            sg.Button('Start Recording', size=(15, 3), font=['Lucida', 18]),
            sg.Text(text='', size = (1, 2)),
            sg.Button('View Driver Reports', size=(15, 3), font=['Lucida', 18])]
            ]

        '''
            [sg.Button('Power Off', 'right', size=(10,1))],
            [sg.Text(text=datetime.datetime.now().strftime('%m/%d/%Y'), key='-DATE-')],
            [sg.Text(text=time.strftime('%H:%M'), key='-TIME-')],
            [sg.Text(text='Score: ' + str(user['aveScore']), key= '-SCORE-')],
            [sg.Button('Settings', size=(15, 5)),
            sg.Button('Start Recording', size=(15, 5)),
            sg.Button('View Driver Reports', size=(15, 5))],'''
        homeLayout = [
            [sg.Column(rightAligned, vertical_alignment='right', justification='right', element_justification='right')],
            [sg.Column(centerAlignedText, vertical_alignment='center', justification='center', element_justification='center')],
            [sg.Column(centerAligned, vertical_alignment='center', justification='center')]
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
                SoundFuncs.playSound("Sounds/menuButtonClick.mp3")
                user = RecordingPage.openRecordingPage(homePageWindow, user)
                homePageWindow['-SCORE-'].update('Score: ' + str(user['aveScore']))
                homePageWindow.refresh()

            if event == 'View Driver Reports':  #and not driverReportPage_active:
                SoundFuncs.playSound('Sounds/menuButtonClick.mp3') #play button click sound
                user = DriverReportsPage.openDriverReportsPage(
                    homePageWindow, user)

            if event == 'Settings':
                SoundFuncs.playSound("Sounds/menuButtonClick.mp3")
                user = SettingsPage.openSettingsPage(user)

            if event == 'Parking Mode':
                SoundFuncs.playSound("Sounds/menuButtonClick.mp3")
                user = ParkingModePage.openParkingModePage(user)

            #update time
            homePageWindow['-TIME-'].update(time.strftime('%H:%M'))

            #update date
            homePageWindow['-DATE-'].update(
                datetime.datetime.now().strftime('%m/%d/%Y'))
            homePageWindow.finalize()
        
