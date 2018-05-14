import logging, json

from hestia.library.monitor import yeelight
from hestia.library.monitor import rpi
from hestia.model import message
import hestia.library.server as S

def execute(msg):
    logging.info("[library.brain.monitor:execute] msg:" + msg)
    data = {}
    data["bulb_status"] = yeelight.get_bulb_info(yeelight.IDX_YEELIGHT_BEDROOM_LIGHT)
    data["light_model_status"] = rpi.get_light_data()
    result = message.get_common_msg()
    data["message_type"] = message.MESSAGE_TYPE_RPI_DATA_HOME_DEVICE_INFO
    result["data"] = data
    S.server.writeline(json.dumps(result))
