import mido
import mido.backends.rtmidi # Necessary for build the exe version
import os
import time
import sys

inputMIDIport='emulatore 1' #From Cymatic

try:
    inport = mido.open_input(inputMIDIport, autoreset=True) #Open input MIDI port
    print('Listener: Waiting for MIDI message...')

    while True:
        #print('Listener: Waiting MIDI message from Cymatic...')
        msg = inport.receive() # Read MIDI message received from Cymatic
        epoch = time.time() # Get time in Unix epoch
        local_time = time.ctime(epoch) #Convert time to standard format
        
        print('Received:', end ="\t")
        print(msg, end = "\t @") # Print received message
        print(local_time)
        #print() # New line

except:
    print('ERROR: Unable to open MIDI port(s).')
    print('Solutions:')
    print('\tIs the MIDI-usb adapter connected?')
    print()
    print('Window closing in 10 seconds...')
    time.sleep(10)