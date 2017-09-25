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
Name:	       Metro_preprocess_interpol_forecast
Description: Interpolation of data in order to be at every 30 seconds.
  Solar flux is a special case.

Note: Solar and infrared flux are interpolated in metro_preprocess_fsint2.py
 when they are given in the atmospheric forecast file.

 TODO MT: Do the update in order that the array are 0-based
 Auteur: Miguel Tremblay
 Date: August 2nd 2004
"""

from metro_preprocess import Metro_preprocess

import metro_config
import time
import numpy

from toolbox import metro_util
from toolbox import metro_date
from toolbox import metro_constant

##
# Class attributes
##
npTime = None # Array representing the time in seconds.


class Metro_preprocess_interpol_forecast(Metro_preprocess):

    def start(self):
        Metro_preprocess.start(self)

        pForecast = self.get_infdata_reference('FORECAST')
        forecast_data = pForecast.get_data_collection()

        self.__set_attribute(forecast_data.get_original_data(),\
                             forecast_data.get_controlled_data())
        self.__interpolate_FT(forecast_data.get_original_data(), \
                              forecast_data.get_controlled_data(), \
                              forecast_data.get_interpolated_data() )
        self.__interpolate_AT(forecast_data.get_original_data(), \
                              forecast_data.get_interpolated_data() )
        self.__interpolate_QP(forecast_data.get_original_data(), \
                              forecast_data.get_interpolated_data() )
        self.__interpolate_WS(forecast_data.get_original_data(), \
                              forecast_data.get_interpolated_data() )
        self.__interpolate_TD(forecast_data.get_original_data(), \
                              forecast_data.get_interpolated_data() )
        self.__interpolate_AP(forecast_data.get_original_data(), \
                              forecast_data.get_interpolated_data() )
        self.__interpolate_PI(forecast_data.get_original_data(), \
                              forecast_data.get_interpolated_data() )
        self.__interpolate_CC(forecast_data.get_original_data(), \
                              forecast_data.get_interpolated_data() )
        self.__interpolate_FA(forecast_data.get_original_data(), \
                              forecast_data.get_interpolated_data() )

        pForecast.set_data_collection(forecast_data)


    def __set_attribute(self, wf_original_data, wf_controlled_data):
        """
        Name: __set_attribute

        Parameters: metro_data original_data : original forecast data

        Returns: None

        Functions Called: forecast_data.get_matrix_col
                          numpy.arange,                  
                          metro_date.get_hour
                          wf_controlled_data.append_matrix_col

        Description: Set the npTime array to span all the values
                     of the input matrix. The input must be at every hour.

        Notes: The initialization of the processed_data is made here.

        Revision History:
        Author		Date		Reason
        Miguel Tremblay      July 12th 2004
        """
        
        #  Used in fsint2.
        npFT = wf_original_data.get_matrix_col('FORECAST_TIME')

        nHourStart = int(metro_date.get_hour(npFT[0]))
        nbrHours = metro_date.get_elapsed_time(npFT[-1], \
                                               npFT[0]) + 1
        self.npTime = numpy.arange(0, nbrHours, dtype=numpy.float)*3600 

        npTimeAtHours = numpy.arange(0,nbrHours, dtype=numpy.float) + nHourStart
        wf_controlled_data.append_matrix_col('Hour', npTimeAtHours)



    def __interpolate_FT(self, wf_original_data, wf_controlled_data, \
                         wf_interpolated_data):
        """
        Name: __interpolate_FT

        Parameters:[I] metro_data wf_original_data : original data.  Read-only
                   [I] metro_data wf_processed_data : container of the
                        interpolated data.

        Returns: None

        Functions Called: metro_util.interpolate,
                         metro_data.get_matrix_col
                         metro_data.append_matrix_col

         Description: Interpolate forcast time.
                      Copy self.npTime in wf_processed_data 'FORECAST_TIME'

         Revision History:
         Author		Date		Reason
         Miguel Tremblay      July 13th 2004
         """
        
        npFT = wf_original_data.get_matrix_col('FORECAST_TIME')
        npFT = metro_util.interpolate(self.npTime, npFT)
                                      
        wf_interpolated_data.append_matrix_col('FORECAST_TIME', npFT)
        
        nHourStart = int(metro_date.get_hour(npFT[0]))
        # A strange trick of copying the NumPy array locally to set it in the matrix
        #  must be done (if I remember well), because otherwhise the array are not included
        #  in the matrix. It might be because NumPy made use of pointers.
        npTime = self.npTime
        wf_controlled_data.append_matrix_col('Time', npTime)
        npTime = metro_util.interpolate(self.npTime, npTime)
        npTime = (npTime+30)/3600+nHourStart
        wf_interpolated_data.append_matrix_col('Time', npTime)



    # Air temperature
    def __interpolate_AT(self, wf_originpl_data, wf_interpolated_data):
        """
        Name: __interpolate_AT
        
        Parameters:[I] metro_data wf_originpl_data : originpl data.  Read-only
                   [I] metro_data wf_processed_data : container of the interpolated
                    data.

        Returns: None

        Functions Called: metro_util.interpolate,
                          metro_data.get_matrix_col
                          metro_data.append_matrix_col

        Description: Does the interpolation of the air temperature


        Revision History:
        Author		Date		Reason
        Miguel Tremblay      July 12th 2004
        """
        
        npAT = wf_originpl_data.get_matrix_col('AT')
        npAT = metro_util.interpolate(self.npTime, npAT)
        wf_interpolated_data.append_matrix_col('AT', npAT)

        
    def __interpolate_QP(self, wf_originpl_data, wf_interpolated_data):
        """
        Name: __interpolate_QP

        Parameters:[I] metro_data wf_originpl_data : originpl data.  Read-only
                   [I] metro_data wf_interpolated_data : container of the interpolated
                   data.

        Returns: None

        Functions Called: metro_util.interpolate, shift_right
                          metro_data.get_matrix_col
                          metro_data.append_matrix_col


        Description: Add the rain (in mm.) and the snow (in cm.) and store it
                      in RA. Since 1 cm. is, roughly, 1 mm. of water, the sum
                      is considerated in mm.


        Revision History:
        Author		Date		Reason
        Miguel Tremblay      July 12th 2004
        """
        npRA = wf_originpl_data.get_matrix_col('RA')
        npSN = wf_originpl_data.get_matrix_col('SN')
        npQP = npSN/10*metro_constant.nSnowWaterRatio \
               + npRA

        # Patch because of the -99 at the end of the forecast
        fMax = npQP.max()
        npQP = numpy.where(npQP < 0, fMax, npQP)

        # Compute the amount fell at each time step
        npQP = npQP - metro_util.shift_right(npQP, 0)
        npSN = npSN - metro_util.shift_right(npSN, 0)
        npRA = npRA - metro_util.shift_right(npRA, 0)

        # Interpolate these values at each time step
        npQP = metro_util.interpolate(self.npTime, npQP)
        npSN = metro_util.interpolate(self.npTime, npSN)
        npRA = metro_util.interpolate(self.npTime, npRA)

        # Shift all the values to have them started at the right time
        npQP =  metro_util.shift_left(npQP, 0)
        npSN =  metro_util.shift_left(npSN, 0)
        npRA =  metro_util.shift_left(npRA, 0)

        npQP = npQP *10e-4 # Set it in meter
        npQP = npQP / 3600.0 # Convert by second
        npQP = numpy.where(npQP < 0, 0, npQP)

        wf_interpolated_data.append_matrix_col('QP', npQP)
        wf_interpolated_data.append_matrix_col('SN', npSN)
        wf_interpolated_data.append_matrix_col('RA', npRA)
        

    # Wind velocity
    def __interpolate_WS(self, wf_originpl_data, wf_interpolated_data):
        """
        Name: __interpolate_WS

        Parameters:[I] metro_data wf_originpl_data : originpl data.  Read-only
                   [I] metro_data wf_interpolated_data : container of the
                       interpolated data.

        Returns: None

        Functions Called: metro_util.interpolate,
                          metro_data.get_matrix_col
                          metro_data.append_matrix_col


        Description: Interpolate wind speed.  Wind is in km/h and is converted in
                     m/s by the product with 0.2777777


        Revision History:
        Author		Date		Reason
        Miguel Tremblay      July 12th 2004
        """
        npWS = wf_originpl_data.get_matrix_col('WS')*0.2777777
        npWS = metro_util.interpolate(self.npTime, npWS)
        wf_interpolated_data.append_matrix_col('WS', npWS)
        

    # Dew point
    def __interpolate_TD(self, wf_originpl_data, wf_interpolated_data):
        """
        Name: __interpolate_TD

        Parameters:[I] metro_data wf_originpl_data : originpl data.  Read-only
                   [I] metro_data wf_interpolated_data : container of the interpolated
                   data.

        Returns: None

        Functions Called: metro_util.interpolate,
                          metro_data.get_matrix_col
                          metro_data.append_matrix_col


        Description: Interpolate the dew point.


        Revision History:
        Author		Date		Reason
        Miguel Tremblay      July 12th 2004
        """
        npTD = wf_originpl_data.get_matrix_col('TD')
        npTD = metro_util.interpolate(self.npTime, npTD)
        wf_interpolated_data.append_matrix_col('TD', npTD)

        
    # Pressure
    def __interpolate_AP(self, wf_originpl_data, wf_interpolated_data):
        """
        Name: __interpolate_AP

        Parameters:[I] metro_data wf_originpl_data : originpl data.  Read-only
                   [I] metro_data wf_interpolated_data : container of the interpolated
                   data.

        Returns: None

        Functions Called: metro_util.interpolate,
                          metro_data.get_matrix_col
                          metro_data.append_matrix_col


         Description: Interpolate the surface pressure. Pressure in in hectopascal.


         Revision History:
         Author		Date		Reason
         Miguel Tremblay      July 12th 2004
         """
        npAP = wf_originpl_data.get_matrix_col('AP')
        
        # Replace invalid date by the normal pressure (1013.25 mb)
        npAP = numpy.where(npAP < metro_constant.nLowerPressure,\
                              metro_constant.fNormalPressure,  npAP)
        npAP = numpy.where(npAP > metro_constant.nUpperPressure,\
                              metro_constant.fNormalPressure,  npAP)
        
        # Convert it in pascals.
        npAP = npAP*100
        npAP = metro_util.interpolate(self.npTime, npAP)
        wf_interpolated_data.append_matrix_col('AP', npAP)


    # Type of precipitation
    def __interpolate_PI(self, wf_originpl_data, wf_interpolated_data):
        """
        Name: __interpolate_PI

        Parameters:[I] metro_data wf_originpl_data : originpl data.  Read-only
                   [I] metro_data wf_interpolated_data : container of the interpolated
                   data.

        Returns: None

        Functions Called: metro_util.interpolate,
                          metro_data.get_matrix_col
                          metro_data.append_matrix_col
                          numpy.where, around

        Description: Interpolate the type of precipitation.  The nearest neighbor is
                      is used.


        Revision History:
        Author		Date		Reason
        Miguel Tremblay      July 15th 2004
        """
        npRA = wf_originpl_data.get_matrix_col('RA')
        npSN = wf_originpl_data.get_matrix_col('SN')
        npAT = wf_originpl_data.get_matrix_col('AT')
        # Replace the last value if they are not good
        if npRA[len(npRA)-1] < 0:
            npRA[len(npRA)-1] = npRA.max()
        if npSN[len(npSN)-1] < 0:
            npSN[len(npSN)-1] = npSN.max()
        
        npDiffRA = npRA - metro_util.shift_right(npRA, 0)
        npDiffSN = npSN - metro_util.shift_right(npSN, 0)
        lPI = []

        for i in range(0, len(npDiffRA)):
            if npDiffRA[i] > 0:
                lPI.append(1)
            elif npDiffSN[i] > 0:
                lPI.append(2)
            elif npAT[i] > 0:
                lPI.append(1)
            else:
                lPI.append(2)

        npPI = numpy.array(lPI)
            
        # Interpolate
        npPI = metro_util.interpolate(self.npTime, npPI)
        # Round
        npPI = numpy.around(npPI)
        # Store
        wf_interpolated_data.append_matrix_col('PI', npPI)



    def __interpolate_CC(self,  wf_originpl_data, wf_interpolated_data):
        """
        Name: __interpolate_cloud_cover
        
        Parameters:
        [I] metro_data wf_controlled_data : controlled data.  Read-only
        [I] metro_data wf_interpolated_data : container of the interpolated

        Returns: None

        Description: Interpolate the cloud cover. Added in the roadcast file
         to be able to draw the the cloud cover.

        Notes: <other information, if any>
        Revision History:
        Author		Date		Reason
        Miguel Tremblay      June 20th 2005
        """
        lCC = wf_originpl_data.get_matrix_col('CC')

        npCC = numpy.array(lCC)
            
        # Interpolate
        npCC = metro_util.interpolate(self.npTime, npCC)

        # Round
        npCC = numpy.around(npCC)
        # Store
        wf_interpolated_data.append_matrix_col('CC', npCC)



    # Anthropogenic flux
    def __interpolate_FA(self, wf_originpl_data, wf_interpolated_data):
        """
        Name: __interpolate_FA
        
        Parameters:[I] metro_data wf_originpl_data : originpl data.  Read-only
                   [I] metro_data wf_processed_data : container of the interpolated
                    data.

        Returns: None

        Functions Called: metro_util.interpolate,
                          metro_data.get_matrix_col
                          metro_data.append_matrix_col

        Description: Does the interpolation of the anthropogenic flux


        Revision History:
        Author		Date		Reason
        Rok Krsmanc      October 22th 2010
        """

        if metro_config.get_value('FA') == True:
            npFA = wf_originpl_data.get_matrix_col('FA')
        # If anthropogenic flux is not specified, FA is set to a constant value of 10 W/m^2
        else:
            lFA = [10]
            npFA = numpy.array(lFA)

        npFA = metro_util.interpolate(self.npTime, npFA)
        wf_interpolated_data.append_matrix_col('FA', npFA)
