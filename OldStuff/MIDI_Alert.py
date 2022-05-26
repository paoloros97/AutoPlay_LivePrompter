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
    #inport = mido.open_input('emulator', virtual=True)
    
    while True:
        print('Waiting MIDI message from Cymatic...')
        #print()
    
        msg = inport.receive() # Read MIDI message received from Cymatic
        epoch = time.time() # Get time in Unix epoch
        local_time = time.ctime(epoch) #Convert time to standard format
        
        
        print('Received:', end ="\t")
        print(msg, end ="\t @") # Print received message
        print(local_time)
        sys.stdout.flush()
        print() # New line
        outport.send(msg)
        
        time.sleep(0.1) # Wait 1 sec before restart
        #os.execl(sys.executable, 'python', __file__, *sys.argv[1:]) # Restart program

except:
    print('ERROR: Unable to open MIDI port(s).')
    print('Solutions:')
    print('\tIs the MIDI-usb adapter connected?')
    print()
    print('Window closing in 10 seconds...')
    time.sleep(10)