# config for router, make sure that the json file and python file are in the same directory

import telnetlib
import json
import time  # we need this module so the code can wait N second before executing new lines

with open('CCNA_DB.json') as f:
    data = json.load(f)

class CCNA_DEVICE:

    def __init__(self,ip):
        self.tn = telnetlib.Telnet(ip)
        self.M_num = data['Monitor_num']

    def login(self):
        print('Initiating configuration please wait!')
        self.tn.write(b'pass\n')
        self.tn.write(b'enable\n')
        self.tn.write(b'pass\n')
        self.tn.write(b'configure terminal\n')
        time.sleep(1)

    def end_session(self):
        time.sleep(1)
        self.tn.write(b'end\n')
        self.tn.write(b'exit\n')
        decode = self.tn.read_all().decode('ascii')
        print(decode)
        print('Device configured!')

    def config_SW(self):
        commands = [
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
        ]
        for i in commands:
            self.tn.write(i.encode('ascii') + b'\n')

    def config_CUCM(self):
        commands = [
            'no telephony-service',
            'telephony-service',
            'no auto-assign',
            'no auto-reg-ephone',
            'max-ephone 5',
            'max-dn 20',
            'ip source-address ' + data['cucm_fa0/0'] + 'port 2000',
            'create cnf-files',
            'ephone-dn 1',
            'number ' + self.M_num + '00',
            'ephone-dn 2',
            'number ' + self.M_num + '11',
            'ephone-dn 3',
            'number ' + self.M_num + '22',
            'ephone-dn 4',
            'number ' + self.M_num + '33',
            'ephone-dn 5',
            'number ' + self.M_num + '44',
            'ephone-dn 6',
            'number ' + self.M_num + '55',
            'ephone-dn 7',
            'number ' + self.M_num + '66',
            'ephone-dn 8',
            'number ' + self.M_num + '77',
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
        ]
        for i in commands:
            self.tn.write(i.encode('ascii') + b'\n')


    def config_EDGE(self):
        print('Configuring EDGE Router. Please wait!')
        time.sleep(1)
        commands = [
            'configure terminal',
            'ip address ' + data['int_gi0/0/1'] + data['Slash_24'],
            'no shutdown',
        ]
        for i in commands:
            self.tn.write(i.encode('ascii') + b'\n')

print('Starting Automation using Telnetlib')

LEAF_SW = CCNA_DEVICE(data['sw_vlan1'])
LEAF_SW.login()
LEAF_SW.config_SW()
LEAF_SW.end_session()

CUCM = CCNA_DEVICE(data['cucm_fa0/0'])
CUCM.login()
CUCM.config_CUCM()
CUCM.end_session()

EDGE = CCNA_DEVICE(data['int_gi0/0/0'])
EDGE.login()
EDGE.config_EDGE()
EDGE.end_session()

print('AUTOMATION ENDED')
input('Press Enter to exit: ')

