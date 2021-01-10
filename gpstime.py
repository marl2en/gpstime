#! /usr/bin/python
# 
# Every 15 Minutes crontab -e
# */15 * * * * sudo /home/pi/gpstime.sh # >/dev/null 2>&1
# ps -ef | grep gpstime.py 
# cat gpstime.log | grep 'Setting new time'
 
import os
from gps import *
import time
import threading
import urllib.request
import datetime as dt
import pytz
import sys
import subprocess
import shlex
import logging, logging.config

# logging ###########################################################################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                    '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'rotate_file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "/home/pi/gpstime.log",
            'encoding': 'utf8',
            'maxBytes': 100000,
            'backupCount': 1,
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'rotate_file'],
            'level': 'DEBUG',
        },
    }
}
logging.captureWarnings(True) #send warnings to log




def _linux_set_time(gps_local_time): # from: https://stackoverflow.com/questions/12081310/python-module-to-change-system-date-and-time
  time_string = gps_local_time.isoformat()
  #subprocess.call(shlex.split("timedatectl set-ntp false"))  # May be necessary
  subprocess.call(shlex.split("sudo date -s '%s'" % time_string))
  #subprocess.call(shlex.split("sudo hwclock -w")) # no rtc

local_time_zone = pytz.timezone('Europe/Stockholm')

gpsd = None 
 
polling_interval = 2 # in sec
running_time = 60 # in sec
maximum_offset = 2. # in sec before trigger a change in system time

def connected(host='http://svd.se'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False


class GpsPoller(threading.Thread):  # from: https://gist.github.com/wolfg1969/4653340
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

logging.config.dictConfig(LOGGING)

if not connected():
  logging.debug('No Internet Connection. start GPS TIME' )
  gpsp = GpsPoller() # thread
  try:
    gpsp.start() 
    starttime = time.time()
    while (time.time() < starttime + running_time) :
      utc_time=gpsd.utc
      try:
        gpstime_utc = dt.datetime.strptime(utc_time.split('.')[0], "%Y-%m-%dT%H:%M:%S")
        gpstime_utc2 = pytz.utc.localize(gpstime_utc, is_dst=None)
        gps_local_time = gpstime_utc2.astimezone(local_time_zone)
        system_time = dt.datetime.now()
        system_time = local_time_zone.localize(system_time)
        offset = system_time - gps_local_time
        offset = offset.total_seconds()
        logging.debug('Offset: %s' % str(offset))
        if abs(offset) > maximum_offset:
          _linux_set_time(gps_local_time)
          logging.debug('Setting new time. Offset: %s' % str(offset))
      except Exception as e:
        logging.debug('Exception: %s' % e)
      time.sleep(polling_interval) 
  except (KeyboardInterrupt, SystemExit): 
    logging.debug("Killing Thread.")
    gpsp.running = False
    gpsp.join() 
  logging.debug("Done.")
else:
  logging.debug('Internet Connection.No need for GPS Time' )


sys.exit()





