# config for switch , make sure that the json file and python file are in the same directory

import telnetlib
import json

with open('CCNA_DB.json') as f:
    data = json.load(f)

print('Starting Automation using Telnetlib')

tn = telnetlib.Telnet(data['sw_vlan1'])

commands = [
    'pass',
    'enable',
    'pass',
    'configure terminal',
    'interface vlan 10',
    'ip address ' + data['sw_vlan10'] + ' ' + data['Slash_24'],
    'description WIRELESSVLAN',
    'interface vlan 100',
    'no shutdown',
    'ip address ' + data['sw_vlan100'] + ' ' + data['Slash_24'],
    'description VOICEVLAN',
    'end',
    'configure terminal',
    'ip dhcp excluded-address ' + data['exclude_v1'],
    'ip dhcp excluded-address ' + data['exclude_v10'],
    'ip dhcp excluded-address ' + data['exclude_v100'],
    'ip dhcp pool MGMTVLAN',
    'network ' + data['v1_network'] + ' ' + data['Slash_24'],
    'default-router ' + data['sw_vlan1'],
    'dns-server ' + data['pc_ip'],
    'domain-name mgmt.com',
    'ip dhcp pool WIRELESSDATA',
    'network ' + data['v10_network'] + ' ' + data['Slash_24'],
    'default-router ' + data['sw_vlan10'],
    'dns-server ' + data['pc_ip'],
    'domain-name data.com',
    'ip dhcp pool VOICEVLAN',
    'network ' + data['v100_network'] + ' ' + data['Slash_24'],
    'default-router ' + data['sw_vlan100'],
    'dns-server ' + data['pc_ip'],
    'domain-name voice.com',
    'option 150 ip ' + data['cucm_fa0/0'],
    'end',
    'configure terminal',
    'vlan 10',
    'name WirelessDATA',
    'vlan 100',
    'name VoiceVLAN',
    'interface fastethernet 0/2',
    'switchport mode access',
    'switchport access vlan 10',
    'exit',
    'interface range fa0/3 , fa0/7 , fa0/5',
    'switchport mode access',
    'switchport access vlan 100',
    'exit',
    'ip routing',
    'end',
    'exit'
]

for i in commands:
    tn.write(i.encode('ascii') + b'\n')

de = tn.read_all().decode('ascii')
print('AUTOMATION ENDED SHOWING YOU THE LOGS\n')
print(de)