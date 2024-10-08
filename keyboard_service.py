#!/usr/bin/env python
'''foo
'''

import subprocess as sp

BATTERY_FILE = '/home/dan/.battery'
SERIAL_PORT = '/dev/ttyACM0'
cmd = ['cat', SERIAL_PORT]

# p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
with sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE) as p:
    for line in iter(p.stdout.readline, b''):
        line = line.decode('utf-8').strip()
        if not line:
            continue
        elif line.startswith('voltage'):
            voltage = line.split(' ')[-1]
            try:
                voltage = round(float(voltage), 2)
            except ValueError:
                continue

            with open(BATTERY_FILE, 'w', encoding='utf-8') as f:
                f.write(str(voltage))

            print(line, voltage)

        elif line.startswith('SYS'):
            line = line.split()[1:]
            user = line[0]
            command = line[1:]
            cmd = ['/bin/su', user, '-c', ' '.join(command)]
            sp.call(cmd)
