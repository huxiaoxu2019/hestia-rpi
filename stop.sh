#!/bin/bash

pid=`ps -ef | grep "main.py" | grep -v "grep" | awk '{print $2}'`
if [ $pid -gt 0 ];then
    `kill -9 ${pid}`
    echo "hestia rpi(pid ${pid}) has been stopped."
else
    echo "no rpi server running."
fi
