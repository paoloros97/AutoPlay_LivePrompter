# @Author: Paolo Rosettani
# @Date: 24/05/2021 (DD/MM/YYY)
#
# @Description:
# This code receives any kind of message from an external MIDI device (like a Cymatic)
# then forward the received MIDI message to a loopMIDI channel followed by an additional
# MIDI command that trigger the play button on "LivePrompter".
#
# To build the .exe run: 
# pyinstaller --clean --onefile --icon monkey.ico .\AutoPlayer.py

import mido # MIDI library
import mido.backends.rtmidi # Necessary for build the .exe
import time
import configparser
import sys

config = configparser.ConfigParser()
config.read('autoplayer.ini')

outputMIDIport = config['DEFAULT']['midi_out'] #To LivePrompter
inputMIDIport = config['DEFAULT']['midi_in'] #From Cymatic
inputChannel = int(config['DEFAULT']['ch_in']) #Listening MIDI channel

print("AutoPlayer for LivePrompter by PaoloRos. v2")

try:
    print('OUT > Opening output midi port: ' + str(outputMIDIport) + '...', end = ' ')
    outport = mido.open_output(outputMIDIport, autoreset=True) # Open output MIDI port
    print('OK - Output is connected!')
except:
    print("FAILED.")
    print('OUTPUT(s) available:\t', mido.get_output_names())
    print()
    print('SOLUTION: Run the loopMIDI software with a loop channel named: loopMIDI')
    input('Close this window or press Enter to exit.')
    sys.exit(1)


while ('inport' in locals()) == False: # Check if input port is open
    try:
        print('IN > Opening attempt for input: ' + str(inputMIDIport) + '...', end = ' ')
        inport = mido.open_input(inputMIDIport, autoreset=True) # Open input MIDI port
        
        print('OK - Input is connected!')
        print()
        print('- MIDI input:\t', inport.name, '(Channel ' + str(inputChannel) + ')')
        print('- MIDI output:\t', outport.name, '(Channel ' + str(inputChannel) + ')')

        alertMsg = "Connesso a MIDI-USB via AutoPlayer" # Alert text for Live Prompter
        sysex = mido.Message('sysex', data=[125, 77, 65, 1, 70, 71] + [ord(x) for x in list(alertMsg)] + [33]) # Compose MIDI alert
        outport.send(sysex) # Send MIDI alert

        print('- Lyrics change MIDI command: \tprogram_change (Channel ' + str(inputChannel) + ')')

        play = mido.Message('control_change', channel=inputChannel, control=7, value=10) # Compose MIDI Play command for LP
        print('- Play trigger MIDI command: \tcontrol_change (Channel ' + str(inputChannel) + ')')

        print()
        print('>>> Waiting for MIDI message...')

        while True:
            msg = inport.receive() # Read MIDI message received from Cymatic
            local_time = time.ctime(time.time()) # Timestamp
            if msg.type == 'program_change' and msg.channel == inputChannel: # Accept only program_change on channel 0
                outport.send(msg) # Forward message to Live Prompter
                time.sleep(0.001) # LivePrompter needs time to load the song
                outport.send(play) # Send Play message to Live Prompter
                print(msg, ' + Play cmd \t@', local_time)
            else:
                print(msg, '\t\t@', local_time) # Other messages (not program_change)

    except:
        print("FAILED. New attempt in 10 seconds >>>")
        print('INPUT(s) available:\t', mido.get_input_names())
        time.sleep(10)