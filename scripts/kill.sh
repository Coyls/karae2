#!/bin/sh
# launcher.sh
# Execute POC

cd /home/pi/Documents/karae
sudo pkill -f server.py 
sudo pkill -f tmp.py 
sudo pkill -f proximity.py 
sudo pkill -f rotary.py 
sudo pkill -f ground-humidity.py
sudo pkill -f switch.js 
sudo pkill -f delay.py 
sudo pkill -f button.py