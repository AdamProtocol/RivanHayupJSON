# config for cucm, make sure that the json file and python file are in the same directory

import telnetlib
import json
import time  # we need this module so the code can wait N second before executing new lines

with open('CCNA_DB.json') as f:
    data = json.load(f)

monitor_num = 11

print('Starting Automation using Telnetlib')

tn = telnetlib.Telnet(data['cucm_fa0/0'])

commands = [
    'pass',
    'enable',
    'pass',
    'configure terminal',
    'no telephony-service',
    'telephony-service',
    'no auto-assign',
    'no auto-reg-ephone',
    'max-ephone 5',
    'max-dn 20',
    'ip source-address ' + data['cucm_fa0/0'] + 'port 2000',
    'create cnf-files',
    'ephone-dn 1',
    'number ' + str(monitor_num) + '00',
    'ephone-dn 2',
    'number ' + str(monitor_num) + '11',
    'ephone-dn 3',
    'number ' + str(monitor_num) + '22',
    'ephone-dn 4',
    'number ' + str(monitor_num) + '33',
    'ephone-dn 5',
    'number ' + str(monitor_num) + '44',
    'ephone-dn 6',
    'number ' + str(monitor_num) + '55',
    'ephone-dn 7',
    'number ' + str(monitor_num) + '66',
    'ephone-dn 8',
    'number ' + str(monitor_num) + '77',
    'ephone 1',
    'mac-address ' + data['ephone1_mac'],
    '8945',
    'button 1:1 2:3 3:2 4:4',
    'restart',
    'ephone 2',
    'mac-address ' + data['ephone2_mac'],
    '8945',
    'button 1:5 2:6 3:7 4:8',
    'restart',
    'end',
    'configure terminal',
    'ephone 1',
    'video'
    'h323',
    'call start slow',
    'ephone 2',
    'video',
    'h323',
    'call start slow',
    'end',
    'exit'
]

for i in commands:
    tn.write(i.encode('ascii') + b'\n')

de = tn.read_all().decode('ascii')
print('AUTOMATION ENDED SHOWING YOU THE LOGS\n')
print(de)
