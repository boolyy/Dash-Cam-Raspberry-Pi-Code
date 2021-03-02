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

    