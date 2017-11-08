import logging, json
from hestiarpi.library.helper import geo
from hestiarpi.config import common

def execute(msg):
    logging.info("[library.brain.location:execute] msg:" + msg)
    msg_obj = json.loads(msg)
    dis = geo.get_distance_hav(msg_obj["data"]["lnt"], msg_obj["data"]["lat"], common.HOME_LNG, common.HOME_LAT)
    logging.info("[library.brain.location:execute] dis:" + str(dis))
