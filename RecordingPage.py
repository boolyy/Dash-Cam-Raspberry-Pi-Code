import time
from datetime import date

import pygame
import PySimpleGUI as sg

from JsonFiles.JsonFuncs import JsonFuncs
from Objects.DriverReport import DriverReport
from Sounds.SoundFuncs import SoundFuncs
from TripSummaryPage import TripSummaryPage


class RecordingPage: #Page that opens when user starts recording
    def openRecordingPage(homePageWindow, user):
        #Make Driver Report object that will be created once recording is done
        today = date.today()
        driverReport = DriverReport(100,
                                    today.strftime("%m/%d/%Y"),
                                    startTime=time.strftime('%H:%M'),
                                    endTime='',
                                    arrayOfIncidents=[])
        recordingPageLayout = [[sg.Button('Stop Recording')]]

        recordingPageWindow = sg.Window('Recording',
                                        recordingPageLayout,
                                        no_titlebar=False,
                                        location=(0, 0),
                                        size=(800, 480),
                                        finalize=True)
        #recordingPageWindow.Maximize()

        while True:
            event, values = recordingPageWindow.read()
            if event == sg.WINDOW_CLOSED or event == 'Stop Recording':
                #update user object
                SoundFuncs.playSound("Sounds/menuButtonClick.mp3")
                driverReport.arrayOfIncidents.append('hi') #NEED TO ADD INCIDENT HERE
                user['numOfDriverReports'] += 1
                user['driverReports'].append(driverReport.__dict__)
                user['aveScore'] = (user['aveScore'] + driverReport.score
                                    ) / user['numOfDriverReports']
                #user['aveScore'] += 100
                JsonFuncs.writeUserData(user)  #update JSON file
                TripSummaryPage.openTripSummaryPage(homePageWindow, user) #open trip summary page that will show user's a summary of their current trip
                recordingPageWindow.Close()  #close recording page

                return user
                break
