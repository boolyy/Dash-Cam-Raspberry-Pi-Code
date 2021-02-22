import PySimpleGUI as sg
import pygame


class RecordingPage:
    def openRecordingPage(homePageWindow, user):
        recordingPageLayout = [[sg.Button('Stop Recording')]]

        recordingPageWindow = sg.Window('Recording',
                                        recordingPageLayout,
                                        no_titlebar=False,
                                        location=(0, 0),
                                        size=(800, 480),
                                        finalize=True)
        recordingPageWindow.Maximize()

        while True:
            event, values = recordingPageWindow.read()
            if event == sg.WINDOW_CLOSED or event == 'Stop Recording':
                homePageWindow.UnHide()
                recordingPageWindow.Close()
