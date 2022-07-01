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

#Sysex
message = "Connesso a Miditech-USB: Porta 1 (MIDIPRT: 8x8)" #Message to send

messageNum = 1
type = [83, 72, 84, 70] # 0 Show, 1 Hide, 2 Toggle, 3 Flash
color = [66, 71, 82, 89, 79, 80, 69, 87, 75] #0 Blue, 1 Green, 2 Red, 3 Yellow, 4 Orange, 5 Purple, 6 Grey, 7 White, 8 Black 

messageArr = list(message) #Convert message string to char array
messageArr_dec = [ord(x) for x in messageArr] #Convert ASCII array to decimal
messageData = [125, 77, 65, messageNum, type[3], color[1]] + messageArr_dec + [33] # Append header and tale
#print(messageData)
sysex = mido.Message('sysex', data=messageData) #Compose MIDI message

while True:
    
    print("To send sysex", end=" ")
    input("press Enter.")
    alertMsg = "Connesso a MIDI-USB via AutoPlayer" # Alert text
    sysex = mido.Message('sysex', data=[125, 77, 65, 1, 70, 71] + [ord(x) for x in list(alertMsg)] + [33]) # Compose MIDI alert
    
    print(sysex)
    outport.send(sysex)