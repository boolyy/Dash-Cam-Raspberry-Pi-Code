import pygame
import PySimpleGUI as sg

import Sounds
from Sounds.SoundFuncs import SoundFuncs


class TripSummaryPage:
    def openTripSummaryPage(driverReport):
        tripSummaryLayout = [[sg.Text(text='Trip Summary')], [sg.Text(text='Incidents')], [sg.Listbox(TripSummaryPage.makeListBoxArray(driverReport['arrayOfIncidents']), size = (30, 6))], 
                            [sg.Button('OK')]]
        
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
            str = arrayOfIncidents[i]['timeOccured'] + ' ' + arrayOfIncidents[i]['incidentType']
            arr.append(str)
        return arr
