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
#  Viktor Tarjáni - Slovak Hydrometeological Institute
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
Sun-shadow module for METRo road model.

For given location on the Earth and for given time moments 
corrects solar flux by taking into account shielding 
of the Sun by visible horizon. 

"""

import time
import math

import sunpos
		
solar_constant = 1366.0 # [W/m^2]

def get_corrected_solar_flux(utc, S, lat, lon, horiz, m=1):
	"""Returns solar flux corrected by sun-shadow algorithm.
	
	Input:
		utc:   UTC times sequence (len M)
		S:     Input (uncorrected) solar flux sequence (len M)
		lat:   latitude of station (float)
		lon:   longitude of station (float)
		horiz: Discrete visible horizon for location (lat, lon).
			It is list of len N containing (azim, elev) pairs
		m:     Solar flux correcting method (1: basic, 2: enhanced)
	
	Output:
		S_cor: Output (corrected) solar flux sequence (len M)
	"""
	
	## Duplicate input solar flux list (for backup original values)
	S_cor = list(S)
	
	## Sort horiz list on azim values
	horiz = sorted(horiz)
	
	for i in range(len(utc)):
		## Calculate Sun apparent position (azim, elev)
		sun_azim, sun_elev = sunpos.get_sun_position(utc[i], lat, lon)
	
		## Get thes horizon elevation in the Sun direction
		horiz_elev = get_horiz_elev(sun_azim, horiz)
		
		## Check whether Sun is above (1) or below (0) visible horizon
		if (sun_elev > horiz_elev):
			sun = 1
		else:
			sun = 0
		
		## If Sun is bellow visible horizon do solar flux correction
		if (sun == 0):
			## Basic method (default): Zero solar flux 
			if (m == 1):
				S_cor[i] = 0.0
			
			## Enhanced method: 
			## Replace global solar flux with its diffuse component. 
			elif (m == 2):
				S_cor[i] = sflux_diffuse_component(S[i], sun_elev)
	
			## Unknown method: NO correction
			else:
				pass
	
	return S_cor

def sflux_diffuse_component(S_glob, sun_elev):
	"""Extract diffuse component of global solar irradiance.
	 
	Input: 
		S_glob:   Global solar irradiance
		sun_elev: Sun elevation angle [deg.]
	Output:
		S_dif: Diffuse component of global solar irradiance
	"""

	df = 1.0

	if (sun_elev > 0):
		sin_sun_elev = math.sin(sun_elev * math.pi / 180.0)
	
		## Extraterrestrial irradiance at horizontal surface 
		## (solar flux density on horizontal surface at top of atmosphere).
		S_ext = solar_constant * sin_sun_elev
	
		## Clearness index
		kt = S_glob / S_ext

		## Diffuse fraction
		df = diffuse_fraction_OH(kt)
	
	return df * S_glob

def diffuse_fraction_OH(kt):
	"""Orgill and Holland (1977) model for diffuse fraction."""
	
	if (kt < 0.35):
		df = 1 - 0.249*kt
	elif (kt > 0.75):
		df = 0.177
	else:
		df = 1.577 - 1.84*kt
	
	return df

def get_horiz_elev(azim, horiz):
	"""Returns the horizon elevation in the direction given by azim.
	
	As the horizon is discrete, interpolation is necessary to 
	get elevation for arbitrary azimuth. Fast linear interpolation 
	method is implemented which works in normalized units 
	(no searching required). However, it requires horizon (azim, elev) 
	pairs being ordered by growing azimuth values and also uniform step 
	in azimuth (i.e, neighbour azimuth values are displaced by 
	same distance), otherwise it can return a wrong elevation values. 
	Note that uniform azimuth is assumed but not checked. The azim value 
	is assumed within the maximum range 0 to 360 degree, or within the 
	range of horizon azimuth values (horizon must not cover full 360 degree 
	range) but it is not checked. In future, other (more accurate) 
	interpolation methods can be implemented allowing for horizon 
	with non-uniform azimuth step.
	
	Input:
		azim:   Azimuth in range <0, 360) deg.
		horiz:  Discrete visible horizon
	
	Output:
		elev:   Horizon elevation at azim [deg.]
	"""
	
	d_azim = horiz[1][0] - horiz[0][0]
	normalized_azim = (azim - horiz[0][0]) / d_azim
	
	## Linear interpolation
	i = int(normalized_azim)
	z = normalized_azim - i
	elev = horiz[i][1] + z * (horiz[i+1][1] - horiz[i][1])
	
	return elev

