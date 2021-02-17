import PySimpleGUI as sg
from gpiozero import LED
#excercise to figure out PySimpleGUI

sg.theme('DarkAmber')   # Add a touch of color

#list all of the things that will be in window
layout = [[sg.Button('LED ON')],
            [sg.Button('LED OFF')]]
led = LED(14)
ledON = False
#create window
window = sg.Window('LED Toggler', layout)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window, turn led off
        led.off() 
        break
    if event == 'LED ON':
        led.on()
    if event == 'LED OFF':
        led.off()



window.close()

