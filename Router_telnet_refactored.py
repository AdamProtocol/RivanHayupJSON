# config for router, make sure that the json file and python file are in the same directory

import telnetlib
import json
import time  # we need this module so the code can wait N second before executing new lines

with open('CCNA_DB.json') as f:
    data = json.load(f)

print('Starting Automation using Telnetlib')

tn = telnetlib.Telnet(data['int_gi0/0/0'])

commands = [
    'pass',
    'enable',
    'pass',
    'configure terminal',
    'ip address ' + data['int_gi0/0/1'] + data['Slash_24'],
    'no shutdown',
    'end',
    'exit'
]

for i in commands:
    tn.write(i.encode('ascii') + b'\n')

de = tn.read_all().decode('ascii')
print('AUTOMATION ENDED SHOWING YOU THE LOGS\n')
print(de)
