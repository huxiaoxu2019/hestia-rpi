#!/usr/bin/env python

_monitor_server_read_queue = []
_monitor_location_queue = []
_monitor_client_queue = []

def pop_monitor_server_read_msg():
    if len(_monitor_server_read_queue) == 0:
        return ""
    return _monitor_server_read_queue.pop()

def push_monitor_server_read_msg(msg):
    _monitor_server_read_queue.append(msg)

def pop_monitor_location_msg():
    if len(_monitor_location_queue) == 0:
        return ""
    return _monitor_location_queue.pop()

def push_monitor_location_msg(msg):
    _monitor_location_queue.append(msg)

def pop_monitor_client_msg():
    if len(_monitor_client_queue) == 0:
        return ""
    return _monitor_client_queue.pop()

def push_monitor_client_msg(msg):
    _monitor_client_queue.append(msg)
