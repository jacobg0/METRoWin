#
# METRo : Model of the Environment and Temperature of Roads
# METRo is Free and is proudly provided by the Government of Canada
# Copyright (C) Her Majesty The Queen in Right of Canada, Environment Canada, 2006

#  Questions or bugs report: metro@ec.gc.ca
#  METRo repository: https://framagit.org/metroprojects/metro
#  Documentation: https://framagit.org/metroprojects/metro/wikis/home
#
#
# Code contributed by:
#  Miguel Tremblay - Canadian meteorological center
#  Francois Fortin - Canadian meteorological center
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
Name:	       metro_constant
Description: The constant needed in different modules of METRo
Notes:   
"""

# platform dependent?
Infinity = 1e1000
NaN = Infinity - Infinity


fConsol = 0.1367e4
# Time step for finite element method.  In seconds
fTimeStep = 30.0
# Ratio to transform one length of snow in lenth of water
nSnowWaterRatio = 10
# Cloud constant to correct the flux
lCloudsDay = [1.0, 0.97, 0.94, 0.89, 0.85, 0.80, 0.71, 0.65, 0.33]
lCloudsNightCoeff1 = [3.79, 4.13, 4.13, 4.26, 4.38, 4.19, 4.395, 4.34, 4.51]
lCloudsNightCoeff2 = [214.7, 226.2, 234.8, 243.4, 250.7, \
                      259.2, 270.9, 280.9, 298.4]

# QA & QC for observation
nRoadTemperatureMin = -40
nRoadTemperatureHigh = 80
nSubSurRoadTmpHigh = 80
nSubSurRoadTmpMin = -40
nAirTempHigh = 50
nAirTempMin = -60
nMaxWindSpeed = 90
nHourForExpirationOfObservation = 48
nGapMinuteObservation = 240
nThreeHours = 3
nLowerPressure = 700
fNormalPressure = 1013.25 # 1 atmosphere
nUpperPressure = 1100

# Used in the combination of the observation and the forecast
#  (metro_preprocess_combine.py)
fConst = 1. / ( 4.0 * 3.6E3 )

# Used in metro_physics.py
fEps1 = 0.62194800221014 # for the function_foqst
fEps2 = 0.3780199778986
fTrpl = 273.16
fTcdk = 273.15

# Used in metro_model to define the size of npSwo, because it finally
#  goes into fortran...  
nNL = 11520

# METRo output
#  Indicates at what will be the time interval between 2 field in the roadcast
nMinutesForOutput = 20
