#!/usr/bin/env python

import sys, os, socket, json, threading

HESTIA_RPI_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HESTIA_RPI_PATH)

from hestiarpi.library.server import server
from hestiarpi.config import common

# start socket server
server.start(common.SERVER_IP, common.SERVER_SOCKET_PORT)

t1 =threading.Thread(target=server.start, args=(htconfig.common.SERVER_IP, htconfig.common.SERVER_SOCKET_PORT))

t1.start()
t1.join

print 'server shutdown'
