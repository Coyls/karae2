#!/bin/sh
# launcher.sh
# Execute POC

sleep 20
cd /home/pi/Documents/karae
python3 ./server.py &
sleep 3
python3 ./tmp.py &
python3 ./proximity.py &
python3 ./rotary.py &
python3 ./ground-humidity.py &
python3 ./delay.py &
python3 ./button.py &
sudo node ./puck/switch.js &
