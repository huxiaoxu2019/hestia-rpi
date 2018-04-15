import logging, json
from hestiarpi.library.monitor import yeelight
from hestiarpi.library.monitor import rpi
from hestiarpi.model.message import message
from hestiarpi.library.server import server

def execute(msg):
    logging.info("[library.brain.monitor:execute] msg:" + msg)
    data = {}
    data["bulb_status"] = yeelight.get_bulb_info(yeelight.IDX_YEELIGHT_BEDROOM_LIGHT)
    data["light_model_status"] = rpi.get_light_data()
    result = message.get_common_msg()
    result["message_type"] = message.MESSAGE_TYPE_RPI_DATA_DEVICE_INFO
    result["data"] = data
    server.writeline(json.dumps(result))
