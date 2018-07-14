'''
Processing the messages from the clients(android or iOS)
'''
import json, logging, time

from hestia.model import message
from hestia.model import queue
from hestia.util import helper
from hestia.util import yeelight
from hestia.util import rpi
from hestia.util import server

def start():
    logging.info("[library.monitor.client] starting...")
    while True:
        logging.info("library.monitor.client] dispose msg from _monitor_client_queue")
        msg = queue.pop_monitor_client_msg()
        if helper.isJson(msg) == True:
            _execute(msg)
        else:
            time.sleep(2)

def _execute(msg):
    logging.info("[library.client.monitor:_execute_ios_request_home_device_msg] msg:" + msg)
    data = {}
    data["bulb_status"] = yeelight.get_bulb_info(yeelight.IDX_YEELIGHT_BEDROOM_LIGHT)
    data["light_model_status"] = rpi.get_light_data()
    result = message.get_common_msg()
    data["message_type"] = message.MESSAGE_TYPE_RPI_DATA_HOME_DEVICE_INFO
    result["data"] = data
    server.writeline(json.dumps(result))
