#
# @Author: Paolo Rosettani
# @Date: 24/05/2021 (DD/MM/YYY)
# @Description:
# This code is for only testing purpose.
# Emulates an external device connected via MIDI-usb port.
#

import mido
import numpy as np 

outport = mido.open_output('MIDImsg 3')

type = [83, 72, 84, 70] # 0 Show, 1 Hide, 2 Toggle, 3 Flash
color = [66, 71, 82, 89, 79, 80, 69, 87, 75] #0 Blue, 1 Green, 2 Red, 3 Yellow, 4 Orange, 5 Purple, 6 Grey, 7 White, 8 Black 

messageHide = [125, 77, 65, 1, type[1]] + [33] # Append header and tale
sysexHide = mido.Message('sysex', data = messageHide) #Compose MIDI message

#alertMsg = "Connesso a MIDI-USB via AutoPlayer" # Alert text
#sysex = mido.Message('sysex', data=[125, 77, 65, 1, 70, 71] + [ord(x) for x in list(alertMsg)] + [33]) # Compose MIDI alert
while True:
    print("Insert message:", end=" ")
    messageIn = input()
    messageInData = [125, 77, 65, 1, type[3], color[4]] + [ord(x) for x in list(messageIn)] + [33]
    sysexIn = mido.Message('sysex', data = messageInData) #Compose MIDI message
    outport.send(sysexIn)

    input("Enter to hide message.")
    outport.send(sysexHide)