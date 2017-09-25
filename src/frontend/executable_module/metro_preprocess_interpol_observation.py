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
Name:	       Metro_preprocess_interpol_observation
Description: Interplation of data in order to be at every 30 seconds.
               Solar flux is a particular case and is handle in
               metro_preprocess_fsint2.py .

Author: Miguel Tremblay
Date: August 2nd 2004
"""

from metro_preprocess import Metro_preprocess

import time
import numpy

import metro_config
import metro_logger
import metro_error
from toolbox import metro_util
from toolbox import metro_date
from toolbox import metro_constant

_ = metro_util.init_translation('metro_preprocess_interpol_observation')

##
# Class attributes
##
npTimeInterpolated = None # Array representing the time in seconds.
OneObservationException =  _("Not enough observation to do the interpolation")
NoObservationException = _("No valid observation.  Aborting")

class Metro_preprocess_interpol_observation(Metro_preprocess):

    def start(self):
        Metro_preprocess.start(self)

        pObservation = self.get_infdata_reference('OBSERVATION')
        observation_data = pObservation.get_data_collection()
        
        try: 
            self.__set_time(observation_data.get_controlled_data(), \
                            observation_data.get_interpolated_data(), \
                            observation_data)
            self.__interpolate_AT(observation_data.get_controlled_data(), \
                                  observation_data.get_interpolated_data())
            self.__interpolate_TD(observation_data.get_controlled_data(), \
                                  observation_data.get_interpolated_data())
            self.__interpolate_WS(observation_data.get_controlled_data(), \
                                  observation_data.get_interpolated_data())
            self.__interpolate_ST(observation_data.get_controlled_data(), \
                                  observation_data.get_interpolated_data())
            self.__interpolate_SST(observation_data.get_controlled_data(),\
                                   observation_data.get_interpolated_data())
            self.__interpolate_PI(observation_data.get_controlled_data(), \
                                  observation_data.get_interpolated_data())
            self.__interpolate_SC(observation_data.get_controlled_data(), \
                                  observation_data.get_interpolated_data())
            self.__interpolate_validatation(observation_data.\
                                            get_controlled_data(), \
                                            observation_data)      
            
        except metro_error.Metro_input_error, inst:
            metro_logger.print_message(metro_logger.LOGGER_MSG_INFORMATIVE,
                                       str(inst))

        pObservation.set_data_collection(observation_data)

    def __set_time(self, ro_controlled_data, ro_interpolated_data,
                   observation_data):
        """
        Name: __set_time
        
        Parameters: metro_data controlled_data : controlled forecast data
        
        Returns: None
        
        Functions Called:  numpy.arange, astype
                           numpy.zeros
                           metro_data.set_matrix
                           metro_data.get_matrix_col
                           metro_data.append_matrix_col
                           observation_data.set_attribute
                           metro_config.get_value('FILE_OBSERVATION_FILENAME')

        Description: Set the time array in the interpolated matrix.

        Notes:

        Revision History:
        Author		Date		Reason
        Miguel Tremblay      August 5th 2004
        """

        # Set the time in the interpolated matrix.
        npTime =  ro_controlled_data.get_matrix_col('Time')
        self.npTimeInterpolated = numpy.arange(npTime[0], \
                                               npTime[len(npTime)-1],
                                               metro_constant.fTimeStep)

        # 1.1574e-5 is the conversion from seconds to day.
        #  1/(24*3600) = 1.1574e-5
        self.npTimeInterpolated =  self.npTimeInterpolated/3600 -\
                                  24*((self.npTimeInterpolated*1.1574e-5)\
                                      .astype(numpy.int32))

        # Save the time array
        if len(self.npTimeInterpolated) > 1:
            ro_interpolated_data.append_matrix_col('Time', \
                                                self.npTimeInterpolated)
        # Only one observation, abort interpolation
        elif len(self.npTimeInterpolated) == 1:
            observation_data.set_attribute('NO_OBS',\
                                           [False, False, False, True])
            raise metro_error.Metro_input_error(OneObservationException)
        else:
            observation_data.set_attribute('NO_OBS',\
                                           [True, True, True, True])
            sMessage = _("No valid observation in: ") +\
                       metro_config.get_value('FILE_OBSERVATION_FILENAME')
            metro_logger.print_message(metro_logger.LOGGER_MSG_STOP,
                                       sMessage)

            raise metro_error.Metro_input_error(NoObservationException)

    # Air temperature
    def __interpolate_AT(self, ro_controlled_data, ro_interpolated_data):
        """
        Name: __interpolate_AT

        Parameters:[I] metro_data ro_controlled_data : controlled data. Read-only
        [I] metro_data ro_interpolated_data : container of the interpolated
        data.

        Returns: None

        Functions Called: metro_util.interpolate,
                          metro_data.get_matrix_col
                          metro_data.append_matrix_col

        Description: Does the interpolation of the air temperature
        """
        npTimeOrig = ro_controlled_data.get_matrix_col('Time')
        npAT = ro_controlled_data.get_matrix_col('AT')
        npAT = metro_util.interpolate(npTimeOrig, npAT)
        ro_interpolated_data.append_matrix_col('AT', npAT)


    # Dew point
    def __interpolate_TD(self, ro_controlled_data, ro_interpolated_data):
        """
        Name: __interpolate_TD

        Parameters:[I] metro_data ro_controlled_data : controlled data.Read-only
                   [I] metro_data ro_interpolated_data : container of the
                                                         interpolated data.

        Returns: None

        Functions Called: metro_util.interpolate,
                          metro_data.get_matrix_col
                          metro_data.append_matrix_col

        Description: Does the interpolation of the dew point


        Revision History:
        Author		Date		Reason
        Miguel Tremblay      August 5th 2004
        """
        npTimeOrig = ro_controlled_data.get_matrix_col('Time')
        npTD = ro_controlled_data.get_matrix_col('TD')
        npTD = metro_util.interpolate(npTimeOrig, npTD)
        ro_interpolated_data.append_matrix_col('TD', npTD)

    # Wind speed
    def __interpolate_WS(self, ro_controlled_data, ro_interpolated_data):
        """
        Name: __interpolate_WS

        Parameters:[I] metro_data ro_controlled_data : controlled data. Read-only
                   [I] metro_data ro_interpolated_data : container of the
                                                         interpolated data.

        Returns: None

        Functions Called: metro_util.interpolate,
                          metro_data.get_matrix_col
                          metro_data.append_matrix_col

        Description: Does the interpolation of the wind speed.
                     Wind is in km/h and is converted in
                     m/s by the product with 0.2777777


        Revision History:
        Author		Date		Reason
        Miguel Tremblay      August 11th 2004
        """
        npTimeOrig = ro_controlled_data.get_matrix_col('Time')
        npWS = ro_controlled_data.get_matrix_col('WS')*0.2777777
        npWS = metro_util.interpolate(npTimeOrig, npWS)
        ro_interpolated_data.append_matrix_col('WS', npWS)


    def __interpolate_ST(self, ro_controlled_data, ro_interpolated_data):
        """
        Name: __interpolate_ST
        
        Parameters:[I] metro_data ro_controlled_data : controlled data.
                      Read-only
                   [I] metro_data ro_interpolated_data : container of the
                         interpolated data.

        Returns: None

        Functions Called: metro_util.interpolate,
                          metro_data.get_matrix_col
                          metro_data.append_matrix_col

        Description: Does the interpolation of road temperature


        Revision History:
        Author		Date		Reason
        Miguel Tremblay      August 11th 2004
        """
        
        npTimeOrig = ro_controlled_data.get_matrix_col('Time')
        npST = ro_controlled_data.get_matrix_col('ST')
        npST = metro_util.interpolate(npTimeOrig, npST)
        ro_interpolated_data.append_matrix_col('ST', npST)

    def __interpolate_SST(self, ro_controlled_data, ro_interpolated_data):
        """
        Name: __interpolate_SST

        Parameters:[I] metro_data ro_controlled_data : controlled data.  Read-only
                   [I] metro_data ro_interpolated_data : container of the
                        interpolated data.

        Returns: None

        Functions Called: metro_util.interpolate,
                          metro_data.get_matrix_col
                          metro_data.append_matrix_col

        Description: Does the interpolation of road temperature under the surface.
        """
        
        npTimeOrig = ro_controlled_data.get_matrix_col('Time')
        npSST = ro_controlled_data.get_matrix_col('SST')

        npSST = metro_util.interpolate(npTimeOrig, npSST)
        ro_interpolated_data.append_matrix_col('SST', npSST)

    def __interpolate_PI(self, ro_controlled_data, ro_interpolated_data):
        """
        Name: __interpolate_PI

        Parameters:[I] metro_data ro_controlled_data : controlled data.  Read-only
                   [I] metro_data ro_interpolated_data : container of the
                        interpolated data.

        Returns: None

        Functions Called: metro_util.interpolate,
                          metro_data.get_matrix_col
                          metro_data.append_matrix_col
                          numpy.where, around

         Description: Does the interpolation of presence of precipitation.
         """
        
        npTimeOrig = ro_controlled_data.get_matrix_col('Time')
        npPI = ro_controlled_data.get_matrix_col('PI')
        npPI = numpy.where(npPI != 1, 0, npPI)
        npPI = metro_util.interpolate(npTimeOrig, npPI)
        # Round
        npPI = numpy.around(npPI)
        # Store
        ro_interpolated_data.append_matrix_col('PI', npPI)


    def __interpolate_SC(self, ro_controlled_data, ro_interpolated_data):
        """
        Name: __interpolate_SC

        Parameters:[I] metro_data ro_controlled_data : controlled data.
                                                        Read-only
                   [I] metro_data ro_interpolated_data : container of the
                                                  interpolated data.

        Returns: None

        Functions Called: metro_util.interpolate,
                          metro_data.get_matrix_col
                          metro_data.append_matrix_col
                          numpy.where, around

        Description: Does the interpolation of the Road Condition
          33 is the SSI code.  SEE the documentation for the conversion
          between this code and the other standard:
          https://framagit.org/metroprojects/metro/wikis/Road_condition_(METRo)

          Revision History:
          Author		Date		Reason
          Miguel Tremblay      August 12th 2004
          """
        
        npTimeOrig = ro_controlled_data.get_matrix_col('Time')
        npSC = ro_controlled_data.get_matrix_col('SC')
        # Convert
        npSC = numpy.where(npSC == 33, 0, 1)
        npSC = numpy.where(npSC < 0, 0, npSC)
        npSC = numpy.where(npSC > 1, 0, npSC)
        npSC = metro_util.interpolate(npTimeOrig, npSC)
        # Round
        npSC = numpy.around(npSC)
        # Store
        ro_interpolated_data.append_matrix_col('SC', npSC)
 

    def __interpolate_validatation(self,ro_controlled_data, observation_data):
        """
        Name: __interpolate_validatation
        
        Parameters:[I] metro_data ro_controlled_data : controlled data.  Read-only
                   [I] metro_data ro_interpolated_data : container of the
                        interpolated data.

        Returns: None

        Functions Called: metro_util.interpolate,
                          observation_data.get_attribute
                          observation_data.set_attribute
                          numpy.around

         Description: Does the interpolation of all the attributes that were set in
                      metro_preprocess_qa_qc_observation

        """
        
        npTimeOrig = ro_controlled_data.get_matrix_col('Time')
        npSST = observation_data.get_attribute('SST_VALID')
        npAT = observation_data.get_attribute('AT_VALID')
        npTD = observation_data.get_attribute('TD_VALID')
        npWS = observation_data.get_attribute('WS_VALID')

        # Interpolate
        npSST = metro_util.interpolate(npTimeOrig, npSST)
        npAT = metro_util.interpolate(npTimeOrig, npAT)
        npTD = metro_util.interpolate(npTimeOrig, npTD)
        npWS = metro_util.interpolate(npTimeOrig, npWS)
        # Round
        npTD = numpy.floor(npTD)
        npAT = numpy.floor(npAT)
        npSST = numpy.floor(npSST)
        npWS = numpy.floor(npWS)
        # Store
        observation_data.set_attribute('TD_VALID_INTERPOLATED', npTD)
        observation_data.set_attribute('AT_VALID_INTERPOLATED', npAT)
        observation_data.set_attribute('SST_VALID_INTERPOLATED', npSST)
        observation_data.set_attribute('WS_VALID_INTERPOLATED', npWS)
