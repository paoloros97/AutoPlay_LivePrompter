import mido # MIDI library
import mido.backends.rtmidi # Necessary for build the .exe
import time
import configparser


config = configparser.ConfigParser()
config.read('autoplayer.ini')

outputMIDIport = config['DEFAULT']['midi_out'] #To LivePrompter
inputMIDIport = config['DEFAULT']['midi_in'] #From Cymatic
inputChannel = int(config['DEFAULT']['ch_in']) #Listening MIDI channel

outport = mido.open_output(outputMIDIport, autoreset=True) # Open output MIDI port

while ('inport' in locals()) == False:
    print("è chiusa")
    time.sleep(5)
    try:
        print("Provo ad aprirla")
        inport = mido.open_input(inputMIDIport, autoreset=True) # Open input MIDI port
        print("Aperta!!!!!!!!! :)")

        while True:
            time.sleep(2)
            print("programma")
    except:
        print("Aspetto")




"""
while True:
    if inport.closed == True

    try:
        i = int(input('Select: '))
        if i in range(4):
            print("bella")
            break
    except:    
        pass

    print ('\nIncorrect input, try again')

"""