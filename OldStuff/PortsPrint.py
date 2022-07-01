import mido
print('MIDI ports available:')
print('INPUT:\t', mido.get_input_names())
print('OUTPUT:\t', mido.get_output_names())