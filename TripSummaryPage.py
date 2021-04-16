import pygame
import PySimpleGUI as sg

import Sounds
from Sounds.SoundFuncs import SoundFuncs


class TripSummaryPage:
    def openTripSummaryPage(driverReport):
        textLayout = [[sg.Text(text='', size = (10, 2))],
                        [sg.Text(text='Trip Summary')], [sg.Text(text='Incidents')]]
        columnLayout = [
                            [sg.Listbox(TripSummaryPage.makeListBoxArray(driverReport['arrayOfIncidents']), size = (30, 15), key= '-LIST-')], 
                            [sg.Button('OK'), sg.Button('Open Video')]]
        
        #tripSummaryLayout = [[sg.Text(text='Trip Summary')], [sg.Text(text='Incidents')], 
        #                    [sg.Listbox(TripSummaryPage.makeListBoxArray(driverReport['arrayOfIncidents']), size = (30, 6), key= '-LIST-')], 
        #                    [sg.Button('Back'), sg.Button('Open Video')]]
        tripSummaryLayout = [[sg.Column(textLayout, vertical_alignment='center', justification='center')],
                              [sg.Column(columnLayout, vertical_alignment='center', justification='center')]]
        
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

            if event == 'Open Video':
                print("Clicked Open Video")
                values['-LIST-']
                
                
    def makeListBoxArray(arrayOfIncidents):  #returns array of strings that will be shown
        arr = []  #array that will be returned
        for i in range(0, len(arrayOfIncidents)):
            str = arrayOfIncidents[i]['timeOccured'] + ' ' + arrayOfIncidents[i]['incidentType']
            arr.append(str)
        return arr
