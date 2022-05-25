#
# @Author: Paolo Rosettani
# @Date: 24/05/2021 (DD/MM/YYY)
# @Description:
# This code receive any kind of message received from an external MIDI device (like a Cymatic)
# Forward the received MIDI message to a loopMIDI channel with an addition MIDI command that trigger
# the play button on "LivePrompter".
#
# In this way it keep simple the MIDI programing for the Cymatic, it just trigger a Program Change
# matched with a ceratin song (in LivePrompter), and ti peace of code include the play command (send by
# a MIDI Control Change).
#

import mido
import mido.backends.rtmidi
import os
import time
import sys

outputMIDI='loopMIDI 1' #To LivePrompter
inputMIDI='emulatore 1' #From Cymatic
try:
    outport = mido.open_output(outputMIDI, autoreset=True) #Oper output MIDI port
    inport = mido.open_input(inputMIDI, autoreset=True) #Open input MIDI port



    print('Waiting MIDI message from Cymatic...')
    print()
    msg = inport.receive() # Leggo il messagio dal Cymatic

    if msg.type == 'program_change':
        print('Forward:')
        print(msg) # Visualizzo il messaggio ricevuto
        outport.send(msg) # Inoltro il messaggio a Live Prompter

        # Play MIDI command
        print('Play command:')
        play = mido.Message('control_change', control=7, value=10) #Play
        print(play)
        outport.send(play)

    else:
        print('MIDI message Discarded: not a control_change!')

    print() #New line

    time.sleep(1)
    
    os.execl(sys.executable, 'python', __file__, *sys.argv[1:]) #Restart program

except:
    print('Unable to open MIDI port(s).')
    print('Is the loopMIDI program running?')
    print('Is the MIDI-usb adapter connected?')
    print('Window closing in 10 seconds...')
    time.sleep(10)