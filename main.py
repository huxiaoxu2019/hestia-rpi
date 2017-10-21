#!/usr/bin/env python

import sys, os, socket

HESTIA_RPI_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HESTIA_RPI_PATH)

from hestiarpi.config import common
from hestiarpi.client import server
from hestiarpi.model.brain import handler

server.start(common.SERVER_IP, common.SERVER_SOCKET_PORT)

while True:
    msg = server.readLine()
    handler.execute(msg)
