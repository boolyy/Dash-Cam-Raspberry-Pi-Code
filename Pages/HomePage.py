import PySimpleGUI as sg
import pygame
from Pages.DriverReportsPage import DriverReportsPage
import Pages.VoiceAlerts
from Pages.JsonFiles.LoadUserData import LoadUserData
import datetime
import time


class HomePage:
    def openHomePage():  #user object will be passed in
        user = LoadUserData.loadUserData()

        #maybe change theme based on time of day
        sg.theme('DarkAmber')
        homeLayout = [
            [sg.Button('Start Recording', size=(20, 20))],
            [
                sg.Text(text=datetime.datetime.now().strftime('%m/%d/%Y'),
                        key='-DATE-')
            ], [sg.Text(text=time.strftime('%H:%M'), key='-TIME-')],
            [sg.Button('Settings')], [sg.Button('View Driver Reports')],
            [sg.Button('Play Sound')], [sg.Button('Cancel')]
        ]

        homePageWindow = sg.Window(
            'Home',
            homeLayout,
            no_titlebar=False,
            location=(0, 0),
            size=(800, 480),
            finalize=True)  #set no_titleb ar to true later
        homePageWindow.Maximize()

        #driverReportPage_active = False

        while True:
            event, values = homePageWindow.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window, end program
                homePageWindow.Close()
                break

            if event == 'Play Sound':
                print("Clicked Play Sound")
                pygame.mixer.init()
                pygame.mixer.music.load("Pages/VoiceAlerts/ranStopSign.mp3")
                pygame.mixer.music.play()
                #Code below is not necessary
                #while pygame.mixer.music.get_busy() == True:
                #    continue

            if event == 'Start Recording':
                print("Clicked Start Recording")

            if event == 'View Driver Reports':  #and not driverReportPage_active:
                print(user)
                user = DriverReportsPage.openDriverReportsPage(
                    homePageWindow, user)
                print("after")
                print(user)

            #update time
            homePageWindow['-TIME-'].update(time.strftime('%H:%M'))

            #update date
            homePageWindow['-DATE-'].update(
                datetime.datetime.now().strftime('%m/%d/%Y'))
            homePageWindow.finalize()
            #driverReportPage_active = True

            #homePageWindow.Hide()

            #driverReportLayout = [[sg.Button('Ok')],
            #            [sg.Button('Back')]]

            #driverReportsPageWindow = sg.Window('Driver Reports', driverReportLayout, no_titlebar=False, location=(0,0), size = (800,480), finalize = True) #set no_titlebar to true later
            #driverReportsPageWindow.Maximize()

            #while True:
            #    event1, values1 = driverReportsPageWindow.read()
            #    if event1 == sg.WIN_CLOSED or event1 == 'Back':
            #        driverReportsPageWindow.Close()
            #        driverReportPage_active = False
            #        homePageWindow.UnHide()
            #        break
            #    if event1 == 'Ok':
            #        print("Ok button pressed")
