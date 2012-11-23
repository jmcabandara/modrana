# -*- coding: utf-8 -*-
# supplies position info from the GPS daemon
#---------------------------------------------------------------------------
# Copyright 2007-2008, Oliver White
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#---------------------------------------------------------------------------
from __future__ import with_statement # for python 2.5
from modules.base_module import ranaModule
from time import *
from core import gs

def getModule(m,d,i):
  return Location(m,d,i)

class Location(ranaModule):
  """Supplies position info from a position source"""
  def __init__(self, m, d, i):
    ranaModule.__init__(self, m, d, i)
    self.tt = 0
    self.connected = False
    self.set('speed', None)
    self.set('metersPerSecSpeed', None)
    self.set('bearing', None)
    self.set('elevation', None)
    self.status = "Unknown"
    self.enabled = False
    self.provider = None

    # check if the device handles location by itself
    if not self.modrana.dmod.handlesLocation():
      method = self.modrana.dmod.getLocationType()
      if method == "qt_mobility":
        print(" @ location: using Qt Mobility")
        import qt_mobility
        self.provider = qt_mobility.QtMobility(self)
      else: # GPSD
        print(" @ location: using GPSD")
        import gps_daemon
        self.provider = gps_daemon.GPSD(self)

  def firstTime(self):
    # periodic screen redraw
    if self.modrana.dmod.getLocationType() in ("gpsd", "liblocation"):
      print "location: starting GPSD 1 second timer"
      # start screen update 1 per second screen update
      # TODO: event based redrawing
      cron = self.m.get('cron', None)
      if cron:
        cron.addTimeout(self._screenUpdateCB, 1000, self, "screen and GPSD update")

    # start location if enabled in options
    if self.get('GPSEnabled', True): # is GPS enabled ?
      self.startLocation()

  def _screenUpdateCB(self):
    """update the screen and also GPSD location if enabled
    TODO: more efficient screen updates"""
#    print("location: screen update")

    # only try to update position info if
    # location is enabled
    if self.enabled and self.provider:
      self.provider._updateGPSD()

      fix = self.provider.getFix()
      if fix:
        self.updatePosition(fix)
      else:
        print("location: fix not valid")
        print(fix)

      # forced screen update is only needed by the GTK GUI
      """
      the location update method which might run asynchronously in the
      device module also sends redraw requests
      -> no need to send a new one if there is already one pending
      --> there would not be a change position anyway until next the fix
      -> surplus redraw requests are actually harmful with map rotation enabled
      NOTE: this currently applies only to the GTK GUI
      """
    if gs.GUIString == "GTK":
      # make sure the screen is updated at least once per second
      sFromLastRequest = time() - self.modrana.gui.getLastFullRedrawRequest()
      if sFromLastRequest > 0.85:
        self.set('needRedraw', True)

  def handleMessage(self, message, type, args):
    if message == "setPosLatLon" and type == "ml":
      if args and len(args) == 2:
        lat = float(args[0])
        lon = float(args[1])
        print "gps:setting current position to: %f,%f" % (lat,lon)
        self.set('pos',(lat,lon))
    elif message == "checkGPSEnabled":
        state = self.get('GPSEnabled', True)
        if state == True:
          self.startLocation()
        elif state == False:
          self.stopLocation()
    elif message == "gpsdCheckVerboseDebugEnabled":
      self._checkVerbose()

  def updatePosition(self, fix):
    """
    update position info with new Fix data
    """
    if fix.position is None:
      # set fix class to 0 - nothing yet
      self.set('fix', 0)
      # wait for valid data
      return
    (lat,lon) = fix.position
    fixClass = 2 # 2D data

    # position
    self.set('pos', (lat,lon))
    self.set('pos_source', 'GPSD')
    # bearing
    self.set('bearing', float(fix.bearing))
    # speed
#    if speed != None:
#      # normal gpsd reports speed in knots per second
#      gpsdSpeed = self.get('gpsdSpeedUnit', 'knotsPerSecond')
#      if gpsdSpeed == 'knotsPerSecond':
#        # convert to meters per second
#        speed = float(speed) * 0.514444444444444 # knots/sec to m/sec
    if fix.speed is not None:
      self.set('metersPerSecSpeed', fix.speed)
      self.set('speed', fix.speed * 3.6)
    else:
      self.set('metersPerSecSpeed', None)
      self.set('speed', None)
      # elevation
    if fix.altitude is not None:
      self.set('elevation', fix.altitude)
      fixClass = 3
    else:
      self.set('elevation', None)

    # set fix class
    # NOTE:
    # 0 - no sats
    # 1 - no fix
    # 2 - 2D
    # 3 - 3D
    self.set("fix", fixClass)


    """always set this key to current epoch once the location is updated
    so that modules can watch it and react on position updates"""
    self.set('locationUpdated', time())

  def getFix(self):
    return self.provider.getFix()

  def startLocation(self):
    """start location - device based or gpsd"""
    if not self.enabled:
      print "location: enabling location"
      if self.modrana.dmod.handlesLocation():
        self.modrana.dmod.startLocation()
      else:
        self.provider.start()
      self.enabled = True
    else:
      print('location: location already enabled')

  def stopLocation(self):
    """stop location - device based or gpsd"""
    print "location: disabling location"
    if self.modrana.dmod.handlesLocation():
      self.modrana.dmod.stopLocation()
    else:
      self.provider.stop()
    self.enabled = False

  def shutdown(self):
    try:
      self.stopLocation()
    except Exception, e:
      print "location: stopping location failed", e
