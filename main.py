#!/usr/bin/env python

import sys, os, socket, json

HESTIA_RPI_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HESTIA_RPI_PATH)

import hestiarpi.config as htconfig
import hestiarpi.library as htlibrary
import hestiarpi.model as htmodel

# start socket server
htlibrary.server.server.start(htconfig.common.SERVER_IP, htconfig.common.SERVER_SOCKET_PORT)

# send identity info (client key) to server
msg = htmodel.message.get_rpi_data_device_info_message()
htlibrary.server.server.writeline(json.dumps(msg))

while True:
    msg = htlibrary.server.server.readline()
    htlibrary.brain.handler.execute(msg)
