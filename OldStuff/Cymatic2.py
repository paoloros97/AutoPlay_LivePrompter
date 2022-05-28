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

while True:
    
    print("To send note_on", end=" ")
    input("press Enter.")
    noteOn = mido.Message('note_on')
    print(noteOn)
    outport.send(noteOn)

    for x in range(20):
        RealNum = x+1
        print("To send program change", RealNum, end=" ")
        input("press Enter.")
        prgChange = mido.Message('program_change', program=x, channel=0)
        print(prgChange)
        outport.send(prgChange)