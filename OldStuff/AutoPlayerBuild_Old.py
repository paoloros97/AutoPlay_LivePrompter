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

import mido
import mido.backends.rtmidi # Necessary for build the exe version
import os
import time
import sys

outputMIDIport='loopMIDI 1' #To LivePrompter
inputMIDIport='emulatore 1' #From Cymatic

try:
    outport = mido.open_output(outputMIDIport, autoreset=True) #Open output MIDI port
    inport = mido.open_input(inputMIDIport, autoreset=True) #Open input MIDI port

    print('Waiting MIDI message from Cymatic...')
    #print()

    msg = inport.receive() # Read MIDI message received from Cymatic
    play = mido.Message('control_change', control=7, value=10) # MIDI Play command

    epoch = time.time() # Get time in Unix epoch
    local_time = time.ctime(epoch) #Convert time to standard format

    if msg.type == 'program_change': # Accept only program_change
        outport.send(msg) # Forward message to Live Prompter
        time.sleep(0.1) # LivePrompter needs time to load the song
        outport.send(play) # Send Play message to Live Prompter

        print(local_time)
        print('Forward:', end ="\t")
        print(msg) # Print received message
        
        print('Play command:', end ="\t")
        
        print(play) # Print Play message
        
    else:

        print('MIDI message Discarded: not a control_change!')

    print() # New line

    time.sleep(1) # Wait 1 sec before restart
    os.execl(sys.executable, 'python', __file__, *sys.argv[1:]) # Restart program

except:
    print('ERROR: Unable to open MIDI port(s).')
    print('Solutions:')
    print('\tIs the \"loopMIDI\" program running?')
    print('\tIs the MIDI-usb adapter connected?')
    print()
    print('Window closing in 10 seconds...')
    time.sleep(10)