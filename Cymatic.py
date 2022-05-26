#
# @Author: Paolo Rosettani
# @Date: 24/05/2021 (DD/MM/YYY)
# @Description:
# This code is for only testing purpose.
# Emulates an external device connected via MIDI-usb port.
#

import mido
import numpy as np 

outport = mido.open_output('emulatore 2')

prgChange = mido.Message('program_change', program=1, channel=0) #Change Program here
noteOn = mido.Message('note_on', note=60)
noteOff = mido.Message('note_off', note=60)

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
    input("Press Enter to continue.")
    send = prgChange
    print(send)
    outport.send(send)
    input("Press Enter to continue.")
    send = noteOn
    print(send)
    outport.send(send)
    input("Press Enter to continue.")
    prgChange1 = mido.Message('program_change', program=1, channel=1) #Change Program here
    print(prgChange1)
    outport.send(prgChange1)
    input("Press Enter to continue.")
    send = sysex
    print(send)
    outport.send(send)

#Test
#hex_array = [0x7D, 0x4D, 0x41, 0x01, 0x53, 0x52, 0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x20, 0x57, 0x6F, 0x72, 0x6C, 0x64, 0x21]
#dec_array = [125, 77, 65, 1, 83, 82, 72, 101, 108, 108, 111, 32, 87, 111, 114, 108, 100, 33]
#dec_array = [int(x) for x in hex_array]

