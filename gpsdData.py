#! /usr/bin/python
 
import os
import time
import threading
import math
from time import *
import datetime
import csv
import numpy as np
import functions as func
from gps import *
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)
GPIO.setup(10, GPIO.IN) #pin 19
GPIO.setup(18, GPIO.OUT) #pin 12
GPIO.setup(17, GPIO.OUT) #pin 11
GPIO.setup(27, GPIO.OUT) #pin 13
GPIO.setup(22, GPIO.OUT) #pin 15
 
gpsd = None #seting the global variable
 
track_points = 1167
gps_coords = []

track_coords = func.functions.getTrackData('LongLat')
track_ranges = func.functions.getTrackData('Range')

gps_long = 0
gps_lat = 0

lap_start = time.time()
lap_time = 0

os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
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
 
if __name__ == '__main__':

  gpsp = GpsPoller() # create the thread
  try:

    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
      
      GPIO.output(18, GPIO.LOW)
      if (GPIO.input(10) == False):
          GPIO.output(18, GPIO.HIGH)
          
      GPIO.output(17, GPIO.LOW)
      GPIO.output(27, GPIO.LOW)
      GPIO.output(22, GPIO.LOW)

      t1 = time.time()
      current_lap_time = time.time() - lap_start

      os.system('clear')
 
      # print
      # print ' GPS reading'
      # print '----------------------------------------'
      # print 'latitude    ' , gpsd.fix.latitude
      # print 'longitude   ' , gpsd.fix.longitude
      # print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      # print 'altitude (m)' , gpsd.fix.altitude
      # print 'eps         ' , gpsd.fix.eps
      # print 'epx         ' , gpsd.fix.epx
      # print 'epv         ' , gpsd.fix.epv
      # print 'ept         ' , gpsd.fix.ept
      # print 'speed (m/s) ' , gpsd.fix.speed
      # print 'climb       ' , gpsd.fix.climb
      # print 'track       ' , gpsd.fix.track
      # print 'mode        ' , gpsd.fix.mode
      # print
      # print 'sats        ' , gpsd.satellites
 
      gps_long = gpsd.fix.longitude
      gps_lat = gpsd.fix.latitude

      closest_dist = -1
      closest_point = -1


      for i in range(track_points):
          track_long = track_coords[i, 0]
          track_lat = track_coords[i, 1]
          dist_from_point = math.sqrt((gps_long - track_long)**2 + (gps_lat - track_lat)**2)
          if closest_dist < 0 or dist_from_point < closest_dist:
              closest_dist = dist_from_point
              closest_point = i
      # check to see if you are at the finish line
      if closest_point == 0:
          lap_finish = time.time()
          lap_time = lap_finish - lap_start
          # if lap time is at least 60 seconds record the lap time (otherwise
          # impossible for a full lap to have been completed
          if lap_time.total_seconds() > 60:
              print "Lap time: " + lap_time
          # reset the lap start time
          lap_start = time.time()


      print "closest point is " + str(closest_point)
      desired_range = int(track_ranges[closest_point])

      def range_1():
          # between 5-7m/s
          GPIO.output(17, GPIO.HIGH)
          GPIO.output(27, GPIO.HIGH)
          GPIO.output(22, GPIO.HIGH)
          print "range 1"

      def range_2():
          # between 7-10m/s
          GPIO.output(17, GPIO.HIGH)
          GPIO.output(27, GPIO.HIGH)
          GPIO.output(22, GPIO.LOW)
          print "range 2"

      def range_3():
          GPIO.output(17, GPIO.HIGH)
          GPIO.output(27, GPIO.LOW)
          GPIO.output(22, GPIO.HIGH)
          print "range 3"

      def range_4():
          GPIO.output(17, GPIO.HIGH)
          GPIO.output(27, GPIO.LOW)
          GPIO.output(22, GPIO.LOW)
          print "range 4"

      ranges = {
          1 : range_1,
          2 : range_2,
          3 : range_3,
          4 : range_4
      }

      ranges[desired_range]()

      t2 = time.time()
      delta = t2 - t1
      millis = int(delta*1000)
      print "milliseconds: " + str(millis)

      # return array()
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
  print "Done.\nExiting."
