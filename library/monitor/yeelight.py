#!/usr/bin/env python

from hestiarpi.config import common

import logging
import socket
import time
import fcntl
import re
import os
import errno
import struct
from time import sleep

_detected_bulbs = {}
_bulb_idx2ip = {}
_current_command_id = 0
_MCAST_GRP = '239.255.255.250'

IDX_YEELIGHT_BEDROOM_LIGHT = 1 # default for the bedroom light

IDX_BULB_INFO_BULB_ID = 0
IDX_BULB_INFO_MODEL = 1
IDX_BULB_INFO_POWER = 2
IDX_BULB_INFO_BRIGHT = 3
IDX_BULB_INFO_RGB = 4

_scan_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fcntl.fcntl(_scan_socket, fcntl.F_SETFL, os.O_NONBLOCK)

def start():
    logging.info("[library.monitor.yeelight:start] started")
    _bulbs_detection_loop()

def _debug(msg):
    logging.info("[library.monitor.yeelight:_debug] " + msg)

def _next_cmd_id():
    global _current_command_id
    _current_command_id += 1
    return _current_command_id
 
def _send_search_broadcast():
    '''
    multicast search request to all hosts in LAN, do not wait for response
    '''
    multicase_address = (_MCAST_GRP, 1982)
    _debug("send search request")
    msg = "M-SEARCH * HTTP/1.1\r\n"
    msg = msg + "HOST: 239.255.255.250:1982\r\n"
    msg = msg + "MAN: \"ssdp:discover\"\r\n"
    msg = msg + "ST: wifi_bulb"
    _scan_socket.sendto(msg, multicase_address)

def _bulbs_detection_loop():
    '''
    a standalone thread broadcasting search request and listening on all responses
    '''
    _debug("_bulbs_detection_loop running")
    search_interval=30000
    read_interval=100
    time_elapsed=0

    while True:
        if time_elapsed%search_interval == 0:
            _send_search_broadcast()

        # scanner
        while True:
            try:
                data = _scan_socket.recv(2048)
            except socket.error, e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    break
                else:
                    logging.warning(str(e))
                    sys.exit(1)
            _handle_search_response(data)

        time_elapsed+=read_interval
        sleep(read_interval/1000.0)
    _scan_socket.close()

def _get_param_value(data, param):
    '''
    match line of 'param = value'
    '''
    param_re = re.compile(param+":\s*([ -~]*)") #match all printable characters
    match = param_re.search(data)
    value=""
    if match != None:
        value = match.group(1)
        return value

def _handle_search_response(data):
    '''
    Parse search response and extract all interested data.
    If new bulb is found, insert it into dictionary of managed bulbs.
    '''
    # Location: yeelight://192.168.99.122:55443
    location_re = re.compile("Location.*yeelight[^0-9]*([0-9]{1,3}(\.[0-9]{1,3}){3}):([0-9]*)")
    match = location_re.search(data)
    if match == None:
        _debug( "invalid data received: " + data )
        return

    host_ip = match.group(1)
    if _detected_bulbs.has_key(host_ip):
        bulb_id = _detected_bulbs[host_ip][0]
    else:
        bulb_id = len(_detected_bulbs)+1
    host_port = match.group(3)
    model = _get_param_value(data, "model")
    power = _get_param_value(data, "power")
    bright = _get_param_value(data, "bright")
    rgb = _get_param_value(data, "rgb")
    # use two dictionaries to store index->ip and ip->bulb map
    _detected_bulbs[host_ip] = [bulb_id, model, power, bright, rgb, host_port]
    _bulb_idx2ip[bulb_id] = host_ip

def display_bulb(idx):
    if not _bulb_idx2ip.has_key(idx):
        logging.warning("error: invalid bulb idx")
        return
    bulb_ip = _bulb_idx2ip[idx]
    model = _detected_bulbs[bulb_ip][1]
    power = _detected_bulbs[bulb_ip][2]
    bright = _detected_bulbs[bulb_ip][3]
    rgb = _detected_bulbs[bulb_ip][4]
    logging.info(str(idx) + ": ip=" \
        +bulb_ip + ",model=" + model \
        +",power=" + power + ",bright=" \
        + bright + ",rgb=" + rgb)

def get_bulb_info(idx):
    if not _bulb_idx2ip.has_key(idx):
        logging.warning("error: invalid bulb idx")
        return
    bulb_ip = _bulb_idx2ip[idx]
    return _detected_bulbs[bulb_ip]

def display_bulbs():
    logging.info(str(len(_detected_bulbs)) + " managed bulbs")
    for i in range(1, len(_detected_bulbs)+1):
        display_bulb(i)

def operate_on_bulb(idx, method, params):
    '''
    Operate on bulb; no gurantee of success.
    Input data 'params' must be a compiled into one string.
    E.g. params="1"; params="\"smooth\"", params="1,\"smooth\",80"
    '''
    if not _bulb_idx2ip.has_key(idx):
        logging.warning("error: invalid bulb idx")
        return

    bulb_ip=_bulb_idx2ip[idx]
    port=_detected_bulbs[bulb_ip][5]
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info( "connect " + str(bulb_ip) + str(port) + "...")
        tcp_socket.connect((bulb_ip, int(port)))
        msg="{\"id\":" + str(_next_cmd_id()) + ",\"method\":\""
        msg += method + "\",\"params\":[" + params + "]}\r\n"
        tcp_socket.send(msg)
        tcp_socket.close()
    except Exception as e:
        logging.warning( "Unexpected error:" + str(e))

def toggle_bulb(idx):
    _debug("toggle_bulb")
    operate_on_bulb(idx, "toggle", "")

def set_bright(idx, bright):
    _debug("set_bright")
    operate_on_bulb(idx, "set_bright", str(bright))
