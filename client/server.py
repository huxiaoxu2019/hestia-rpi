#!/usr/bin/env python

import socket

_s = ''

def start(ip, port):
    global _s
    _s = socket.socket(socket.AF_INET)
    _s.connect((ip, port))
    return _s

def readLine():
    global _s
    while True:
        b = _s.recv(1)
        rs += b
        if b == '/n':
            break
    return rs

def writeLn(msg):
    global _s
    _s.send(msg + '/n')
