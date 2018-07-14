import logging
import socket
import time
import fcntl
import os

IDX_YEELIGHT_BEDROOM_LIGHT = 1 # default for the bedroom light

IDX_BULB_INFO_BULB_ID = 0
IDX_BULB_INFO_MODEL = 1
IDX_BULB_INFO_POWER = 2
IDX_BULB_INFO_BRIGHT = 3
IDX_BULB_INFO_RGB = 4

detected_bulbs = {}
bulb_idx2ip = {}
current_command_id = 0
MCAST_GRP = '239.255.255.250'
scan_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fcntl.fcntl(scan_socket, fcntl.F_SETFL, os.O_NONBLOCK)

def get_bulb_info(idx):
    if not bulb_idx2ip.has_key(idx):
        logging.warning("error: invalid bulb idx")
        return
    bulb_ip = bulb_idx2ip[idx]
    return detected_bulbs[bulb_ip]

def display_bulb(idx):
    if not bulb_idx2ip.has_key(idx):
        logging.warning("error: invalid bulb idx")
        return
    bulb_ip = bulb_idx2ip[idx]
    model = detected_bulbs[bulb_ip][1]
    power = detected_bulbs[bulb_ip][2]
    bright = detected_bulbs[bulb_ip][3]
    rgb = detected_bulbs[bulb_ip][4]
    logging.info(str(idx) + ": ip=" \
        +bulb_ip + ",model=" + model \
        +",power=" + power + ",bright=" \
        + bright + ",rgb=" + rgb)

def display_bulbs():
    logging.info(str(len(detected_bulbs)) + " managed bulbs")
    for i in range(1, len(detected_bulbs)+1):
        display_bulb(i)

def operate_on_bulb(idx, method, params):
    '''
    Operate on bulb; no gurantee of success.
    Input data 'params' must be a compiled into one string.
    E.g. params="1"; params="\"smooth\"", params="1,\"smooth\",80"
    '''
    if not bulb_idx2ip.has_key(idx):
        logging.warning("error: invalid bulb idx")
        return

    bulb_ip=bulb_idx2ip[idx]
    port=detected_bulbs[bulb_ip][5]
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info( "connect " + str(bulb_ip) + ":" + str(port) + "...")
        tcp_socket.connect((bulb_ip, int(port)))
        msg="{\"id\":" + str(_next_cmd_id()) + ",\"method\":\""
        msg += method + "\",\"params\":[" + params + "]}\r\n"
        tcp_socket.send(msg)
        tcp_socket.close()
    except Exception as e:
        logging.warning( "Unexpected error:" + str(e))

def toggle_bulb(idx):
    logging.info("[library.monitor.yeelight:toggle_bulb] toggle_bulb")
    operate_on_bulb(idx, "toggle", "")

def set_bright(idx, bright):
    logging.info("[library.monitor.yeelight:toggle_bulb] set_bright")
    operate_on_bulb(idx, "set_bright", str(bright))

def set_rgb(idx, rgb):
    logging.info("[library.monitor.yeelight:toggle_bulb] set_rgb")
    operate_on_bulb(idx, "set_rgb", str(rgb))

def set_ct_abx(idx, ct):
    logging.info("[library.monitor.yeelight:toggle_bulb] set_ct_abx")
    operate_on_bulb(idx, "set_ct_abx", str(ct))
