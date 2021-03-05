#MAY OR MAY NOT USE THIS OBJECT
from datetime import date

class User:
    def __init__(self):
        self.aveScore = 100
        self.driverReports = [] #arr of driver Report objects
        self.voiceToggle = True
        self.collisionDetectionToggle = True
        self.numOfDriverReports = 0
        self.dataCreated = date.today().strftime('%m/%d/%Y')
    #make function that will recalculate average
    def calcAveScore(user):
        total = 0
        for i in range(0, len(user['driverReports'])):
            total += user['driverReports'][i]['score']
        return (total/user['numOfDriverReports'])