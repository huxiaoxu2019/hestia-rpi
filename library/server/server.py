#!/usr/bin/env python

import socket
import hestiarpi.config as htconfig

_s = ''
_sFile = ''

def start(ip, port):
    global _s, _sFile
    _s = socket.socket(socket.AF_INET)
    _s.connect((ip, port))
    _sFile = _s.makefile()

def readline():
    global _sFile
    return _sFile.readline()

def writeline(msg):
    global _s
    _s.send(msg + '\n')
    if (htconfig.common.DEBUG == True):
        print "msg sent:" + msg
