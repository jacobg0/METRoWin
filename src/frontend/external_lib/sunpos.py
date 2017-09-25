#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# METRo : Model of the Environment and Temperature of Roads
# METRo is Free and is proudly provided by the Government of Canada
# Copyright (C) Her Majesty The Queen in Right of Canada, Environment Canada, 2006
#
#  Questions or bugs report: metro@ec.gc.ca
#  METRo repository: https://framagit.org/metroprojects/metro
#  Documentation: https://framagit.org/metroprojects/metro/wikis/home
#
#
# Code contributed by:
#  Viktor Tarj·ni - Slovak Hydrometeological Institute
#  
#
#  $LastChangedDate$
#  $LastChangedRevision$
#
########################################################################
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
#
"""
Sun position algorithm.

This is a python version of the PSA algorithm developed by 
Manuel Blanco-Muriel et al. at the Plataforma Solar de Almeria. 
For further details regarding the algorithm refer to the article 
M. Blanco-Muriel, D. C. Alarcon-Padilla, T. Lopez-Moratalla, 
and M. Lara-Coira. Solar Energy 70(5):431--441 (2001).
The original algorithm is implemented in C++ and source code 
is available in electronic form at http://www.psa.es/sdg/sunpos.htm

This python version was written by Viktor Tarj√°ni at SHMU Bratislava. 
Authors of original C++ algorithm have not reviewed or endorsed this 
implementation in any way and they are not responsible for behavior 
of this code. This code is distributed under the terms of the 
GNU General Public License (GPL). 
Ownership of algorithm itself is held by authors of original code. 

Differences and changes made to original C++ code: 
1. Python implementation returns Sun elevation angle while 
   original C++ code returned Sun zenith angle.
2. The Julian date calculation in original C++ code (liAux1 and liAux2 terms) 
   contains integer divisions which however behaves differently in Python and C/C++. 
   In C/C++ integer division truncates towards zero (that is, floor 
   for positive numbers and ceil for negative numbers) while 
   in Python it always floors (see for example 
   http://python-history.blogspot.sk/2010/08/why-pythons-integer-division-floors.html) 
   The C like behaviour is restored by explicitly casting divisor 
   to float in all integer divisions, in order to force real division, 
   and then cast result to integer. This affected calculation of 
   liAux1 and liAux2 terms in Julian date calculation.
"""

import time
from math import sin, cos, tan, asin, acos, atan2

pi = 3.14159265358979323846
twopi = 2*pi
rad = (pi/180)
dEarthMeanRadius = 6371.0 # In km
dAstronomicalUnit = 149597890.0 # In km
	
def get_sun_position(utc, lat, lon):
	"""Calculate Sun apparent position (azimuth, elevation) on the sky.
	
	Input:
	  utc: UTC time
	  lat: Latitude of observing location [deg.]
	  lon: Longitude of observing location [deg.]
	
	Output:
	  dAzimuth:        Sun topocentric azimuth angle [deg.]
	  dElevationAngle: Sun topocentric elevation angle [deg.]
	"""
	
	iYear = utc.tm_year
	iMonth = utc.tm_mon
	iDay = utc.tm_mday
	dHours = float(utc.tm_hour)
	dMinutes = float(utc.tm_min)
	dSeconds = float(utc.tm_sec)

	# Calculate time of the day in UT decimal hours
	dDecimalHours = dHours + (dMinutes + dSeconds / 60.0 ) / 60.0
	
	# Calculate current Julian Day
	liAux1 = int((iMonth - 14) / float(12))
	
	liAux2 = int((1461 * (iYear + 4800 + liAux1)) / float(4)) \
		+ int((367 * (iMonth - 2 - 12*liAux1)) / float(12)) \
		- int((3 * ((iYear + 4900 + liAux1) / 100)) / float(4)) \
		+ iDay - 32075
	
	dJulianDate = float(liAux2) - 0.5 + dDecimalHours / 24.0

	
	# Calculate difference in days between the current Julian Day 
	# and JD 2451545.0, which is noon 1 January 2000 Universal Time
	dElapsedJulianDays = dJulianDate - 2451545.0

	# Calculate ecliptic coordinates (ecliptic longitude and obliquity of the 
	# ecliptic in radians but without limiting the angle to be less than 2*Pi 
	# (i.e., the result may be greater than 2*Pi)
	dOmega = 2.1429 - 0.0010394594 * dElapsedJulianDays
	dMeanLongitude = 4.8950630 + 0.017202791698 * dElapsedJulianDays # Radians
	dMeanAnomaly = 6.2400600 + 0.0172019699 * dElapsedJulianDays
	dEclipticLongitude = dMeanLongitude + 0.03341607 * sin(dMeanAnomaly) + \
			     0.00034894 * sin(2*dMeanAnomaly) - 0.0001134 -\
			     0.0000203 * sin(dOmega)
	dEclipticObliquity = 0.4090928 - 6.2140e-9 * dElapsedJulianDays +\
			     0.0000396 * cos(dOmega)

	# Calculate celestial coordinates ( right ascension and declination ) in radians 
	# but without limiting the angle to be less than 2*Pi (i.e., the result may be 
	# greater than 2*Pi)
	dSin_EclipticLongitude = sin(dEclipticLongitude)
	dY = cos(dEclipticObliquity) * dSin_EclipticLongitude
	dX = cos(dEclipticLongitude)
	dRightAscension = atan2( dY,dX )
	if (dRightAscension < 0.0):
		dRightAscension = dRightAscension + twopi
	dDeclination = asin(sin(dEclipticObliquity) * dSin_EclipticLongitude)

	# Calculate local coordinates ( azimuth and zenith angle ) in degrees
	dGreenwichMeanSiderealTime = 6.6974243242 + 0.0657098283 * dElapsedJulianDays +\
				     dDecimalHours
	dLocalMeanSiderealTime = (dGreenwichMeanSiderealTime * 15 + lon) * rad
	dHourAngle = dLocalMeanSiderealTime - dRightAscension
	dLatitudeInRadians = lat * rad
	dCos_Latitude = cos(dLatitudeInRadians)
	dSin_Latitude = sin(dLatitudeInRadians)
	dCos_HourAngle = cos(dHourAngle)
	dZenithAngle = (acos(dCos_Latitude * dCos_HourAngle * cos(dDeclination) +\
			     sin(dDeclination) * dSin_Latitude))
	dY = -sin(dHourAngle)
	dX = tan(dDeclination) * dCos_Latitude - dSin_Latitude * dCos_HourAngle
	dAzimuth = atan2(dY, dX)
	if (dAzimuth < 0.0):
		dAzimuth = dAzimuth + twopi
	dAzimuth = dAzimuth / rad
	# Parallax Correction
	dParallax = (dEarthMeanRadius / dAstronomicalUnit) * sin(dZenithAngle)
	dZenithAngle = (dZenithAngle + dParallax) / rad
	dElevationAngle = 90.0 - dZenithAngle

	return (dAzimuth, dElevationAngle)
		
if __name__ == "__main__":
	"""Selftest"""
	
	utc = time.gmtime()
	#utc = time.strptime("2012-10-09", "%Y-%m-%d")
	
	lat = 48.167803
	lon = 17.106844

	sun_azim, sun_elev = get_sun_position(utc, lat, lon)
	
	utc_iso = time.strftime("%Y-%m-%dT%H:%M:%S", utc)
	print "UTC=%s, AZIM=%3.10f, ELEV=%3.10f" % (utc_iso, sun_azim, sun_elev)
