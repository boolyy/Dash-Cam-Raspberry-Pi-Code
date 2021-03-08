import time
from datetime import date

import pygame
import PySimpleGUI as sg

from JsonFiles.JsonFuncs import JsonFuncs
from Objects.DriverReport import DriverReport
from Objects.Incident import Incident
from Objects.User import User
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
                                    
        recordingPageLayout = [[sg.Button('Stop Recording')], 
                                [sg.Button('Make incident happen (FOR TROUBLESHOOTING)', key='-INCIDENT-')]]

        recordingPageWindow = sg.Window('Recording',
                                        recordingPageLayout,
                                        no_titlebar=False, 
                                        location=(0, 0),
                                        size=(800, 480),
                                        finalize=True)
        #recordingPageWindow.Maximize()
        incidentOccured = False
        while True:

            if incidentOccured == True: #if some incident occurs
                #update current score
                #make incident object
                today = date.today() #get current time
                incident = Incident(today.strftime("%m/%d/%Y"), time.strftime('%H:%M'), 
                                    'Ran over a pedestrian', 50)
                print("video title: " + incident.videoTitle)
                #alter driver report
                driverReport.score -= incident.incidentValue
                driverReport.arrayOfIncidents.append(incident.__dict__) #append incident to list of incidents in a dict format

                incidentOccured = False
                
            event, values = recordingPageWindow.read()

            if event == sg.WINDOW_CLOSED or event == 'Stop Recording':
                #update user object
                SoundFuncs.playSound("Sounds/menuButtonClick.mp3")
                driverReport.endTime = time.strftime('%H:%M') #update end time of driverReport object

                #print(str(user['numOfDriverReports']))
                user['numOfDriverReports'] = user['numOfDriverReports'] + 1

                user['driverReports'].append(driverReport.__dict__)
                #make ave score
                user['aveScore'] = User.calcAveScore(user)
                print('Ave Score ' + str(user['aveScore']))
                #user['aveScore'] += 100
                JsonFuncs.writeUserData(user)  #update JSON file
                TripSummaryPage.openTripSummaryPage(user['driverReports'][len(user['driverReports']) - 1]) #open trip summary page that will show user's a summary of their current trip
                recordingPageWindow.Close()  #close recording page

                return user
                break
            
            if event == '-INCIDENT-':
                incidentOccured = True