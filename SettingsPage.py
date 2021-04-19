import PySimpleGUI as sg
import theme

from JsonFiles.JsonFuncs import JsonFuncs
from Sounds.SoundFuncs import SoundFuncs

class SettingsPage:
    def openSettingsPage(user):

        sg.theme(theme.names[theme.index])
        
        checkboxLayout = [
            [sg.Text(text='', size = (10, 8))],
            [sg.Checkbox(text='Collision Detection', 
                                            default= user['collisionDetectionToggle'],
                                            key='-COLLISION DETECTION-', enable_events= True, font=['Lucida', 27])], 
                                [sg.Checkbox(text= 'Voice Alerts', default= user['voiceToggle'],
                                            key = '-VOICE TOGGLE-', enable_events= True, font=['Lucida', 27])]]
        #toggleLayout = [[sg.Button('Change Theme', font=['Lucida', 16], key = '-THEME TOGGLE-')]]
        buttonLayout = [[sg.Button('OK', font=['Lucida', 16])]]
        '''[sg.Button('Change Theme', font=['Lucida', 16], key = '-THEME TOGGLE-')],
                        [sg.Text(text='', size = (10, 1))],'''
        '''
        settingsPageLayout = [[sg.Checkbox(text='Collision Detection', 
                                            default= user['collisionDetectionToggle'],
                                            key='-COLLISION DETECTION-', enable_events= True)], 
                                [sg.Checkbox(text= 'Voice Alerts', default= user['voiceToggle'],
                                            key = '-VOICE TOGGLE-', enable_events= True)],
                                [sg.Button('OK')]]'''
        settingsPageLayout = [
            [sg.Column(checkboxLayout, vertical_alignment='center', justification='center')],
            [sg.Column(buttonLayout, vertical_alignment='center', justification='center')]
            ]
        
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
            '''
            if event == '-THEME TOGGLE-': #if user toggles the voice checkbox
                SoundFuncs.playSound('Sounds/menuButtonClick.mp3')
                theme.index = (theme.index+1) % len(theme.names)
                sg.theme(theme.names[theme.index]) #changes theme
                settingsPageWindow.redraw()'''
            


        
