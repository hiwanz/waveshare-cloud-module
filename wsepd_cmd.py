#!/usr/bin/python3
# -*- coding:utf-8 -*-

from PyInquirer import prompt
from pprint import pprint
import bluetooth
import struct
import time


def check_get(self, check=b'1'):
    msg = read_msg(self)
    if (msg == check):
        return True
    else:
        print('get: {0} check:{1}'.format(msg, check))
        return False


def safe_send(self, send_msg, check):
    while True:
        self.send(send_msg)
        if (check_get(self, check) == True):
            break
        time.sleep(1)


def send_cmd(self, cmd):
    check = 0
    cmd = cmd.encode()

    for i in range(0, len(cmd)):
        check = check ^ cmd[i]
    check = struct.pack(">B", check)
    cmd = b';' + cmd + b'/' + check
    print('Sending: {}'.format(cmd))
    safe_send(self, cmd, check)


def read_msg(self):
    msg = b''
    temp = ''
    while temp != b'$':
        temp = self.recv(1)
        time.sleep(0.001)
    temp = self.recv(1)
    if temp != b'$':
        msg = msg + temp
    while True:
        temp = self.recv(1)
        if temp == b'#':
            break
        msg = msg + temp
    if msg == b'':
        msg = b'$'
    return msg


if __name__ == "__main__":
    # Searching bluetooth devices
    device_names = []
    device_addrs = {}
    wsepd = {'name': 'WaveShare_EPD', 'addr': '', 'port': 1}
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print('Found {} devices.'.format(len(nearby_devices)))
    for addr, name in nearby_devices:
        print("  {} - {}".format(addr, name))
        device_names.append(name)
        device_addrs[name] = addr.decode()
    if len(device_names) == 0:
        print('No available device found.')
        quit()
    # Choose which device you want to connect with
    questions = [{
        'type': 'list',
        'name': 'device_name',
        'message': 'Which device do you choose?',
        'choices': device_names
    }]
    answers = prompt(questions)
    wsepd['addr'] = device_addrs[answers['device_name']]
    # Connect to the device
    print('Connecting WaveShare_EPD address: {}'.format(wsepd['addr']))
    try:
        s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        conn = s.connect((wsepd['addr'], wsepd['port']))
        print('{}[{}] is connected.'.format(wsepd['name'], wsepd['addr']))
        while 1:
            cmd = input('Please input your command:')
            if (not cmd):
                continue
            if (cmd == "quit"):
                break
            send_cmd(s, cmd)
            print('Receiving: {}'.format(read_msg(s)))
        s.close()
    except bluetooth.btcommon.BluetoothError as err:
        print(err)
        s.close()
