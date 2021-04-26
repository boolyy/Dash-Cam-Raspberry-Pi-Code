import time
from datetime import date
import os
import pygame
import PySimpleGUI as sg
import theme
import cv2
from JsonFiles.JsonFuncs import JsonFuncs
from Objects.DriverReport import DriverReport
from Objects.Incident import Incident
from Objects.User import User
from Sounds.SoundFuncs import SoundFuncs
from TripSummaryPage import TripSummaryPage
from TFLite_detection_cam import *


class RecordingPage: #Page that opens when user starts recording
    def openRecordingPage(homePageWindow, user):
        sg.theme(theme.names[theme.index])
        
        #Make Driver Report object that will be created once recording is done
        today = date.today()
        driverReport = DriverReport(100,
                                    today.strftime("%m/%d/%Y"),
                                    startTime=time.strftime('%H:%M'),
                                    endTime='',
                                    arrayOfIncidents=[],
                                    vidPath = '')
        #deleteThisLayout = [
        #    [sg.Button('Make incident happen (FOR TROUBLESHOOTING)', key='-INCIDENT-')]
        #    ]

        bigButtonLayout = [
            [sg.Text(text='', size = (10, 8))],
            [sg.Button('Stop Recording', font=['Lucida', 50])]
            ]

        bottomTextLayout = [
            [sg.Text(text='Recording In Progress...', font=['Lucida', 15])]
            ]

        recordingPageLayout = [
            [sg.Button('Make incident happen (FOR TROUBLESHOOTING)', key='-INCIDENT-')],
            [sg.Column(bigButtonLayout, vertical_alignment='center', justification='center')],
            [sg.Column(bottomTextLayout, vertical_alignment='center', justification='center')]
            ]

        '''                            
        recordingPageLayout = [[sg.Button('Stop Recording')], 
                                [sg.Button('Make incident happen (FOR TROUBLESHOOTING)', key='-INCIDENT-')]]
        '''

        recordingPageWindow = sg.Window('Recording',
                                        recordingPageLayout,
                                        no_titlebar=True, 
                                        location=(0, 0),
                                        size=(800, 480),
                                        finalize=True)
        recordingPageWindow.Maximize()
        incidentOccured = False

        frame_rate_calc = 1
        freq = cv2.getTickFrequency()

        ''' ITEMS TO TRACK '''
        person = 0
        
        #Creates Video File for the output
        date_and_time = time.strftime("%Y%m%d-%H-%M-%S") #Stores current date and time in YYYY-MM-DD-HH:MM format
        PROJECT_DIR = os.getcwd()
        vid_out_path = os.path.join(PROJECT_DIR, 'Videos', date_and_time + '.mp4')

        #Starts the Thread which streams the output
        videostream = VideoStream(resolution=(imW,imH),framerate=30, path=0).start()

        width = int(videostream.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(videostream.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(videostream.stream.get(cv2.CAP_PROP_FPS))
        codec = cv2.VideoWriter_fourcc(*'XVID')
        output_video = cv2.VideoWriter(vid_out_path, codec, fps, (width,height))
        
        #time.sleep(1)
        while True:
            t1 = cv2.getTickCount()
            frame1 = videostream.read()
            names, frame_rate_calc, frame_out = capture(frame1, frame_rate_calc, t1)
            #print(names)
            output_video.write(frame_out)
            # get count of items
            personCount = names.get("person") if names.get("person") != None else 0

            # only logs 1 incident if #people in frame > #people previous frame
            if personCount > person:
                Incident.incidentHappened(user, driverReport, 'ranOverPedestrian')
            person = personCount
            
            if incidentOccured == True: #if some incident occurs
                Incident.incidentHappened(user, driverReport, 'ranOverPedestrian')
                incidentOccured = False

            event, values = recordingPageWindow.read(timeout = 10)
            
            if event == sg.WINDOW_CLOSED or event == 'Stop Recording' or cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                videostream.stop()
                
                #update user object
                SoundFuncs.playSound("Sounds/menuButtonClick.mp3")
                driverReport.endTime = time.strftime('%H:%M') #update end time of driverReport object
                driverReport.vidPath = vid_out_path
                user['numOfDriverReports'] = user['numOfDriverReports'] + 1 
                user['driverReports'].append(driverReport.__dict__)
                user['aveScore'] = User.calcAveScore(user) #update user's average score
                JsonFuncs.writeUserData(user)  #update JSON file
                TripSummaryPage.openTripSummaryPage(user['driverReports'][len(user['driverReports']) - 1]) #open trip summary page that will show user's a summary of their current trip
                recordingPageWindow.Close()  #close recording page

                return user
                break
            
            if event == '-INCIDENT-':
                incidentOccured = True

            # Press 'q' to quit
            #if cv2.waitKey(1) == ord('q'):
            #   break

        # Clean up
        #cv2.destroyAllWindows()
        #videostream.stop()    
