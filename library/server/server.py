import socket, json, sys, logging

from hestiarpi.model import message
from hestiarpi.library.brain import handler
from hestiarpi.config import common

_s = ''
_sFile = ''

def start(ip, port):
    global _s, _sFile
    _s = socket.socket(socket.AF_INET)
    _s.connect((ip, port))
    _sFile = _s.makefile()
    # send identity info (client key) to server
    msg = message.get_rpi_data_device_info_message()
    writeline(json.dumps(msg))
    while True:
        msg = readline()
        handler.execute(msg)

def readline():
    global _sFile
    return _sFile.readline()

def writeline(msg):
    logging.info("[library.server.server:writeline] msg sent:" + msg)
    global _s
    _s.send(msg + '\n')
