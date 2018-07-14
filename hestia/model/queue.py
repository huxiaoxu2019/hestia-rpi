#!/usr/bin/env python

_server_read_queue = []
_monitor_location_queue = []

def pop_server_read_msg():
    return _server_read_queue.pop()

def push_server_read_msg(msg):
    _server_read_queue.append(msg)

def pop_monitor_location_msg():
    return _monitor_location_queue.pop()

def push_monitor_location_msg(msg):
    _monitor_location_queue.append(msg)

