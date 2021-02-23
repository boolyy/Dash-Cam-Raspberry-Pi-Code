import PySimpleGUI as sg
from VoiceAlerts.VoiceFuncs import VoiceFuncs
from JsonFiles.JsonFuncs import JsonFuncs


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
                VoiceFuncs.playSound('VoiceAlerts/menuButtonClick.mp3')
                JsonFuncs.writeUserData(user) #write updated user data to json
                settingsPageWindow.Close()
                return user
                break

            if event == '-VOICE TOGGLE-': #if user toggles the voice checkbox
                VoiceFuncs.playSound('VoiceAlerts/menuButtonClick.mp3')
                user['voiceToggle'] = not user['voiceToggle']
            
            if event == '-COLLISION DETECTION-':
                VoiceFuncs.playSound('VoiceAlerts/menuButtonClick.mp3')
                user['collisionDetectionToggle'] = not user['collisionDetectionToggle']
            

            


        