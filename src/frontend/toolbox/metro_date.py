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
Name:	 metro_date.py
Description: Date and time functions for METRo

Notes: Time zone string used through this file correspond to the code
 used by the OS. The list can be found in the directory usr/share/zoneinfo
 on your system.
"""


import math
from math import pi
from math import sin
from math import cos

# Date import
import time
import datetime
import calendar

import os
import string

import metro_util
import metro_constant
import metro_error

_ = metro_util.init_translation('metro_date')

def parse_date_string( sDate ):
    """
    Take a date in the ISO 8601 format and return a date in ctime format.

    Parameter:
    sDate (string): date in ISO 8601 format

    Returns fDate (float): time in ctime format.
    """

    if sDate != None:
        try:
            # Strip the date in ISO up to the minute only,
            # ie. the first 16 characters
            sDate = sDate[0:16]
            tDate = time.strptime(sDate, "%Y-%m-%dT%H:%M")
            fDate = time.mktime(tDate)
        except ValueError, sError:
            sMessage = _("The following error occured when parsing the ") +\
                       _("ISO 8601 date:\n %s") % (sError)
            fDate = metro_constant.NaN
            raise metro_error.Metro_date_error(sMessage)
    else:
        sMessage = _("The following error occured when parsing a ") +\
                   _("date:\nNo date string to convert")
        raise  metro_error.Metro_date_error(sMessage)
    
    return fDate

def seconds2iso8601( fDate ):
    """
    Transform a ctime into an ISO8601 format.
    """

    # Transform ctime in tuple
    tDate = time.localtime(fDate)
    # Transform tuple in string
    sDate = time.strftime('%Y-%m-%dT%H:%MZ', tDate)
    
    return sDate

    
def get_current_date_iso8601():
    """
    Returns the current date in iso8601 format
    """
    
    fCurrentTime  = time.time()
    sCurrentTime = seconds2iso8601(fCurrentTime)
    return sCurrentTime

def time_zone_convert(tm, source_zone, dest_zone):
    """
    Convert a broken-down time (time.struct_time or tuple) from
    one named time zone to another.
    """
    old_zone = os.environ['TZ']
    try:
        os.environ['TZ'] = source_zone
        time.tzset()
        stamp = time.mktime(tm)

        os.environ['TZ'] = dest_zone
        time.tzset()
        return time.mktime(time.localtime(stamp))
    finally:
        os.environ['TZ'] = old_zone
        time.tzset()

def is_daylight_saving_time(fTime, sTime_zone):
    bRslt = False
    tmp_time = get_struct_time(fTime, sTime_zone)
    if( tmp_time[8] == 1 ):
        bRslt = True
    return bRslt

def get_year( fTime, sTime_zone="UTC" ):
    tmp_time = get_struct_time(fTime, sTime_zone)
    return tmp_time[0]

def get_month( fTime, sTime_zone="UTC" ):
    tmp_time = get_struct_time(fTime, sTime_zone)
    return tmp_time[1]

def get_day( fTime, sTime_zone="UTC" ):
    tmp_time = get_struct_time(fTime, sTime_zone)
    return tmp_time[2]

def get_hour( fTime, sTime_zone="UTC" ):
    tmp_time = get_struct_time(fTime, sTime_zone)
    return tmp_time[3]

def get_minute( fTime, sTime_zone="UTC" ):
    tmp_time = get_struct_time(fTime, sTime_zone)
    return tmp_time[4]

def get_system_tz():
    return os.environ['TZ']

def get_struct_time( fTime, sTime_zone="UTC" ):
    sOld_zone = os.environ['TZ']
    rslt = (-1,-1,-1,-1,-1,-1,-1,-1,-1)

    try:
        os.environ['TZ'] = sTime_zone
        time.tzset()
        rslt = time.localtime(fTime)
    finally:
        os.environ['TZ'] = sOld_zone
        time.tzset()

    return rslt


def get_short_time_zone(tm, sTime_zone):
    """
    Get first part of time zone spec ( before first comma ) 
     see http://www.qnx.com/developers/docs/momentics621_docs/neutrino/ ...
         lib_ref/global.html#TheTZEnvironmentVariable
    
    ex: EST5EDT4,M4.1.0/02:00:00,M10.5.0/02:00:00 ->  EST5EDT4
    """
    if ',' in sTime_zone:
        lTz = string.split(sTime_zone,',')
        sTime_zone = lTz[0]
        
    # extract time zone letter
    #
    # ex: EST5EDT4 -> ESTEDT
    sTz_letter = ""
    for letter in sTime_zone:
        if letter.isalpha():
            sTz_letter = sTz_letter + letter

    if is_daylight_saving_time(tm, sTime_zone):
        return sTz_letter[-3:]
    else:
        return sTz_letter[:3]


def get_elapsed_time(ftime1, ftime2, sTimeZone="UTC", sUnit="hours"):
    """
    Return the difference between the 2 ctime: ftime1 - ftime2.

    Parameters.
    ftime1 (float): ctime for end time.
    ftime2 (float): ctime for start time.
    sTimeZone (string): time zone code. See 'Note' in the general comment
    of metro_util.
    sUnit (string): Precision of which this function should round. Possible
    choices are in ['hours', 'days', 'seconds']

    Return nResult (int): Values rounded to sUnit.
    """
    
    # Transform the ctime in the datetime.datetime class
    cTime1 = datetime.datetime(get_year(ftime1,sTimeZone), \
                               get_month(ftime1,sTimeZone), \
                               get_day(ftime1,sTimeZone), \
                               get_hour(ftime1,sTimeZone), \
                               get_minute(ftime1,sTimeZone))
    cTime2 = datetime.datetime(get_year(ftime2,sTimeZone),\
                               get_month(ftime2,sTimeZone), \
                               get_day(ftime2,sTimeZone), \
                               get_hour(ftime2,sTimeZone), \
                               get_minute(ftime2,sTimeZone))
        
    # Get the timedelta object from the substraction.
    cTimeDifference = cTime1-cTime2
    if(sUnit == "hours"):
        nNbrHours = cTimeDifference.days*24.0+cTimeDifference.seconds/3600.0
        return nNbrHours
    elif(sUnit == "days"):
        nNbrDays = cTimeDifference.days \
                   + cTimeDifference.seconds/3600.0*1/24.0
        return nNbrDays
    elif(sUnit == "seconds"):
        nNbrSeconds = ftime1-ftime2
        return nNbrSeconds
    else:
        sInvalidParameterError =_("Invalid criteria in get_elapsed_time: sUnit = %s")\
                                     % (sUnit)
        raise  metro_error.Metro_date_error(sInvalidParameterError)


def tranform_decimal_hour_in_minutes(fTimeHour):
    """
    Return an array containing the hour, the minutes and the secondes,
    respectively.

    Parameter:
    fTimeHour (float): ctime to be transformed

    Return a tuple: (nHour, nMinute, nSecond)
    """
    # Extract decimal from integer part
    tModHour = math.modf(fTimeHour)
    nHour = int(tModHour[1])
    fDecimalHour = tModHour[0]
    # Transform decimal in minutes
    fMinute = fDecimalHour*60
    # Again, extract the decimal and the integer part
    tModMinute = math.modf(fMinute)
    nMinute = int(tModMinute[1])
    fDecimalMinute = tModMinute[0]
    # Transform decimal in seconds
    fSecond = fDecimalMinute*60    
    # Again, extract the decimal and the integer part
    tModSecond = math.modf(fSecond)
    nSecond = int(tModSecond[1])

    return (nHour, nMinute, nSecond)

def get_iso_8601(nYear, nMonth, nDay, nHour=0, nMinute=0, nSecond=0):
    """
    Convert numbers of date in the iso 8601 format
    We assume UTC time zone.
    """

    sYear = str_to_at_least_two_digits(nYear)
    sMonth = str_to_at_least_two_digits(nMonth)
    sDay = str_to_at_least_two_digits(nDay)

    if (nHour == nMinute == nSecond == 0):
        sIso = sYear + '-' + sMonth + '-' + sDay
    else:
        sHour = str_to_at_least_two_digits(nHour)
        sMinute = str_to_at_least_two_digits(nMinute)
        sSecond = str_to_at_least_two_digits(nSecond)
        sIso = sYear + '-' + sMonth + '-' + sDay+ 'T' +\
           sHour + ':' + sMinute + ':' + sSecond + 'Z'

    return sIso

def str_to_at_least_two_digits(nNumber):
    """
    Take an int and return '01' instead of '1'.
    There must be a 'regular' way to do it in python but
    it takes longer to find it than to write it.
    """     
    sRes = str(nNumber)
    if len(sRes) < 2:
        sRes = '0'+sRes

    return sRes


def in_the_dark(nCurrentTime, fSunrise, fSunset):
    """
    Sometimes, value returned by Sun.py are over 24. Since
    the time of day is needed with modulo 24, a special check must be
    performed. See https://gna.org/bugs/?8277 for more details.
        
    Parameters:
    nCurrentTime (int): Current time. In [0,24]
    fSunrise (float): Sunrise time as returned by Sun.py. Value could be > 24.
    fSunset (float): Sunset time as returned by Sun.py.  Value could be > 24.
                      
    Returns bDark (bool): True if between fSunset and fSunrise.
                          False if between fSunrise and fSunset.

    """
    bDark=False
        
    if ((fSunset%24 > fSunrise%24) and \
        (nCurrentTime < fSunrise or \
         nCurrentTime > fSunset)) or \
         (not(fSunset%24 > fSunrise%24) and \
          (nCurrentTime > fSunset%24 and \
           nCurrentTime < fSunrise%24)):
        bDark=True

    return bDark
        

def get_eot(fTime, fLat):
    """
    Subroutine computing the part of the equation of time
    needed in the computing of the theoritical solar flux
    Correction originating of the CMC GEM model.
    
    Parameters:
    fTime (float): cTime of the beginning of the forecast
    fLat (float): latitude of emplacement

    Returns: tuple (double fEot, double fR0r, tuple tDeclsc)
             dEot: Correction for the equation of time 
             dR0r: Corrected solar constant for the equation of time
             tDeclsc: Declinaison

    """
    # Convert ctime to python tuple for time.
    # see http://www.python.org/doc/current/lib/module-time.html
    tDate = time.gmtime(fTime)
    # Julian date is the 7th argument
    fJulianDate = tDate[7] + tDate[3]/24.0
    # Check if it is a leap year
    if(calendar.isleap(tDate[0])):
        fDivide = 366.0
    else:
        fDivide = 365.0
    # Correction for "equation of time"
    fA = fJulianDate/fDivide*2*pi
    fR0r = solcons(fA)*metro_constant.fConsol
    fRdecl = 0.412*cos((fJulianDate+10.0)*2.0*pi/fDivide-pi)
    fDeclsc1 = sin(fLat*pi/180.0)*sin(fRdecl)
    fDeclsc2 = cos(fLat*pi/180.0)*cos(fRdecl)
    tDeclsc = (fDeclsc1, fDeclsc2)
    # in minutes
    fEot = 0.002733 -7.343*sin(fA)+ .5519*cos(fA) -9.47*sin(2.0*fA) \
                -3.02*cos(2.0*fA) -0.3289*sin(3.*fA) -0.07581*cos(3.0*fA) \
                -0.1935*sin(4.0*fA) -0.1245*cos(4.0*fA)
    # Express in fraction of hour
    fEot = fEot/60.0
    # Express in radians
    fEot = fEot*15*pi/180.0

    return (fEot, fR0r, tDeclsc)


def solcons(dAlf):
    """
    Statement function that calculates the variation of the
    solar constant as a function of the julian day. (dAlf, in radians)
    
    Parameters:
    dAlf (double) : Solar constant to correct the excentricity
        
    Returns dVar (double : Variation of the solar constant
    """
        
    dVar = 1.0/(1.0-9.464e-4*sin(dAlf)-0.01671*cos(dAlf)- \
                + 1.489e-4*cos(2.0*dAlf)-2.917e-5*sin(3.0*dAlf)- \
                + 3.438e-4*cos(4.0*dAlf))**2
    return dVar

