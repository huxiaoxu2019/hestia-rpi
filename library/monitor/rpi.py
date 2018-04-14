#!/usr/bin/env python

import RPi.GPIO as GPIO
from hestiarpi.config import common
import time, logging, threading, socket, errno, commands

IR_REMOTE_CMD_TV_TURE_ON = 'KEY_POWER';
IR_REMOTE_CMD_TV_TURE_OFF = 'KEY_POWER';
IR_REMOTE_CMD_AIR_CONDITIONER_TURE_ON = 'KEY_OPEN';
IR_REMOTE_CMD_AIR_CONDITIONER_TURE_OFF = 'KEY_CLOSE';

def start():
    logging.info("[library.monitor.rpi:start] started")

def _observe_light_module():
    get_light_data()

def get_light_data():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(common.GPIO_LIGHT_OUTPUT_VCC, GPIO.OUT)
    GPIO.setup(common.GPIO_LIGHT_INPUT_DATA, GPIO.IN)
    GPIO.output(common.GPIO_LIGHT_OUTPUT_VCC, GPIO.HIGH)
    return GPIO.input(common.GPIO_LIGHT_INPUT_DATA)

def set_sound_on():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(common.GPIO_ALERT_OUTPUT_VCC, GPIO.OUT)
    GPIO.setup(common.GPIO_ALERT_OUTPUT_DATA, GPIO.OUT)
    GPIO.output(common.GPIO_ALERT_OUTPUT_DATA, GPIO.LOW)
    GPIO.output(common.GPIO_ALERT_OUTPUT_VCC, GPIO.HIGH)

def set_sound_off():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(common.GPIO_ALERT_OUTPUT_VCC, GPIO.OUT)
    GPIO.setup(common.GPIO_ALERT_OUTPUT_DATA, GPIO.OUT)
    GPIO.output(common.GPIO_ALERT_OUTPUT_DATA, GPIO.HIGH)
    GPIO.cleanup((common.GPIO_ALERT_OUTPUT_VCC, common.GPIO_ALERT_OUTPUT_DATA))

def send_cmd_by_ir_remote(cmd):
    status, output = commands.getstatusoutput("irsend SEND_ONCE /home/pi/lircd.conf " + cmd)
    logging.info("[library.monitor.rpi:send_cmd_by_ir_remote] execute cmd: irsend SEND_ONCE /home/pi/lircd.conf " + cmd + " status:" + str(status))
    if status != 0:
        logging.warning("[library.monitor.rpi:send_cmd_by_ir_remote] output:" + output)
    return status

