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
import time

outputMIDIport='loopMIDI 1' #To LivePrompter
inputMIDIport='emulatore 1' #From Cymatic

try:
    outport = mido.open_output(outputMIDIport, autoreset=True) #Open output MIDI port
    inport = mido.open_input(inputMIDIport, autoreset=True) #Open input MIDI port

    # Connected Alert on Live Prompter
    message = "Connesso a MIDI-USB (Porta 1) via AutoPlayer" # Message to send
    messageArr = list(message) # Convert message string to char array
    messageArr_dec = [ord(x) for x in messageArr] # Convert ASCII array to decimal
    messageData = [125, 77, 65, 1, 70, 71] + messageArr_dec + [33] # Header and tail of the MIDI message
    sysex = mido.Message('sysex', data=messageData) # Compose MIDI message
    outport.send(sysex)

    play = mido.Message('control_change', control=7, value=10) # Compose MIDI Play command

    while True:
        print('Waiting MIDI message from Cymatic...')
        msg = inport.receive() # Read MIDI message received from Cymatic
        
        epoch = time.time() # Get time in Unix epoch
        local_time = time.ctime(epoch) # Convert time to standard format
        print("Received @",local_time) # Timestamp

        if msg.type == 'program_change': # Accept only program_change
            outport.send(msg) # Forward message to Live Prompter
            time.sleep(0.1) # LivePrompter needs time to load the song
            outport.send(play) # Send Play message to Live Prompter

            print('Forward:', end ="\t")
            print(msg) # Print received message
            
            print('Play command:', end ="\t")
            print(play) # Print Play message
            
        else:
            print('DISCARDED: MIDI message not a control_change!')

        print()

except:
    print('ERROR: Unable to open MIDI port(s).')
    print('Solutions:')
    print('\tIs the \"loopMIDI\" program running?')
    print('\tIs the MIDI-usb adapter connected?')
    print()
    print('Window closing in 10 seconds...')
    time.sleep(10)