import json
import os
from os import path

class JsonStuff:
    def loadUserData():
        if(not path.exists('JsonFiles/user.txt')): #if file does not exist create user object and write it to a json file
            user = { #create dict
                'aveScore' : 0, #aveScore
                'driverReports' : [], #array of driverReports that will be filled dataReport objects
                'voiceToggle' : True, #if true, then user will hear voice telling them what they did wrong
                'collisionDetectionToggle' : True, #if true, then user will hear beeping sound for collision detection
                'numOfDriverReports' : 0, #used for calculating averages
            }

            with open('JsonFiles/user.txt', 'w') as outfile: #creates txt file with json info
                json.dump(user, outfile, indent=4) #indent param used to format json file
        else: #load data into user object from json file
            with open('JsonFiles/user.txt') as jsonFile:
                user = json.load(jsonFile)
            print(user)

def main():
    #Check if user has generated a json file already
    #if user is starting the app for the first time, then they will have no json file with info
    JsonStuff.loadUserData()


if __name__ == "__main__":
    main()