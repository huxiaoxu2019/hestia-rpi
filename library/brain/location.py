import logging, json, math, time
from hestiarpi.library.helper import geo
from hestiarpi.config import common

_STATUS_NOT_CHANGED = 0
_STATUS_BIGGER = 1
_STATUS_SMALLER = 2
_STATUS_CONTINUOUS_BIGGER = 3
_STATUS_CONTINUOUS_SMALER = 4

_TIME_INTERNAL = 60 # one minute

_last_entry = {"last_dis" : 0, "last_time" : 0, "last_status" : _STATUS_NOT_CHANGED}

def execute(msg):
    logging.info("[library.brain.location:execute] msg:" + msg)
    _set_status(msg)


def _set_status(msg):
    global _last_entry

    # get dis
    msg_obj = json.loads(msg)
    dis = geo.get_distance_hav(msg_obj["data"]["lnt"], msg_obj["data"]["lat"], common.HOME_LNG, common.HOME_LAT)
    dis = int(math.floor(dis * 1000))
    logging.info("[library.brain.location:_set_status] dis:" + str(dis) + "m")

    # frequency
    if _last_entry["last_time"] + _TIME_INTERNAL >= int((math.floor(time.time()))):
        logging.info("[library.brain.location:_set_status] return by frequency limit")
        return

    # set status
    if dis == _last_entry["last_dis"] or 0 == _last_entry["last_dis"]:
        logging.info('no changes');
        _last_entry["last_status"] = _STATUS_NOT_CHANGED
    elif dis < _last_entry["last_dis"] and (_last_entry["last_status"] == _STATUS_SMALLER 
            or _last_entry["last_status"] == _STATUS_CONTINUOUS_SMALER):
        logging.info("c smaller");
        _last_entry["last_status"] = _STATUS_CONTINUOUS_SMALER
    elif dis > _last_entry["last_dis"] and (_last_entry["last_status"] == _STATUS_BIGGER 
            or _last_entry["last_status"] == _STATUS_CONTINUOUS_BIGGER):
        logging.info("c bigger");
        _last_entry["last_status"] = _STATUS_CONTINUOUS_BIGGER
    elif dis < _last_entry["last_dis"] and (_last_entry["last_status"] == _STATUS_NOT_CHANGED 
            or _last_entry["last_status"] == _STATUS_BIGGER or _last_entry["last_status"] == _STATUS_CONTINUOUS_BIGGER):
        logging.info("smaller");
        _last_entry["last_status"] = _STATUS_SMALLER
    elif dis > _last_entry["last_dis"] and (_last_entry["last_status"] == _STATUS_NOT_CHANGED 
            or _last_entry["last_status"] == _STATUS_SMALLER or _last_entry["last_status"] == _STATUS_CONTINUOUS_SMALER):
        logging.info("bigger");
        _last_entry["last_status"] = _STATUS_BIGGER
    else:
        logging.warning("[library.brain.location:_set_status] unknown status")

    _last_entry["last_dis"] = dis
    _last_entry["last_time"] = int(math.floor(time.time()))

    # print
    logging.info("[library.brain.location:_set_status] now entry info status:" + str(_last_entry["last_status"]) + " time:" + str(_last_entry["last_time"]))
