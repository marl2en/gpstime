#!/bin/sh
# start gps time 


#
echo "starting gps time program"
cd /home/pi
#echo "Deleting log files"
#rm -f *.log.*
echo "Kill processes then restart"
sudo kill $(ps -ef | grep gpstime.py | awk '{print $2}')
#sleep 2
echo "start gps time"
sudo python3 /home/pi/gpstime.py >/dev/null 2>&1
