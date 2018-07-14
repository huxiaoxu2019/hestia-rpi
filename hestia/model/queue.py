#!/usr/bin/env python

_monitor_server_read_queue = []
_monitor_location_queue = []
_monitor_client_queue = []

def pop_monitor_server_read_msg():
    return _monitor_server_read_queue.pop()

def push_monitor_server_read_msg(msg):
    _monitor_server_read_queue.append(msg)

def pop_monitor_location_msg():
    return _monitor_location_queue.pop()

def push_monitor_location_msg(msg):
    _monitor_location_queue.append(msg)

def pop_monitor_client_msg():
    return _monitor_client_queue.pop()

def push_monitor_client_msg(msg):
    _monitor_client_queue.append(msg)
