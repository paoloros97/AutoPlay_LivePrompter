#
# @Author: Paolo Rosettani
# @Date: 24/05/2021 (DD/MM/YYY)
#
# @Description:
# This code receive any kind of message received from an external MIDI device (like a Cymatic)
# Forward the received MIDI message to a loopMIDI channel with an addition MIDI command that trigger
# the play button on "LivePrompter".
#
# In this way it keep simple the MIDI programing for the Cymatic, it just trigger a Program Change
# matched with a ceratin song (in LivePrompter), and ti peace of code include the play command (send by
# a MIDI Control Change).
#
#For build .exe Run: pyinstaller --onefile .\AutoPlayerBuild.py

# Version 2

import mido # MIDI library
import mido.backends.rtmidi # Necessary for build the .exe
import time

outputMIDIport='loopMIDI 1' #To LivePrompter
inputMIDIport='emulatore 1' #From Cymatic
inputChannel = 0

try:
    outport = mido.open_output(outputMIDIport, autoreset=True) # Open output MIDI port
    inport = mido.open_input(inputMIDIport, autoreset=True) # Open input MIDI port

    # Connected Alert to Live Prompter
    alert = "Connesso a MIDI-USB (Porta 1) via AutoPlayer" # Alert to send
    sysex = mido.Message('sysex', data=[125, 77, 65, 1, 70, 71] + [ord(x) for x in list(alert)] + [33]) # Compose MIDI alert
    outport.send(sysex)

    play = mido.Message('control_change', control=7, value=10) # Compose MIDI Play command

    print('>>> Waiting MIDI message from Cymatic... ( Only program_change on Channel', inputChannel,')')

    while True:
        msg = inport.receive() # Read MIDI message received from Cymatic
        
        epoch = time.time() # Get time in Unix epoch
        local_time = time.ctime(epoch) # Convert time to standard format

        if msg.type == 'program_change' and msg.channel == inputChannel: # Accept only program_change
            outport.send(msg) # Forward message to Live Prompter
            time.sleep(0.1) # LivePrompter needs time to load the song
            outport.send(play) # Send Play message to Live Prompter

            print('Forward:\t', msg, " with Play command \t@", local_time)
                        
        else:
            print('DISCARDED:\t', msg, " \t\t@", local_time)

except:
    print('ERROR: Unable to open MIDI port(s).')
    print('Solutions:')
    print('\tIs the \"loopMIDI\" program running?')
    print('\tIs the MIDI-usb adapter connected?')
    print()
    print('Window closing in 10 seconds...')
    time.sleep(10)