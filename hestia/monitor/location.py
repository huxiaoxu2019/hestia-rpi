import logging, json, math, time, threading

from hestia.util import geo
from hestia.config import common
from hestia.util import yeelight
from hestia.util import rpi
from hestia.model import message

_STATUS_NOT_CHANGED = 0
_STATUS_BIGGER = 1
_STATUS_SMALLER = 2
_STATUS_CONTINUOUS_BIGGER = 3
_STATUS_CONTINUOUS_SMALER = 4

_TIME_INTERNAL_4_SAVING_ENTRY = 60 # one minute for save location info to var `_last_entry`
_TIME_INTERNAL_4_MONITOR = 60 # for `monitor interval`
_TIME_MAX_PAST_4_MONITOR = 600 # for monitor `max past time`, within which not to trigger back home event
_DIS_HOME_BOUNDARY = 1000 # for `home boundary`, by which to determine back home or leave home
_TIME_INTERNAL_4_BACK_HOME_AGAIN = 3600 # one hour, allow to trigger back home event again, even it's already in back home event

_last_entry = {"last_dis" : 0, "last_time" : 0, "last_status" : _STATUS_NOT_CHANGED}

_did_leave_home = False
_did_back_home = False

# _last_entry = {"last_dis" : 0, "last_time" : 0, "last_status" : _STATUS_NOT_CHANGED}
def start():
    global _last_entry
    while True:
        try:
            logging.info("[library.brain.location:_monitor] did start")
            current_entry = message.pop_monitor_location_msg()
            _set_status(current_entry)
            if _last_entry["last_dis"] < _DIS_HOME_BOUNDARY and (_last_entry["last_status"] == _STATUS_SMALLER or _last_entry["last_status"] == _STATUS_CONTINUOUS_SMALER) and (int((math.floor(time.time()))) - _last_entry["last_time"] < _TIME_MAX_PAST_4_MONITOR):
                # back home
                _back_home()
            elif _last_entry["last_dis"] >= _DIS_HOME_BOUNDARY:
                # leave home
                _leave_home()
            # sleep
            time.sleep(_TIME_INTERNAL_4_MONITOR)
        except Exception as e:
            logging.warning( "Unexpected error:" + str(e))

def _set_status(msg):
    global _last_entry

    # get dis
    msg_obj = json.loads(msg)
    dis = geo.get_distance_hav(msg_obj["data"]["lnt"], msg_obj["data"]["lat"], common.HOME_LNG, common.HOME_LAT)
    dis = int(math.floor(dis * 1000))
    #logging.info("[library.brain.location:_set_status] dis:" + str(dis) + "m")

    # frequency
    if _last_entry["last_time"] + _TIME_INTERNAL_4_SAVING_ENTRY >= int((math.floor(time.time()))):
        #logging.info("[library.brain.location:_set_status] return by frequency limit")
        return

    # set status
    if dis == _last_entry["last_dis"] or 0 == _last_entry["last_dis"]:
        logging.info('no changes')
        _last_entry["last_status"] = _STATUS_NOT_CHANGED
    elif dis < _last_entry["last_dis"] and (_last_entry["last_status"] == _STATUS_SMALLER
            or _last_entry["last_status"] == _STATUS_CONTINUOUS_SMALER):
        logging.info("c smaller")
        _last_entry["last_status"] = _STATUS_CONTINUOUS_SMALER
    elif dis > _last_entry["last_dis"] and (_last_entry["last_status"] == _STATUS_BIGGER
            or _last_entry["last_status"] == _STATUS_CONTINUOUS_BIGGER):
        logging.info("c bigger")
        _last_entry["last_status"] = _STATUS_CONTINUOUS_BIGGER
    elif dis < _last_entry["last_dis"] and (_last_entry["last_status"] == _STATUS_NOT_CHANGED
            or _last_entry["last_status"] == _STATUS_BIGGER or _last_entry["last_status"] == _STATUS_CONTINUOUS_BIGGER):
        logging.info("smaller")
        _last_entry["last_status"] = _STATUS_SMALLER
    elif dis > _last_entry["last_dis"] and (_last_entry["last_status"] == _STATUS_NOT_CHANGED
            or _last_entry["last_status"] == _STATUS_SMALLER or _last_entry["last_status"] == _STATUS_CONTINUOUS_SMALER):
        logging.info("bigger")
        _last_entry["last_status"] = _STATUS_BIGGER
    else:
        logging.warning("[library.brain.location:_set_status] unknown status")

    _last_entry["last_dis"] = dis
    _last_entry["last_time"] = int(math.floor(time.time()))

    # print
    logging.info("[library.brain.location:_set_status] now entry info status:"
            + str(_last_entry["last_status"]) + " time:" + str(_last_entry["last_time"])
            + " dis:" + str(_last_entry["last_dis"]))

def _leave_home():
    logging.info("[library.brain.location:_leave_home] did start")
    global _did_leave_home
    global _did_back_home
    if _did_leave_home == True:
        logging.info("[library.brain.location:_leave_home] leave home is True")
        return
    else:
        # set flags
        _did_leave_home = True
        _did_back_home = False

    # turn off the light while the light in the room is bright and light is on
    yeelight_bedroom_light_info = yeelight.get_bulb_info(yeelight.IDX_YEELIGHT_BEDROOM_LIGHT)
    logging.info("[library.brain.location:_leave_home] the bulb power:" + str(yeelight_bedroom_light_info[yeelight.IDX_BULB_INFO_POWER]))
    if yeelight_bedroom_light_info[yeelight.IDX_BULB_INFO_POWER] == "off":
        logging.info("[library.brain.location:_leave_home] the light is already off")
        return
    rpi_light_sensor = rpi.get_light_data()
    logging.info("[library.brain.location:_leave_home] the rpi light sersor data:" + str(rpi_light_sensor))
    if rpi_light_sensor == 1:
        return
    logging.info("[library.brain.location:_leave_home] to turn off the light")
    yeelight.toggle_bulb(yeelight.IDX_YEELIGHT_BEDROOM_LIGHT)

def _back_home():
    logging.info("[library.brain.location:_back_home] did start")
    global _did_leave_home
    global _did_back_home
    global _last_entry

    if int((math.floor(time.time()))) - _last_entry["last_time"] > _TIME_INTERNAL_4_BACK_HOME_AGAIN:
        _did_back_home = False
        _did_leave_home = True

    if _did_back_home == True:
        logging.info("[library.brain.location:_back_home] back home is True")
        return
    else:
        # set flags
        _did_back_home = True
        _did_leave_home = False

    # turn on the light while the light in the room is dim and light is off
    yeelight_bedroom_light_info = yeelight.get_bulb_info(yeelight.IDX_YEELIGHT_BEDROOM_LIGHT)
    logging.info("[library.brain.location:_back_home] the bulb power:" + str(yeelight_bedroom_light_info[yeelight.IDX_BULB_INFO_POWER]))
    if yeelight_bedroom_light_info[yeelight.IDX_BULB_INFO_POWER] == "on":
        logging.info("[library.brain.location:_back_home] the light is already on")
        return
    rpi_light_sensor = rpi.get_light_data()
    logging.info("[library.brain.location:_back_home] the rpi light sersor data:" + str(rpi_light_sensor))
    if rpi_light_sensor == 0:
        return
    logging.info("[library.brain.location:_back_home] to turn on the light")
    yeelight.toggle_bulb(yeelight.IDX_YEELIGHT_BEDROOM_LIGHT)
    time.sleep(1)
    yeelight.set_bright(yeelight.IDX_YEELIGHT_BEDROOM_LIGHT, 100)
    time.sleep(1)
    yeelight.set_rgb(yeelight.IDX_YEELIGHT_BEDROOM_LIGHT, 9302576)
    time.sleep(1)
    rpi.send_cmd_by_ir_remote(rpi.IR_REMOTE_CMD_AIR_CONDITIONER_TURE_ON)
    time.sleep(1)
    rpi.send_cmd_by_ir_remote(rpi.IR_REMOTE_CMD_TV_TURE_ON)
