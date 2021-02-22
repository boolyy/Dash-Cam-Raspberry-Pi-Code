import json
import os
from os import path

#NEED TO WRITE writeUserData Function


class LoadUserData:
    def loadUserData():
        if (
                not path.exists('Pages/JsonFiles/user.txt')
        ):  #if file does not exist create user object and write it to a json file
            user = {  #create dict
                'aveScore': 0,  #aveScore
                'driverReports':
                [],  #array of driverReports that will be filled dataReport objects
                'voiceToggle':
                True,  #if true, then user will hear voice telling them what they did wrong
                'collisionDetectionToggle':
                True,  #if true, then user will hear beeping sound for collision detection
                'numOfDriverReports': 0,  #used for calculating averages
                'dateCreated': ''  #date that user's account got reacted
            }

            with open('Pages/JsonFiles/user.txt',
                      'w') as outfile:  #creates txt file with json info
                json.dump(user, outfile,
                          indent=4)  #indent param used to format json file
        else:  #load data into user object from json file
            with open('Pages/JsonFiles/user.txt') as jsonFile:
                user = json.load(jsonFile)

        return user

    def writeUserData():  #writes user object info to JSON file
        return
