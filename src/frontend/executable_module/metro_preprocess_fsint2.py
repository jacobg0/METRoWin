# -*- coding: UTF8 -*-
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
Name:		Metro_preprocess_fsint2
Description: Subroutine correcting the incident solar flux
              to take the sunrise/sunset into account.

Notes: Take a special care with the difference between the interpolated
       values and the raw one. The search for the sunrise/sunset
       is performed on the raw values of SF. The number of time step
       is performed on the raw values of time. The number of time steps
       should normally correspond to the interpolated intervals.
"""

from metro_preprocess import Metro_preprocess

import time
import calendar
from math import pi
from math import sin
from math import cos
import numpy

import metro_logger
import metro_config
import metro_preprocess_sunshadw 
import Sun
from toolbox import metro_physics
from toolbox import metro_util
from toolbox import metro_date
from data_module import metro_data


_ = metro_util.init_translation('metro_preprocess_fsint2')


class Metro_preprocess_fsint2(Metro_preprocess):

    ##
    # Class attribute
    ##
    fLat = 0 # Latitude of the station
    fLon = 0 # Longitude of the station

    # Date
    nStartDay = None
    nStartMonth = None
    nStartYear = None
    fSunrise = None
    fSunset = None

    npAzim = None
    npElev = None

#####################################################
    def start(self):
        Metro_preprocess.start(self)
        # Get the attribute of the class
        
        pForecast = self.get_infdata_reference('FORECAST')
        forecast_data = pForecast.get_data_collection()
        pStation = self.get_infdata_reference('STATION')
        station_data = pStation.get_data()
	
        if self.infdata_exist('HORIZON'):
            pHorizon = self.get_infdata_reference('HORIZON')
            horizon_data = pHorizon.get_data()
            if horizon_data != None:
                self.npAzim = horizon_data.get_matrix_col('AZIMUTH')
                self.npElev = horizon_data.get_matrix_col('ELEVATION')

                # Verification if the array has an monotone and
                #  regular incrementation steps
                if not metro_util.is_array_uniform(self.npAzim):
                    sMessage = _("Azimuth data in station configuration file ") +\
                               _("is not ordered by equal growing azimuths. ")+\
                               _("Please correct this or remove the option --enable-sunshadow")
                    metro_logger.print_message(metro_logger.LOGGER_MSG_STOP,\
                                               sMessage).Metro_util_error(sMessage)

        self.__set_attribute(forecast_data.get_controlled_data(), \
                             forecast_data.get_interpolated_data(), \
                             station_data)
        self.__print_info()
        # SF
        self.__set_sf(forecast_data.get_controlled_data(),\
                     forecast_data.get_interpolated_data() )
        # IR
        self.__set_ir(forecast_data.get_controlled_data(),\
                     forecast_data.get_interpolated_data() )
        self.__set_cc(forecast_data.get_controlled_data(),\
                      forecast_data.get_interpolated_data() )
        pForecast.set_data_collection(forecast_data)
        pStation.set_data(station_data)        


    def __set_attribute(self, wf_controlled_data,
                        wf_interpolated_data,
                        station_data):
        """
        Set the attributes needed by this class.
        
        Parameters:
        wf_controlled_data (metro_data) : controlled data.  Read-only
        wf_interpolated_data (metro_data) : container of the
        interpolated data.

        Returns: None
        """
        # Lat & Lon
        self.fLat = station_data.get_latitude()
        self.fLon = station_data.get_longitude()
        self.__set_sunrise_sunset(wf_controlled_data)

    def __print_info(self):
        """
        Print the information about the sunrise/sunset computed for this
        day and emplacement.
        """
        if self.fLon < 0:
            sLon = 'W'
        else:
            sLon = 'E'
        if self.fLat > 0:
            sLat = 'N'
        else:
            sLat = 'S'

        tSunset = metro_date.tranform_decimal_hour_in_minutes(\
            self.fSunset)
        tSunrise = metro_date.tranform_decimal_hour_in_minutes(\
            self.fSunrise)      
        sMessage = _("For the date %d-%d-%d,\n") % \
                   ((self.nStartDay,self.nStartMonth,self.nStartYear)) +\
                   _("at the latitude %0.2f ") %(abs(round(self.fLat,2))) + sLat +\
                   _(" and longitude %0.2f ") %(abs(round(self.fLon,2))) + sLon +\
                   _("\nsunrise is at %d:%d:%d UTC\n") \
                   % ((tSunrise[0], tSunrise[1], tSunrise[2])) +\
                   _("sunset  is at %d:%d:%d UTC") \
                  % ((tSunset[0], tSunset[1], tSunset[2])) 
        metro_logger.print_message(metro_logger.LOGGER_MSG_INFORMATIVE,\
                                  sMessage)

 

    def __set_ir(self, wf_controlled_data, wf_interpolated_data):
        """
        Set the theoretical infrared flux.
           
        Parameters:
        wf_controlled_data (metro_data) : controlled data. Read-only
        """
        npTime = wf_controlled_data.get_matrix_col('Time') 

        # Only interpolate if IR is given
        if  metro_config.get_value('IR'):
            npIR = wf_controlled_data.get_matrix_col('IR')
            npIR2 = metro_util.interpolate(npTime, npIR)
            wf_interpolated_data.append_matrix_col('IR', npIR2)
            return
        
        npCloudOctal = wf_controlled_data.get_matrix_col('CC')
        (npCoeff1, npCoeff2) = metro_physics.get_cloud_coefficient(npCloudOctal)
        npAT = wf_controlled_data.get_matrix_col('AT')
        npIR = npCoeff1*npAT+npCoeff2
        npIR2 = metro_util.interpolate(npTime, npIR)
        wf_controlled_data.append_matrix_col('IR', npIR)
        wf_interpolated_data.append_matrix_col('IR', npIR2)

    def __set_sf(self, wf_controlled_data, wf_interpolated_data):
        """
        Set the theoretical solar flux.
           
        Parameters:
        wf_controlled_data (metro_data) : controlled data. Read-only
        """
        npTime = wf_controlled_data.get_matrix_col('Time') 

        # Only interpolate if SF is given
        if  metro_config.get_value('SF'):
            npSF = wf_controlled_data.get_matrix_col('SF')
            npSF2 = metro_util.interpolate(npTime, npSF)
            if ((self.infdata_exist('HORIZON')) and (self.npAzim != None)):
	    	npFT2 = wf_interpolated_data.get_matrix_col('FORECAST_TIME')
		tDate2 = [time.gmtime(x) for x in npFT2]
		sunshadw_method = metro_config.get_value('SUNSHADOW_METHOD')
	    	npSF2 = metro_preprocess_sunshadw.\
                        get_corrected_solar_flux(tDate2, npSF2, \
                                                 self.fLat, self.fLon,\
                                                 zip(self.npAzim, self.npElev),\
                                                 m=sunshadw_method)

            wf_interpolated_data.append_matrix_col('SF', npSF2)
	    return
        
        # Get data
        npCloudOctal = wf_controlled_data.get_matrix_col('CC')
        npTimeHour =  wf_controlled_data.get_matrix_col('Hour')
        npForecastedTime = wf_controlled_data.\
                             get_matrix_col('FORECAST_TIME')
        fStartForecastTime =npForecastedTime [0]
        # Get solar fluxes for this cloud cover for this specific day
        npSF  = metro_physics.get_sf(npCloudOctal, npTimeHour, \
                                    npForecastedTime,\
                                    self.fSunrise, self.fSunset,\
                                    self.fLat, self.fLon)

	npSF2  = metro_util.interpolate(npTime, npSF)

        if ((self.infdata_exist('HORIZON')) and (self.npAzim != None)):
	    npFT2 = wf_interpolated_data.get_matrix_col('FORECAST_TIME')
	    tDate2 = [time.gmtime(x) for x in npFT2]
	    sunshadw_method = metro_config.get_value('SUNSHADOW_METHOD')
	    npSF2 = metro_preprocess_sunshadw.\
                    get_corrected_solar_flux(tDate2, npSF2, \
                                             self.fLat, self.fLon,\
                                             zip(self.npAzim, self.npElev),\
                                             m=sunshadw_method)

        wf_controlled_data.append_matrix_col('SF', npSF)
        wf_interpolated_data.append_matrix_col('SF',  npSF2)


    def __set_cc(self, wf_controlled_data, wf_interpolated_data):
        """
        In the case that SF and IR are given, put the values of CC to -1.
           
        Parameters:
        wf_controlled_data (metro_data) : controlled data. Read-only
        """
        if metro_config.get_value('SF') and metro_config.get_value('IR'):
            npTime = wf_controlled_data.get_matrix_col('Time') 
            npCloudOctal = wf_controlled_data.get_matrix_col('CC')
            nLength = len(npCloudOctal)
            npCloud = numpy.ones(nLength) * (-1)
            npCloud2  = metro_util.interpolate(npTime, npCloud)
            
            wf_controlled_data.set_matrix_col('CC', npCloud)
            wf_interpolated_data.set_matrix_col('CC',  npCloud2)
        

    def __set_sunrise_sunset(self, wf_controlled_data):
        """
        Description: Get the value of sunrise/sunset for the first
        day of forecast.
   
        Parameters:
        wf_controlled_data (metro_data) : controlled data. Read-only
        
        Set the attribute for sunrise/sunset
        """
        ctimeFirstForecast = wf_controlled_data.get_matrix_col\
                             ('FORECAST_TIME')[0]
        # Get the sunrise and the sunset
        self.nStartYear =  metro_date.get_year(ctimeFirstForecast)
        self.nStartMonth =   metro_date.get_month(ctimeFirstForecast)
        self.nStartDay =  metro_date.get_day(ctimeFirstForecast)
        cSun = Sun.Sun()
        (fSunriseTimeUTC, fSunsetTimeUTC) = cSun.sunRiseSet(\
           self.nStartYear, self.nStartMonth, self.nStartDay,\
           self.fLon, self.fLat)

        self.fSunrise = fSunriseTimeUTC
        self.fSunset = fSunsetTimeUTC


    
