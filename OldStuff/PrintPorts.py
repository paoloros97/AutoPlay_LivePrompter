import mido


def print_ports(heading, port_names):
    print(heading)
    for name in port_names:
        print("    '{}'".format(name))
    print()


print()
print_ports('INPUT Ports:', mido.get_input_names())
print_ports('OUTPUT Ports:', mido.get_output_names())