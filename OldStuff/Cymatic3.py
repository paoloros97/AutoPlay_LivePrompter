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
    
    input("Press Enter to start.")

    for x in range(15):
        for c in range (15):
            prgChange = mido.Message('program_change', program=x, channel=c)
            print(prgChange)
            outport.send(prgChange)

    noteOn = mido.Message('note_on')
    print(noteOn)
    outport.send(noteOn) 

    