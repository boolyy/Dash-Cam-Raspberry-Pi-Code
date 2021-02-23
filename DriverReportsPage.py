import PySimpleGUI as sg
from VoiceAlerts.VoiceFuncs import VoiceFuncs

class DriverReportsPage:
    def openDriverReportsPage(homePageWindow, user):
        #driverReportPage_active = True
        driverReportLayout = [[sg.Button('Ok')], [sg.Button('Back')]]

        driverReportsPageWindow = sg.Window(
            'Driver Reports',
            driverReportLayout,
            no_titlebar=False,
            location=(0, 0),
            size=(800, 480),
            finalize=True)  #set no_titlebar to true later
        driverReportsPageWindow.Maximize()

        while True:
            event1, values1 = driverReportsPageWindow.read()
            if event1 == sg.WIN_CLOSED or event1 == 'Back':
                VoiceFuncs.playSound('VoiceAlerts/menuButtonClick.mp3')
                driverReportPage_active = False
                homePageWindow.UnHide()
                driverReportsPageWindow.Close()
                #UPDATE USER JSON
                return user
                break
            if event1 == 'Ok':
                VoiceFuncs.playSound('VoiceAlerts/menuButtonClick.mp3')
                print("Ok button pressed")
