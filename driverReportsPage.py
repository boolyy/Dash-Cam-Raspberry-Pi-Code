import PySimpleGUI as sg

class DriverReportsPage:
    def openDriverReportsPage(homePageWindow):
        print("Clicked View Driver Reports")
        #driverReportPage_active = True
        driverReportLayout = [[sg.Button('Ok')], 
                    [sg.Button('Back')]]

        driverReportsPageWindow = sg.Window('Driver Reports', driverReportLayout, no_titlebar=False, location=(0,0), size = (800,480), finalize = True) #set no_titlebar to true later
        driverReportsPageWindow.Maximize()
        
        while True:
            event1, values1 = driverReportsPageWindow.read()
            if event1 == sg.WIN_CLOSED or event1 == 'Back':
                driverReportPage_active = False
                homePageWindow.UnHide()
                driverReportsPageWindow.Close()
                break
            if event1 == 'Ok':
                print("Ok button pressed")
