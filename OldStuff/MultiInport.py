import mido
#from mido.ports import multi_receive

inputMIDIport='emulatore 1'
MsgInputMIDIport='MIDImsg 2'

# Open all available inputs.
ports = [mido.open_input(inputMIDIport), mido.open_input(MsgInputMIDIport)]

for port in ports:
    print('Using {}'.format(port))
print('Waiting for messages...')

try:
    for message in mido.ports.multi_receive(ports):
        print('Received:', message)
except KeyboardInterrupt:
    pass