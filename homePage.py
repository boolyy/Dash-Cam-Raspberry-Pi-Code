import PySimpleGUI as sg
import pygame
import voiceAlerts

#maybe change theme based on time of day
sg.theme('DarkAmber')

homeLayout = [[sg.Button('Start Recording', size = (20, 20))],
            [sg.Button('Settings')],
            [sg.Button('View Driver Reports')],
            [sg.Button('Play Sound')]]


homePageWindow = sg.Window('Home', homeLayout, no_titlebar=False, location=(0,0), size = (800,480)) #set no_titlebar to true later
driverReportPage_active = False

while True:
    
    event, values = homePageWindow.read()
    if event == sg.WIN_CLOSED: # if user closes window, end program
        break

    if event == 'Play Sound':
        pygame.mixer.init()
        pygame.mixer.music.load("voiceAlerts/ranStopSign.mp3")
        pygame.mixer.music.play()
        #Code below is not necessary
        #while pygame.mixer.music.get_busy() == True:
        #    continue

    if event == 'Start Recording':
        print("Clicked Start Recording")

    if event == 'Play Sound':
        print("Clicked Play Sound")

    if event == 'View Driver Reports' and not driverReportPage_active:
        print("Clicked View Driver Reports")
        driverReportPage_active = True
        homePageWindow.Hide()
        
        driverReportLayout = [[sg.Button('Ok')], 
                    [sg.Button('Back')]]

        driverReportsPageWindow = sg.Window('Driver Reports', driverReportLayout, no_titlebar=False, location=(0,0), size = (800,480)) #set no_titlebar to true later
        while True:
            event1, values1 = driverReportsPageWindow.read()
            if event1 == sg.WIN_CLOSED or event1 == 'Back':
                driverReportsPageWindow.Close()
                driverReportPage_active = False
                homePageWindow.UnHide()
                break
            if event1 == 'Ok':
                print("Ok button pressed")

                



    
