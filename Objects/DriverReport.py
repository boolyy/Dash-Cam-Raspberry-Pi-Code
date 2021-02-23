class DriverReport:
    def __init__(self, score, date, startTime, endTime, arrayOfIncidents):
        self.score = score
        self.date = date
        self.startTime = startTime
        self.endTime = endTime
        self.arrayOfIncidents = arrayOfIncidents #will contain array of incident objects