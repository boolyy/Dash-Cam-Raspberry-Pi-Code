import pygame
import PySimpleGUI as sg
import cv2
import Sounds
import time
from Sounds.SoundFuncs import SoundFuncs
from TFLite_detection_cam import VideoStream

class TripSummaryPage:
    def openTripSummaryPage(driverReport):
        tripSummaryLayout = [[sg.Text(text='Trip Summary')], [sg.Text(text='Incidents')], 
                            [sg.Listbox(TripSummaryPage.makeListBoxArray(driverReport['arrayOfIncidents']), size = (30, 6), key= '-LIST-')], 
                            [sg.Button('OK')], [sg.Button('Open Video')]]
        
        tripSummaryPageWindow = sg.Window('Trip Summary',
                                          tripSummaryLayout,
                                          no_titlebar=False,
                                          location=(0, 0),
                                          size=(800, 480),
                                          finalize=True)

        
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

            print("Preview Path: ", preview_path)

            # Will open video after recording unless the file was renamed or deleted
            # IT WILL PLAY THE WHOLE VIDEO
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
                    else: break
                cap.release()
                cv2.destroyAllWindows()
                    
                # videothread = VideoStream(resolution = (640,480), framerate = 30, path = preview_path)
                # while True:
                #     frame_report = videothread.read()
                #     cv2.imshow("Report Video", frame_report)
                # cv2.destroyAllWindows()
                # videothread.stop()
            else:
                print("Video may have been deleted or renamed\n")
                values['-LIST-']
                
                
    def makeListBoxArray(arrayOfIncidents):  #returns array of strings that will be shown
        arr = []  #array that will be returned
        for i in range(0, len(arrayOfIncidents)):
            str = arrayOfIncidents[i]['timeOccured'] + ' ' + arrayOfIncidents[i]['incidentType']
            arr.append(str)
        return arr

    def set_preview_path(video_out_path):
        preview_path = video_out_path

