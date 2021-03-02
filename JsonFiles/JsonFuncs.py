import json
import os
from os import path
from datetime import date
from Objects.User import User
#NEED TO WRITE writeUserData Function


class JsonFuncs:
    def loadUserData():
        if (
                not path.exists('JsonFiles/user.txt')
        ):  #if file does not exist create user object and write it to a json file
            today = date.today()
            # Below Code is for writing user as 
            #user = {  #create dict
            #    'aveScore': 100,  #aveScore
            #    'driverReports':
            #    [],  #array of driverReports that will be filled dataReport objects
            #    'voiceToggle':
            #    True,  #if true, then user will hear voice telling them what they did wrong
            #    'collisionDetectionToggle':
            #    True,  #if true, then user will hear beeping sound for collision detection
            #    'numOfDriverReports': 0,  #used for calculating averages
            #    'dateCreated': today.strftime(
            #        "%m/%d/%Y")  #date that user's account got creacted
            #}

            user = User() #create user object
            

            with open('JsonFiles/user.txt', 'w') as outfile:  #creates txt file with json info
                json.dump(user.__dict__, outfile, indent=4) #write user object as dictionary
        else:  #load data into user object from json file
            with open('JsonFiles/user.txt') as jsonFile:
                user = json.load(jsonFile)

        return user

    def writeUserData(user):  #writes user object info to JSON file
        with open('JsonFiles/user.txt', 'w') as outfile:
            json.dump(user, outfile, indent=4)
