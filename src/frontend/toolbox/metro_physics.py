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
Name:		Metro_physics.py
Description: Contains the physical equation used in metro
Notes: 
Author: Miguel Tremblay
Date: August 24th 2004
"""

import math
from math import pi
from math import sin
from math import cos

import numpy

import metro_constant
import metro_util
import metro_date
import Sun


def foqst(dTD, dPO):
    """
     Name: fodqst

     Parameters:[I] double dTD : dew point
                [I] double dPO : surface pressure
     Returns: None

     Functions Called:

     Description: Computation of the specific saturating humidity

     Notes: 

     Revision History:
     Author		Date		Reason
     Miguel Tremblay      August 24th 2004
     """
    return metro_constant.fEps1/(max(1.0, dPO/foew(dTD))\
                                 - metro_constant.fEps2)

    
def foew(dPO):
    """
     Name: foew

     Parameters: [I] double dPO : surface pressure
     Returns: None

     Functions Called: Vapour pressure

     Description: 

     Notes: 

     Revision History:
     Author		Date		Reason
     Miguel Tremblay      August 24th 2004
     """
    dDiff = dPO-metro_constant.fTrpl
    fResult =  610.78*math.exp(min(metro_util.sign(17.269,dDiff),\
                               metro_util.sign(21.875,dDiff))*\
                           abs(dDiff)/ \
                           (dPO-35.86+max(0.0,metro_util.sign(28.2,-dDiff))))
    
    return fResult


def get_sf(npCloudsOctal, npTimeHour, npForecastedTime, \
           fSunriseTimeUTC, fSunsetTimeUTC,  fLat, fLon):
    """
    Description: Return an array containing the values of SF.
        
    Parameters:
    npCloudOctal (numpy array): array of octal value representing the
     cloud coverage.
    fSunriseTimeUTC (float): sunrise time in UTC
    fSunsetTimeUT (float): sunset time in UTC
    nStartForecastTime (??):
    fLat (float): latitude of emplacement
    fLon (float): longitude of emplacement

    Return npSF (numpy array): Array containing the solar flux.
     """
    nTimeHourLength = len(npCloudsOctal)

    npSft = numpy.zeros(nTimeHourLength, dtype=numpy.float)
    npCoeff = numpy.zeros(nTimeHourLength, dtype=numpy.float)

    for i in range(len(npForecastedTime)):
        cTime = npForecastedTime[i]
        # Current hour is needed for the computation of
        # fDh in the theoritical solar flux.
        fCurrentHour = float(metro_date.get_hour(cTime))

        # Equation of time of this exact hour
        (fEot, fR0r, tDeclsc) = metro_date.get_eot(cTime, fLat)

        ###### In the night, the solar flux is null ###############
        if metro_date.in_the_dark(fCurrentHour, fSunriseTimeUTC, \
                                  fSunsetTimeUTC):
            npSft[i] = 0
        else: # Position of the sun around the earth, in radian
            fDh =  pi*(fCurrentHour/12.0 + fLon/180 - 1) + fEot
            fCosz = tDeclsc[0] + tDeclsc[1]*cos(fDh)
            npSft[i] = max(0.0, fCosz)*fR0r


    npCoeff =  -1.56e-12*npSft**4 + 5.972e-9*npSft**3 -\
                      8.364e-6*npSft**2  + 5.183e-3*npSft - 0.435
    npCoeff = numpy.where(npCoeff > 0, npCoeff, 0.0)

    # Set npCloudsPercent to be able to reference it in the
    #  numpy.where method.
    npCloudsPercentDay = npCloudsOctal
    # Correction based on the clouds
    for i in range(0,9):
        nPercentDay = metro_constant.lCloudsDay[i]
        npCloudsPercentDay = numpy.where(npCloudsOctal == i,\
                                         nPercentDay, npCloudsPercentDay)

    npCloudsPercentDay = numpy.where(npCloudsPercentDay == 0, 1.0, \
                                     npCloudsPercentDay)
    # Solar flux
    npSF = npSft * npCoeff * npCloudsPercentDay
        
    return npSF


def get_cloud_coefficient(npCloudsOctal):
    """
    Get the coefficient D1 and D2 as described in the metro article
    p.2030 corresponding to the octal values in npCloudsOctal.

    npCloudOctal (numpy array): array of octal value representing the
     cloud coverage.

    Note: Could be place in metro_physic if npCloudsOctal is given
    in arguement instead of wf_controlled_data.

    Return (npCoeff1, npCoeff2) with coefficients.
    """
    npCoeff1 = npCloudsOctal
    npCoeff2 = npCloudsOctal
    for i in range(0,9):
        fCoeff1 = metro_constant.lCloudsNightCoeff1[i]
        fCoeff2 = metro_constant.lCloudsNightCoeff2[i]
        npCoeff1 = numpy.where(npCloudsOctal == i, fCoeff1, npCoeff1)
        npCoeff2 = numpy.where(npCloudsOctal == i, fCoeff2, npCoeff2)
                 

    return (npCoeff1, npCoeff2)

def get_night_or_day(npTime, fLat, fLon):
    """
    npTime (numpy): Array of ctime(?) of the station
    fLat (float): Latitude of the station
    fLon (float): Longitude of the station

    Return npNightDay (numpy), containing '1' for day, '0' for night, for the
     the corresponding time in npTime.
    """
    ctimeFirstForecast = npTime[0]
    
    # Get the sunrise and the sunset
    nStartYear =  metro_date.get_year(ctimeFirstForecast)
    nStartMonth =   metro_date.get_month(ctimeFirstForecast)
    nStartDay =  metro_date.get_day(ctimeFirstForecast)
    cSun = Sun.Sun()
    (fSunriseTimeUTC, fSunsetTimeUTC) = cSun.sunRiseSet(\
        nStartYear, nStartMonth, nStartDay, fLon, fLat)

    npNightDay = numpy.zeros(len(npTime))

    for i in range(len(npNightDay)):
        cTimeCurrent = npTime[i]
        nCurrentHour = metro_date.get_hour(cTimeCurrent)
        nCurrentMinute =  metro_date.get_minute(cTimeCurrent)
        fCurrentHourMinute = nCurrentHour + nCurrentMinute/60.0
        if metro_date.in_the_dark(fCurrentHourMinute, fSunriseTimeUTC, \
                                  fSunsetTimeUTC):
            npNightDay[i]=1

    return npNightDay
        

