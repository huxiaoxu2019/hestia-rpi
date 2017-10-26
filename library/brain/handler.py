#!/usr/bin/env python
import json

from hestiarpi.library.brain import location

# @param string msg json formated string
def execute(msg):
    print msg
    msg_obj = json.loads(msg)
    message_type = msg_obj["data"]["message_type"]
    if message_type == MESSAGE_TYPE_UNKNOWN:
        pass
    elif message_type == MESSAGE_TYPE_IOS_DATA_LOCATION:
        location.execute(msg)
    elif message_type == MESSAGE_TYPE_CSERVER_DATA_SOMEWHAT:
        pass
    elif message_type == MESSAGE_TYPE_RPI_DATA_DEVICE_INFO:
        pass
    else:
        pass
