import time
from datetime import date

import pygame


class Incident:
    
    def __init__(self, date, timeOccured, incidentType, incidentValue):
        self.timeOccured = timeOccured  #time that incident happened
        self.date = date
        self.incidentType = incidentType
        self.incidentValue = incidentValue #may have to make dictionary with incident values
        self.videoTitle = Incident.makeVideoTitle(date, timeOccured, incidentType)  #string that will contain directory that video is in folder
    
    def makeVideoTitle(date, timeOccured, incidentType):
        str = date + ' ' + incidentType + ' ' + timeOccured
        return str

    dict = { #dictionary of incidents that contain incident Value as well as path to voice alert
        'ranOverPedestrian' : [100, "Sounds/VoiceAlerts/ranOverPedestrian.mp3",
                                'Ran over a pedestrian'],
        'ranStopSign' : [20, "Sounds/VoiceAlerts/ranStopSign.mp3",
                                'Ran a stop sign']
    }

    def incidentHappened(user, driverReport, incident): #string of incident gets passed into function
        if(user['voiceToggle'] == True): #play voice alert if user has toggled voice alerts
            Incident.playSound(Incident.dict[incident][1])
        today = date.today()
        incidentObj = Incident(today.strftime("%m/%d/%Y"), time.strftime('%H:%M'),
                            Incident.dict[incident][2], Incident.dict[incident][0])
        driverReport.score -= incidentObj.incidentValue
        driverReport.arrayOfIncidents.append(incidentObj.__dict__)
        return
    
    def playSound(path):
        pygame.mixer.init()
        pygame.mixer.music.load(path) #loads sound from path given
        pygame.mixer.music.play() #plays sound


    

    