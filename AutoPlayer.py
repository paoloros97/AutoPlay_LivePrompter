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

config = configparser.ConfigParser()
config.read('autoplayer.ini')

outputMIDIport = config['DEFAULT']['midi_out'] #To LivePrompter
inputMIDIport = config['DEFAULT']['midi_in'] #From Cymatic
inputChannel = int(config['DEFAULT']['ch_in']) #Listening MIDI channel

try:
    outport = mido.open_output(outputMIDIport, autoreset=True) # Open output MIDI port
    inport = mido.open_input(inputMIDIport, autoreset=True) # Open input MIDI port
    print('Connected to physical MIDI in-port:', inport.name, 'and virtual MIDI out-port:', outport.name + '.')

    alertMsg = "Connesso a MIDI-USB via AutoPlayer" # Alert text
    sysex = mido.Message('sysex', data=[125, 77, 65, 1, 70, 71] + [ord(x) for x in list(alertMsg)] + [33]) # Compose MIDI alert
    outport.send(sysex) # Send MIDI alert

    print('Remember: here numbers goes from 0 to 15 instead of 1 to 16.')

    play = mido.Message('control_change', control=7, value=10) # Compose MIDI Play command for LP
    print('The Play command is:', play)
    
    print()
    print('>>> Waiting MIDI message from Cymatic... (Obey only to program_change on Channel ' + str(inputChannel) + ')')
    
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
    print('ERROR')
    print('Unable to open MIDI port(s)!')
    print()
    print('MIDI ports available:')
    print('INPUT:\t', mido.get_input_names())
    print('OUTPUT:\t', mido.get_output_names())
    print()
    input('Close this window or press Enter to Exit.')