#!/usr/bin/env python

import sys, os, socket, json, threading

HESTIA_RPI_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HESTIA_RPI_PATH)

from hestiarpi.library.server import server
from hestiarpi.library.monitor import rpi
from hestiarpi.config import common

# start socket server
t1 = threading.Thread(target=server.start, args=(common.SERVER_IP, common.SERVER_SOCKET_PORT))
t2 = threading.Thread(target=rpi.start)

t1.start()
t2.start()
