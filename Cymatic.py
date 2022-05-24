#
# @Author: Paolo Rosettani
# @Date: 24/05/2021 (DD/MM/YYY)
# @Description:
# This code is for only testing purpose.
# Emulates an external device connected via MIDI-usb port.
#

import mido

outport = mido.open_output('emulatore 2')
songCymatic = mido.Message('program_change', program=1) #Change Program here

print(songCymatic)
outport.send(songCymatic)