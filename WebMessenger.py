import PySimpleGUIWeb as sg
import mido
import mido.backends.rtmidi # Necessary for build the .exe
import socket

addr = socket.getaddrinfo(socket.gethostname(), None)
print(addr)
print("Socket: 2222")

# Launch the following command to build the .exe version:
# pyinstaller --clean --noconsole --onefile .\Messenger.py

# Get the list of midi outports
PortList = mido.get_output_names() 
PortList = PortList[::-1] # reverse the list so the last one is first

# LED status attributes
CIRCLE = '🟢'
CIRCLE_OUTLINE = '⚪'

# Sysex attributes
type = [83, 72, 84, 70] # 0 Show, 1 Hide, 2 Toggle, 3 Flash
color = [66, 71, 82, 89, 79, 80, 69, 87, 75] #0 Blue, 1 Green, 2 Red, 3 Yellow, 4 Orange, 5 Purple, 6 Grey, 7 White, 8 Black 
colorName = ['Blue', 'Green', 'Red', 'Yellow', 'Orange', 'Purple', 'Grey', 'White', 'Black']
# Hide alert sysex definition 
messageHide = [125, 77, 65, 1, type[1]] + [33] # Append header and tale
sysexHide = mido.Message('sysex', data = messageHide) #Compose MIDI message


layout = [  [sg.Text('Select MIDI port')],
            [sg.Combo(values=PortList, default_value=(PortList[0]), key='device')], 
            [sg.Button('Connect', size=(9, 1), key='-B-'), sg.Text(key='statusLED'), sg.Text(key='portStatus')],
            
            [sg.Text('Send message')],
            [sg.Input(key='-in-')],
            [sg.Button('Flash'), sg.Button('Show'), sg.Button('Hide'),
             sg.Combo(values=colorName, default_value=(colorName[3]), size=(10, 1), key='-color-')]
         ]

window = sg.Window('LivePrompter Messenger MIDI', layout, web_port=2222, web_start_browser=False, disable_close=True)

down = True # Toggle MIDI port status (open or close)

while True:
    event, values = window.read()
    
    if event == '-B-':                # if the normal button that changes color and text
        down = not down
        if down:
            outport.close()
            window['portStatus'].update('Disconnected')
            window['statusLED'].update(CIRCLE_OUTLINE)
            #print("Disconnected")
        else:
            outMIDIport = values['device']
            outport = mido.open_output(outMIDIport) #Open MIDI outport
            window['portStatus'].update('Connected to: ' + str(outMIDIport))
            window['statusLED'].update(CIRCLE)
            #print('Connected to Midi outport: ' + str(outMIDIport))
        
        window['-B-'].update(text='Connect' if down else 'Disconnect')

    elif event == 'Flash' and down == False: 
        if values['-in-'] != '':
            messageIn = values['-in-'] #Read the text
            messageInData = [125, 77, 65, 1, type[3], color[colorName.index(values['-color-'])]] + [ord(x) for x in list(messageIn)] + [33]
            sysexIn = mido.Message('sysex', data = messageInData) #Compose MIDI message
            outport.send(sysexIn) #Send midi message

    elif event == 'Show' and down == False: 
        if values['-in-'] != '':
            messageIn = values['-in-'] #Read the text
            messageInData = [125, 77, 65, 1, type[0], color[colorName.index(values['-color-'])]] + [ord(x) for x in list(messageIn)] + [33]
            sysexIn = mido.Message('sysex', data = messageInData) #Compose MIDI message
            outport.send(sysexIn) #Send midi message

    elif event == 'Hide' and down == False: 
        outport.send(sysexHide)

    