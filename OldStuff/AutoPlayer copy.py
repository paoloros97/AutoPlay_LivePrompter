#
# @Author: Paolo Rosettani
# @Date: 24/05/2021 (DD/MM/YYY)
#
# @Description:
# This code receive any kind of message received from an external MIDI device (like a Cymatic)
# Forward the received MIDI message to a loopMIDI channel with an addition MIDI command that trigger
# the play button on "LivePrompter".
#
#For build .exe Run: pyinstaller --onefile --icon ananas.ico .\AutoPlayer.py
#--onefile --windowed --icon=app.ico app.py
#Colors: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
#Version 2

import mido # MIDI library
import mido.backends.rtmidi # Necessary for build the .exe
import time

outputMIDIport='loopMIDI 1' #To LivePrompter
inputMIDIport='emulatore 1' #From Cymatic
inputChannel = 0

try:
    outport = mido.open_output(outputMIDIport, autoreset=True) # Open output MIDI port
    inport = mido.open_input(inputMIDIport, autoreset=True) # Open input MIDI port

    print('\x1b[6;30;42m' + 'Connected' + '\x1b[0m', 'to physical MIDI in-port:', inport.name, 'and virtual MIDI out-port:', outport.name + '.')

    # Send the "connected Alert" to Live Prompter
    alert = "Connesso a MIDI-USB (Porta 1) via AutoPlayer" # Alert to send
    sysex = mido.Message('sysex', data=[125, 77, 65, 1, 70, 71] + [ord(x) for x in list(alert)] + [33]) # Compose MIDI alert
    outport.send(sysex) # Send MIDI alert

    play = mido.Message('control_change', control=7, value=10) # Compose MIDI Play command

    print('\x1b[3;36;40m' + 'Remember: here numbers goes from 0 to 15 instead of 1 to 16.' + '\x1b[0m') #32
    print('\x1b[1;35;40m' + 'The Play command is:'+ '\x1b[0m', play)
    print()
    print('>>> Waiting MIDI message from Cymatic... (Obey only to program_change on Channel '+ str(inputChannel) + ')')
    
    t = time.time()
    while True:
        msg = inport.receive() # Read MIDI message received from Cymatic
        
        epoch = time.time() # Get time in Unix epoch
        local_time = time.ctime(epoch) # Convert time to standard format

        if msg.type == 'program_change' and msg.channel == inputChannel: # Accept only program_change
            outport.send(msg) # Forward message to Live Prompter
            time.sleep(0.1) # LivePrompter needs time to load the song
            outport.send(play) # Send Play message to Live Prompter
            #print('\x1b[1;32;40m', msg, '\x1b[0m' + '\x1b[1;35;40m' + ' + Play cmd '+ '\x1b[0m' , '\t@', local_time)
                        
        #else:
            #print('\x1b[1;33;40m', msg, '\x1b[0m' + '\t\t\t@', local_time)
        


except:
    
    print('\x1b[6;30;41m' + 'ERROR: Unable to open MIDI port(s)!' + '\x1b[0m')
    print('\x1b[6;30;43m' + 'MIDI ports available:' + '\x1b[0m')
    print('INPUT:\t', mido.get_input_names())
    print('OUTPUT:\t', mido.get_output_names())
    print('Note: take the physical MIDI port as Input.')

    print()
    input('Close this window or ' + '\x1b[6;30;47m' + 'press Enter to Exit' + '\x1b[0m' + '.')