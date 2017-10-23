#!/usr/bin/env python

import sys, os, socket

HESTIA_RPI_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HESTIA_RPI_PATH)

from hestiarpi.config import common
from hestiarpi.library.brain import handler
from hestiarpi.library.server import server
import hestiarpi.model.message as htmessage

server.start(common.SERVER_IP, common.SERVER_SOCKET_PORT)

print htmessage.get_rpi_data_device_info_message()

msg = '{"errno":0,"errmsg":"successfully","data":{"message_type":' + str(htmessage.MESSAGE_TYPE_RPI_DATA_DEVICE_INFO) +',"client_key":"raspberry_pi_client_key","token":"aaabbbccc"}}'

server.writeline(msg)

while True:
    msg = server.readline()
    handler.execute(msg)
