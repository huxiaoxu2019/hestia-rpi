'''
Distribute  messages.
'''
#!/usr/bin/env python
import json, logging, time

from hestia.model import message
from hestia.model import queue
from hestia.util import helper
from hestia.util import yeelight
from hestia.util import rpi
from hestia.util import server

def start():
    logging.info("[library.monitor.proxy] starting...")
    while True:
        logging.info("library.monitor.proxy] dispose msg from _monitor_server_read_queue")
        msg = queue.pop_monitor_server_read_msg()
        if helper.isJson(msg) == True:
            _execute(msg)
        else:
            time.sleep(2)

# @param string msg json formated string
def _execute(msg):
    logging.info("[library.monitor.proxy:_execute] msg:" + msg)
    msg_obj = json.loads(msg)
    message_type = msg_obj["data"]["message_type"]
    if message_type == message.MESSAGE_TYPE_UNKNOWN:
        pass
    elif message_type == message.MESSAGE_TYPE_IOS_DATA_LOCATION:
        queue.push_monitor_location_msg(msg)
    elif message_type == message.MESSAGE_TYPE_IOS_REQUEST_HOME_DEVICE:
        queue.push_monitor_client_msg(msg)
    elif message_type == message.MESSAGE_TYPE_CSERVER_DATA_SOMEWHAT:
        pass
    elif message_type == message.MESSAGE_TYPE_RPI_DATA_DEVICE_INFO:
        pass
    else:
        pass
