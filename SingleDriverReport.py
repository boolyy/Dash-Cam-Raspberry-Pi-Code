import pygame
import PySimpleGUI as sg

import Sounds
from Sounds.SoundFuncs import SoundFuncs


class SingleDriverReport:
    def openSingleDriverReportPage(driverReport): #takes one Driver Report and will display list of incidents
        singleDriverReportLayout = [[sg.Listbox(driverReport.arrayOfIncidents)], 
                                    [sg.Button('OK')]]

        homePageWindow = sg.Window('Drive Report', singleDriverReportLayout,
                                    no_titlebar=False,
                                    location=(0, 0),
                                    size=(800, 480),
                                    finalize=True)

        singleDriverReportWindow = sg.Window('Driver Report', singleDriverReportLayout, 
                                            no_titlebar=False, location=(0,0), size=(800, 480),
                                            finalize= True)

        while True:
            event, values = singleDriverReportWindow.read()
            if event == sg.WIN_CLOSED or event == 'OK':
                SoundFuncs.playSound('Sounds/menuButtonClick.mp3')
                singleDriverReportWindow.Close()
                break
