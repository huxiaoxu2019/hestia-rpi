#!/usr/bin/env python

# author yeelight.com
# author genialx <admin@ihuxu.com>
from hestia.config import common
from hestia.util import yeelight

import logging
import socket
import time
import fcntl
import re
import os
import errno
import struct
from time import sleep

def start():
    logging.info("[library.monitor.yeelight:start] started")
    _bulbs_detection_loop()

def _next_cmd_id():
    yeelight.current_command_id += 1
    return yeelight.current_command_id
 
def _send_search_broadcast():
    '''
    multicast search request to all hosts in LAN, do not wait for response
    '''
    multicase_address = (yeelight.MCAST_GRP, 1982)
    logging.info("[library.monitor.yeelight:_send_search_broadcast] send search request")
    msg = "M-SEARCH * HTTP/1.1\r\n"
    msg = msg + "HOST: 239.255.255.250:1982\r\n"
    msg = msg + "MAN: \"ssdp:discover\"\r\n"
    msg = msg + "ST: wifi_bulb"
    try:
        yeelight.scan_socket.sendto(msg, multicase_address)
    except  yeelight.scan_socket.error, e:
        logging.warning("[library.monitor.yeelight:_send_search_broadcast] Error:%s" + str(e)) 

def _bulbs_detection_loop():
    '''
    a standalone thread broadcasting search request and listening on all responses
    '''
    logging.info("[library.monitor.yeelight:_bulbs_detection_loop] running")
    search_interval=30000
    read_interval=100
    time_elapsed=0

    while True:
        if time_elapsed%search_interval == 0:
            _send_search_broadcast()

        # scanner
        while True:
            try:
                data = yeelight.scan_socket.recv(2048)
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
    yeelight.scan_socket.close()

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
        logging.info("[library.monitor.yeelight:_bulbs_detection_loop] invalid data received: " + data)
        return

    host_ip = match.group(1)
    if yeelight.detected_bulbs.has_key(host_ip):
        bulb_id = yeelight.detected_bulbs[host_ip][0]
    else:
        bulb_id = len(yeelight.detected_bulbs)+1
    host_port = match.group(3)
    model = _get_param_value(data, "model")
    power = _get_param_value(data, "power")
    bright = _get_param_value(data, "bright")
    rgb = _get_param_value(data, "rgb")
    # use two dictionaries to store index->ip and ip->bulb map
    yeelight.detected_bulbs[host_ip] = [bulb_id, model, power, bright, rgb, host_port]
    yeelight.bulb_idx2ip[bulb_id] = host_ip
