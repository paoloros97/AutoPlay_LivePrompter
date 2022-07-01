#
# @Author: Paolo Rosettani
# @Date: 01/07/2021 (DD/MM/YYY)
# @Description:
#

import mido
import PySimpleGUI as sg

outMIDIport = 'MIDImsg 3' # Write the midi output port name here

# Define the window's contents
layout = [[sg.Button('Check connection'), sg.Text(size=(40,1), key='-PORT-')],
          [sg.Text("Message: ")],
          [sg.Input(key='-INPUT-'), sg.Button('Flash'), sg.Button('Show'), sg.Button('Hide'),],
          [sg.Button('Quit')]]

outport = mido.open_output(outMIDIport) #Open MIDI outport

type = [83, 72, 84, 70] # 0 Show, 1 Hide, 2 Toggle, 3 Flash
color = [66, 71, 82, 89, 79, 80, 69, 87, 75] #0 Blue, 1 Green, 2 Red, 3 Yellow, 4 Orange, 5 Purple, 6 Grey, 7 White, 8 Black 

messageHide = [125, 77, 65, 1, type[1]] + [33] # Append header and tale
sysexHide = mido.Message('sysex', data = messageHide) #Compose MIDI message

#alertMsg = "Connesso a MIDI-USB via AutoPlayer" # Alert text
#sysex = mido.Message('sysex', data=[125, 77, 65, 1, 70, 71] + [ord(x) for x in list(alertMsg)] + [33]) # Compose MIDI alert
#while True:
# Create the window
window = sg.Window('Messenger MIDI', layout)



# Display and interact with the Window using an Event Loop
while True:

    event, values = window.read()

    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    elif event == 'Flash':
        print("Premuto Flash")

    # Output a message to the window
    window['-PORT-'].update('Connected to Output Port: ' + str(outMIDIport))

# Finish up by removing from the screen
window.close()

"""
print("Insert message:", end=" ")
messageIn = input()
messageInData = [125, 77, 65, 1, type[3], color[4]] + [ord(x) for x in list(messageIn)] + [33]
sysexIn = mido.Message('sysex', data = messageInData) #Compose MIDI message
outport.send(sysexIn)

input("Enter to hide message.")
outport.send(sysexHide)
"""








