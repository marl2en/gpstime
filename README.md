# gpstime

a simple program to adjust time when no internet connection is available
Running on a Raspberry Pi.
Spending hours trying to use gps time as source for  chrony or ntp I finally gave up and wrote a tiny python program to do the job. 

 # Requirement:
    • Rpi (tested on Rpi 3+ and Rpi 4
    • a cheap GPS-USB Dongle



Use this software at your own risk. 


# Install:
Plug the GPS dongle into a USB port.
lsusb: “Bus 001 Device 010: ID 1546:01a7 U-Blox AG [u-blox 7]”
dmesg: look for something like: “/dev/ttyACM0″


sudo apt-get install gpsd-clients gpsd python-gps
sudo apt-get install chrony (or ntp)

sudo nano /etc/default/gpsd
START_DAEMON=”true”
USBAUTO=”true”
DEVICES=”/dev/ttyACM0″
GPSD_OPTIONS=”-n”

reboot
check status:
sudo systemctl status -l gpsd.socket
sudo systemctl status -l gpsd.service

# check GPS data:
cat /dev/ttyACM0
cgps    
gpsmon -n  
xgps 127.0.0.1:2947

# How to use:
copy gpstime.py and gpstime.sh to home/pi
create a cron job: crontab -e
*/15 * * * * sudo /home/pi/gpstime.sh # >/dev/null 2>&1

Adjust your settings in  gpstime.py like polling interval, running time, maximum time offset to trigger time reset etc. 
Look at log file:
cat home/pi/gpstime.log 

Have a nice day. 
