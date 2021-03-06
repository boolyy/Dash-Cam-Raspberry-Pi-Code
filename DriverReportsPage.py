import PySimpleGUI as sg

import Sounds
from Sounds.SoundFuncs import SoundFuncs

from TripSummaryPage import TripSummaryPage

class DriverReportsPage: #will show list of incidents
    def openDriverReportsPage(homePageWindow, user):
        listBoxArray = DriverReportsPage.makeListBoxArray(user['driverReports'])
        #driverReportPage_active = True
        #arrOfDriverReports = DriverReportsPage.makeListBoxArray(user['driverReports'][len(user['driverReports']) - 1])
        driverReportLayout = [[sg.Button('Open Selected Driver Report')], [sg.Button('Back')],
                                [sg.Listbox(listBoxArray, enable_events=True, size=(30,6), 
                                            auto_size_text=True, key='-LIST-', select_mode= 'single')]]

        driverReportsPageWindow = sg.Window(
            'Driver Reports',
            driverReportLayout,
            no_titlebar= False,
            location=(0, 0),
            size=(800, 480),
            finalize=True)  #set no_titlebar to true later
        #driverReportsPageWindow.Maximize()

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

            if event1 == 'Open Selected Driver Report': #open driver report that corresponds with the selected item
                SoundFuncs.playSound("Sounds/menuButtonClick.mp3")

                if(values1['-LIST-']): #make sure that something is selected in List Box
                    userDriverReportsIndex = listBoxArray.index(values1['-LIST-'][0]) #get index of driver report representation in listbox array
                    userDriverReportsIndex = (len(listBoxArray) - 1) - userDriverReportsIndex #get index of driver report in user dict
                    TripSummaryPage.openTripSummaryPage(user['driverReports'][userDriverReportsIndex])
        
    def makeListBoxArray(arrayOfDriverReports): #represents array of driver reports as array of strings to store in list box
        arr = []
        #Use reversed loop to show the latest driver reports first in the 
        for i in reversed(range(len(arrayOfDriverReports))): #create string with all the basic information about driver report
            string = "Score:" + str(arrayOfDriverReports[i]['score']) + '  ' + arrayOfDriverReports[i]['date'] + '  ' + arrayOfDriverReports[i]['startTime']
            arr.append(string)
        return arr
