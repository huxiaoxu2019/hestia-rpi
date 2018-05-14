#!/bin/bash

nohup ./main.py > console &

tail -f console log
