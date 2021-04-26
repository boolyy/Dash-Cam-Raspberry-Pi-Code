import pygame
import PySimpleGUI as sg
import theme
import time
import cv2
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
                                          no_titlebar=True,
                                          location=(0, 0),
                                          size=(800, 480),
                                          finalize=True)
        tripSummaryPageWindow.Maximize()

        try:
            preview_path = driverReport['vidPath']
        except:
            preview_path = 0

        while True:
            event, values = tripSummaryPageWindow.read()
            
            if event == sg.WIN_CLOSED or event == 'OK':
                SoundFuncs.playSound("Sounds/menuButtonClick.mp3")
                tripSummaryPageWindow.Close()
                break

            if event == 'Open Video' and preview_path != 0:
                print("Clicked Open Video")
                cap = cv2.VideoCapture(preview_path)
                cap_fps = int(cap.get(cv2.CAP_PROP_FPS))

                while cap.isOpened():
                    ret, f = cap.read()

                    if ret == True:
                        time.sleep(1/cap_fps)
                        cv2.imshow('Report Video', f)
                        if cv2.waitKey(1) and 0xFF == ord('q') or ret == False:
                            break
                    else:
                        break
                cap.release()
                cv2.destroyAllWindows()
            
            else:
                print("Video may have been deleted or renamed\n")
                values['-LIST-']
                
                
    def makeListBoxArray(arrayOfIncidents):  #returns array of strings that will be shown
        arr = []  #array that will be returned
        for i in range(0, len(arrayOfIncidents)):
            str = arrayOfIncidents[i]['timeOccured'] + ' ' + arrayOfIncidents[i]['incidentType']
            arr.append(str)
        return arr
