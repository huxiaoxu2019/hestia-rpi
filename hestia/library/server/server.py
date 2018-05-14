import socket, json, sys, logging, time

from hestia.model import message
from hestia.library.brain import handler
from hestia.config import common

_s = ''
_sFile = ''
_ip = ''
_port = ''

def start(ip, port):
    global _s, _sFile, _ip, _port
    _ip = ip
    _port = port
    go = True
    while go:
        try:
            _s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _s.connect((ip, port))
            _sFile = _s.makefile()
            # send identity info (client key) to server
            msg = message.get_rpi_data_device_info_message()
            writeline(json.dumps(msg))
            go = False
        except socket.error, e:
            logging.info("socket exception" + e.message)
            _reconnect()
    while True:
        try:
            logging.info("socket read...")
            msg = readline()
            if _isJson(msg) == True:
                handler.execute(msg)
        except socket.error, e:
            logging.info("socket exception" + e.message)
            _reconnect()

def readline():
    global _sFile
    try:
        msg = _sFile.readline()
        if msg == "":
            _reconnect()
    except socket.error, e:
        logging.info("socket exception" + e.message)
        _reconnect()
    return msg

def writeline(msg):
    logging.info("[library.server.server:writeline] msg sent:" + msg)
    global _s
    try:
        _s.send(msg + '\n')
    except socket.error, e:
        logging.info("socket exception" + e.message)
        _reconnect()

def _isJson(msg):
    try:
        json.loads(msg)
    except ValueError:
        return False
    return True

def _reconnect():
    try:
        logging.info("reconnect to server...")
        global _s, _sFile, _ip, _port
        _s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _s.connect((_ip, _port))
        _sFile = _s.makefile()
        # send identity info (client key) to server
        msg = message.get_rpi_data_device_info_message()
        writeline(json.dumps(msg))
        time.sleep(2)
    except socket.error, e:
        logging.info("socket exception" + e.message)
        time.sleep(2)
