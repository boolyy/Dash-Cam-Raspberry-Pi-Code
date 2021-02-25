import PySimpleGUI as sg

from JsonFiles.JsonFuncs import JsonFuncs
from Sounds.SoundFuncs import SoundFuncs


class SettingsPage:
    def openSettingsPage(user):
        
        settingsPageLayout = [[sg.Checkbox(text='Collision Detection', 
                                            default= user['collisionDetectionToggle'],
                                            key='-COLLISION DETECTION-', enable_events= True)], 
                                [sg.Checkbox(text= 'Voice Alerts', default= user['voiceToggle'],
                                            key = '-VOICE TOGGLE-', enable_events= True)],
                                [sg.Button('OK')]]

        settingsPageWindow = sg.Window('Settings', settingsPageLayout,
                                        no_titlebar= False, location=(0,0),
                                        size=(800, 480), finalize= True)

        while True:
            event, values = settingsPageWindow.read()
            if event == sg.WINDOW_CLOSED or event == 'OK': #if window is closed or if user clickes OK button
                SoundFuncs.playSound('Sounds/menuButtonClick.mp3')
                JsonFuncs.writeUserData(user) #write updated user data to json
                settingsPageWindow.Close()
                return user
                break

            if event == '-VOICE TOGGLE-': #if user toggles the voice checkbox
                SoundFuncs.playSound('Sounds/menuButtonClick.mp3')
                user['voiceToggle'] = not user['voiceToggle'] #changes preference in user object
            
            if event == '-COLLISION DETECTION-': #if user toggles the collision detection checkbox
                SoundFuncs.playSound('Sounds/menuButtonClick.mp3')
                user['collisionDetectionToggle'] = not user['collisionDetectionToggle'] #changes preference in user object
            

            


        