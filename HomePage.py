import PySimpleGUI as sg
import pygame
import VoiceAlerts
import datetime
import time
from VoiceAlerts.VoiceFuncs import VoiceFuncs
from JsonFiles.JsonFuncs import JsonFuncs
from DriverReportsPage import DriverReportsPage
from RecordingPage import RecordingPage
from SettingsPage import SettingsPage


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
            [sg.Button('Cancel')]
        ]

        homePageWindow = sg.Window(
            'Home',
            homeLayout,
            no_titlebar=False,
            location=(0, 0),
            size=(800, 480),
            finalize=True)  #set no_titleb ar to true later
        #homePageWindow.Maximize()

        #driverReportPage_active = False

        while True:
            event, values = homePageWindow.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window, end program
                VoiceFuncs.playSound('VoiceAlerts/menuButtonClick.mp3')
                homePageWindow.Close()
                break

            if event == 'Start Recording':
                print("Clicked Start Recording")
                VoiceFuncs.playSound("VoiceAlerts/menuButtonClick.mp3")
                user = RecordingPage.openRecordingPage(homePageWindow, user)

            if event == 'View Driver Reports':  #and not driverReportPage_active:
                print(user)
                VoiceFuncs.playSound('VoiceAlerts/menuButtonClick.mp3') #play button click sound
                user = DriverReportsPage.openDriverReportsPage(
                    homePageWindow, user)
                print("after")
                print(user)

            if event == 'Settings':
                print('Settings')
                VoiceFuncs.playSound("VoiceAlerts/menuButtonClick.mp3")
                user = SettingsPage.openSettingsPage(user)


            #update time
            homePageWindow['-TIME-'].update(time.strftime('%H:%M'))

            #update date
            homePageWindow['-DATE-'].update(
                datetime.datetime.now().strftime('%m/%d/%Y'))
            homePageWindow.finalize()
        