#!/usr/bin/env python

import sys, os, socket, json, threading, logging, time

HESTIA_RPI_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HESTIA_RPI_PATH)

from hestiarpi.library.server import server
from hestiarpi.library.monitor import rpi
from hestiarpi.config import common

# log settings
# CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
logging.basicConfig(level = logging.NOTSET,
        format='[%(levelname)s] [%(asctime)s] [%(filename)s] [line:%(lineno)d] %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='log',
        filemode='w')

# start socket server & rpi monitor
t1 = threading.Thread(target=server.start, args=(common.SERVER_IP, common.SERVER_SOCKET_PORT))
t2 = threading.Thread(target=rpi.start)

t1.setDaemon(True)
t2.setDaemon(True)
t1.start()
t2.start()

# other
logging.info("[main] server started")

while True:
    # for receive the keyboard interupt event
    time.sleep(1)
