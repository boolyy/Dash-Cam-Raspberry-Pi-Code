import PySimpleGUI as sg
import pygame
from Sounds.SoundFuncs import SoundFuncs

class TripSummaryPage:
    def openTripSummaryPage(homePageWindow, user):
        #MAKE IT SHOW LIST OF
        #arrOfIncidents = TripSummaryPage.makeListBoxArray(user['driverReports'][len(user['driverReports']) - 1]['arrayOfIncidents']) #creates array that will be displayed in list box
        tripSummaryLayout = [[sg.Listbox(['hi', 'hi'])], [sg.Button('OK')]]
        tripSummaryPageWindow = sg.Window('Trip Summary',
                                          tripSummaryLayout,
                                          no_titlebar=False,
                                          location=(0, 0),
                                          size=(800, 480),
                                          finalize=True)
        while True:
            event, values = tripSummaryPageWindow.read()
            if event == sg.WIN_CLOSED or event == 'OK':
                SoundFuncs.playSound("Sounds/menuButtonClick.mp3")
                tripSummaryPageWindow.Close()
                break

    def makeListBoxArray(arrayOfIncidents):  #returns array of strings that will be shown
        arr = []  #array that will be returned
        for i in range(0, len(arrayOfIncidents)):
            str = arrayOfIncidents[i].timeOccured + "/t" + arrayOfIncidents[i].incidentType
            arr.append(str)
        return arr