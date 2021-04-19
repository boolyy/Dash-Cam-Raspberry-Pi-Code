import pygame
import PySimpleGUI as sg
import theme

import Sounds
from Sounds.SoundFuncs import SoundFuncs


class TripSummaryPage:
    def openTripSummaryPage(driverReport):
        sg.theme(theme.names[theme.index])
        
        textLayout = [[sg.Text(text='', size = (10, 1))],
                      [sg.Text(text='Trip Summary', font=['Lucida', 24])],
                      [sg.Text(text='       Incidents', font=['Lucida', 18])]]
        columnLayout = [
                        [sg.Listbox(TripSummaryPage.makeListBoxArray(driverReport['arrayOfIncidents']), size = (30, 12), font=['Lucida', 14], key= '-LIST-')] 
                        ]
        buttonsLayout = [[sg.Button('OK', font=['Lucida', 14]), sg.Button('Open Video', font=['Lucida', 14])]]
        
        #tripSummaryLayout = [[sg.Text(text='Trip Summary')], [sg.Text(text='Incidents')], 
        #                    [sg.Listbox(TripSummaryPage.makeListBoxArray(driverReport['arrayOfIncidents']), size = (30, 6), key= '-LIST-')], 
        #                    [sg.Button('Back'), sg.Button('Open Video')]]
        tripSummaryLayout = [[sg.Column(textLayout, vertical_alignment='center', justification='center')],
                             [sg.Column(columnLayout, vertical_alignment='center', justification='center')],
                             [sg.Column(buttonsLayout, vertical_alignment='center', justification='center')]]
        
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
