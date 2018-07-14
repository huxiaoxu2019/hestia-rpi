import socket, json, logging, time
from hestia.config import common
from hestia.model import message

_socket = ''
_sfile = ''

def get_socket():
    global _socket
    return _socket

def connect():
    global _socket, _sfile
    go = True
    while go:
        try:
            _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _socket.connect((common.SERVER_IP, common.SERVER_SOCKET_PORT))
            _sfile = _socket.makefile()
            # send identity info (client key) to server
            msg = message.get_rpi_data_device_info_message()
            writeline(json.dumps(msg))
            go = False
        except socket.error, e:
            logging.info("socket exception" + e.message)
            reconnect()

def writeline(msg):
    logging.info("[library.util.server:writeline] msg sent:" + msg)
    try:
        global _socket
        _socket.send(msg + '\n')
    except socket.error, e:
        logging.warning("socket exception" + e.message)
        reconnect()

def readline():
    try:
        global _sfile
        msg = _sfile.readline()
        if msg == "":
            reconnect()
    except socket.error, e:
        logging.info("socket exception" + e.message)
        reconnect()
    return msg

def reconnect():
    try:
        global _socket, _sfile
        logging.info("reconnect to server...")
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.connect((common.SERVER_IP, common.SERVER_SOCKET_PORT))
        _sfile = _socket.makefile()
        # send identity info (client key) to server
        msg = message.get_rpi_data_device_info_message()
        writeline(json.dumps(msg))
        time.sleep(2)
    except socket.error, e:
        logging.info("socket exception" + e.message)
        time.sleep(2)
