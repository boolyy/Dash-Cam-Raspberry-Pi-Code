import PySimpleGUI as sg
from Sounds.SoundFuncs import SoundFuncs

class DriverReportsPage: #will show list of incidents
    def openDriverReportsPage(homePageWindow, user):
        #driverReportPage_active = True
        #arrOfDriverReports = DriverReportsPage.makeListBoxArray(user['driverReports'][len(user['driverReports']) - 1])
        driverReportLayout = [[sg.Button('Ok')], [sg.Button('Back')],
                                [sg.Listbox('hi', 'hi')]]

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
                SoundFuncs.playSound("Sounds/menuButtonClick.mp3")
                driverReportPage_active = False
                homePageWindow.UnHide()
                driverReportsPageWindow.Close()
                #UPDATE USER JSON
                return user
                break

            if event1 == 'Ok':
                SoundFuncs.playSound("Sounds/menuButtonClick.mp3")
                print("Ok button pressed")

    def makeListBoxArray(arrayOfDriverReports):
        arr = []
        for i in range(0, len(arrayOfDriverReports)): #create string with all the basic information about driver report
            str = arrayOfDriverReports[i]
            arr.append(str)
        return arr
