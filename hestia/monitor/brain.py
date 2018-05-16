#!/usr/bin/env python
import json, logging

from hestia.model import message
from hestia.model import queue
from hestia.util import helper
from hestia.util import yeelight
from hestia.util import rpi
from hestia.util import server

def start():
    logging.info("[library.monitor.brain] starting...")
    while True:
        logging.info("library.monitor.brain] dispose msg from _server_read_queue")
        msg = queue.pop_server_read_msg()
        if helper.isJson(msg) == True:
            _execute(msg)
        else:
            time.sleep(2)

# @param string msg json formated string
def _execute(msg):
    logging.info("[library.monitor.brain:_execute] msg:" + msg)
    msg_obj = json.loads(msg)
    message_type = msg_obj["data"]["message_type"]
    if message_type == message.MESSAGE_TYPE_UNKNOWN:
        pass
    elif message_type == message.MESSAGE_TYPE_IOS_DATA_LOCATION:
        queue.push_monitor_location_msg(msg)
    elif message_type == message.MESSAGE_TYPE_IOS_REQUEST_HOME_DEVICE:
        _execute_ios_request_home_device_msg(msg)
    elif message_type == message.MESSAGE_TYPE_CSERVER_DATA_SOMEWHAT:
        pass
    elif message_type == message.MESSAGE_TYPE_RPI_DATA_DEVICE_INFO:
        pass
    else:
        pass

def _execute_ios_request_home_device_msg(msg):
    logging.info("[library.brain.monitor:_execute_ios_request_home_device_msg] msg:" + msg)
    data = {}
    data["bulb_status"] = yeelight.get_bulb_info(yeelight.IDX_YEELIGHT_BEDROOM_LIGHT)
    data["light_model_status"] = rpi.get_light_data()
    result = message.get_common_msg()
    data["message_type"] = message.MESSAGE_TYPE_RPI_DATA_HOME_DEVICE_INFO
    result["data"] = data
    server.writeline(json.dumps(result))
