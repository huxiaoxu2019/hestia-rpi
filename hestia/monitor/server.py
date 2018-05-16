import socket, json, sys, logging, time

from hestia.model import message
from hestia.model import queue
from hestia.util import server
from hestia.util import helper

def start():
    server.connect()
    while True:
        try:
            logging.info("socket read...")
            msg = server.readline()
            if helper.isJson(msg) == True:
                queue.push_server_read_msg(msg)
        except socket.error, e:
            logging.info("socket exception" + e.message)
            server.reconnect()
