#!/usr/bin/env python

import sys, os, socket, json, threading, logging, time

HESTIA_RPI_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HESTIA_RPI_PATH)

from hestia.monitor import server
from hestia.monitor import yeelight
from hestia.monitor import location
from hestia.monitor import brain
from hestia.config import common

# log settings
# CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
logging.basicConfig(level = logging.NOTSET,
        format='[%(levelname)s] [%(asctime)s] [%(filename)s] [line:%(lineno)d] %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename=HESTIA_RPI_PATH + '/hestia/log',
        filemode='w')

# start socket server & yeelight monitor
t1 = threading.Thread(target=server.start)
t2 = threading.Thread(target=yeelight.start)
t3 = threading.Thread(target=location.start)
t4 = threading.Thread(target=brain.start)

t1.setDaemon(True)
t2.setDaemon(True)
t3.setDaemon(True)
t4.setDaemon(True)
t1.start()
t2.start()
t3.start()
t4.start()

# other
logging.info("[main] server started")

while True:
    # for receive the keyboard interupt event
    time.sleep(1)
