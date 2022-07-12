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

    print('CONNECTED - OK')
    print()
    print('- MIDI input:\t', inport.name, '(Channel ' + str(inputChannel) + ') # Remember to add 1 (i.e. Ch 0 is 1, Ch 2 is 3... )')
    print('- MIDI output:\t', outport.name, '(Channel ' + str(inputChannel) + ')')

    alertMsg = "Connesso a MIDI-USB via AutoPlayer" # Alert text for Live Prompter
    sysex = mido.Message('sysex', data=[125, 77, 65, 1, 70, 71] + [ord(x) for x in list(alertMsg)] + [33]) # Compose MIDI alert
    outport.send(sysex) # Send MIDI alert

    print('- Lyrics change MIDI command: \tprogram_change (Channel ' + str(inputChannel) + ')')

    play = mido.Message('control_change', channel=inputChannel, control=7, value=10) # Compose MIDI Play command for LP
    print('- Play trigger MIDI command: \tcontrol_change (Channel ' + str(inputChannel) + ')')

    print()
    print('>>> Waiting for MIDI message from Cymatic...')

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
    print('ERROR!')
    print()
    print('Unable to open MIDI port(s)!')
    print()
    print('MIDI ports available:')
    print('INPUT(s):\t', mido.get_input_names())
    print('OUTPUT(s):\t', mido.get_output_names())
    print()
    input('Close this window or press Enter to Exit.')