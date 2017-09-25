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
Name:	      metro_preprocess_validate_input
Description:  Validate input data to make sure they conform to certain rule. 
               1) Forecast and observation must overlap

Note:         Observation file cannot be too long because of the limitation of
               length in the fortran array.

               
Author: Francois Fortin
        Miguel Tremblay
Date: 9 novembre 2004
"""

from metro_preprocess import Metro_preprocess

import metro_logger
import metro_config
from toolbox import metro_date
from toolbox import metro_util
from toolbox import metro_constant

import numpy

_ = metro_util.init_translation('metro_config')

class Metro_preprocess_validate_input(Metro_preprocess):

    def start(self):
        Metro_preprocess.start(self)

        pForecast = self.get_infdata_reference('FORECAST')
        forecast_data = pForecast.get_data_collection()
        pObservation = self.get_infdata_reference('OBSERVATION')
        observation_data = pObservation.get_data_collection()

        self.__validate_observation_length(observation_data.\
                                            get_controlled_data())
        self.__validate_forecast_length(forecast_data.get_controlled_data())
        self.__validate_optional_args_forecast(forecast_data.\
                                               get_controlled_data())

        self.__validate_last_observation_date(observation_data.\
                                            get_controlled_data())

        self.__validate_overlap(forecast_data.get_controlled_data(),
                                observation_data.get_controlled_data())


    def __validate_optional_args_forecast(self, forecast_data):
        """
        In the case the user asked to use infra-red and/or solar flux
        as input, check if the values are really in the input files.
        """

        # Check for solar-flux
        if metro_config.get_value('SF') and  \
           'SF' not in forecast_data.lMatrix_col_name:
            sInputAtmosphericForecast = metro_config.\
                                        get_value('FILE_FORECAST_IN_FILENAME')
            sMessage = _("The option '--use-solarflux-forecast' was used\n") +\
                       _("but the information was not in the atmospheric\n") +\
                       _("forecast file. Please check for the tag '<sf>'\n") +\
                       _("in the file: %s") % (sInputAtmosphericForecast)
            metro_logger.print_message(
                metro_logger.LOGGER_MSG_STOP, sMessage)
        # Check for infra-red
        if metro_config.get_value('IR') and  \
           'IR' not in forecast_data.lMatrix_col_name:
            sInputAtmosphericForecast = metro_config.\
                                        get_value('FILE_FORECAST_IN_FILENAME')
            sMessage = _("The option '--use-infrared-forecast' was used\n") +\
                       _("but the information was not in the atmospheric\n") +\
                       _("forecast file. Please check for the tag '<ir>'\n") +\
                       _("in the file: %s") % (sInputAtmosphericForecast)
            metro_logger.print_message(
                metro_logger.LOGGER_MSG_STOP, sMessage)
        

    def __validate_forecast_length(self, forecast_data):
        """
        Parameters: controlled forecast data
        
        Description: METRo needs more than one forecast date.
        If there is only one forecast, give an error message an exit.
        """
        
         # Check the length of forecast. 
        npFT = forecast_data.get_matrix_col('FORECAST_TIME')
        
        nbrHours = metro_date.get_elapsed_time(npFT[-1], \
                                               npFT[0]) + 1

        # At least 2 forecast
        if len(npFT) < 2:
            sMessage = _("METRo needs more than one forecast date! Exiting")
            metro_logger.print_message(
                metro_logger.LOGGER_MSG_STOP, sMessage)

        # Forecast must be at every hour.
        for i in range(len(npFT)):
            nHourElapsed = metro_date.get_elapsed_time(npFT[i], \
                                                       npFT[0])
            if i != nHourElapsed:
                sMessage = _("Atmospheric forecast must be at every hour.") +\
                           _(" Check file from %d hours after the start time.") \
                           % (i)
                metro_logger.print_message(
                    metro_logger.LOGGER_MSG_STOP, sMessage)



    def __validate_observation_length(self, observation_data):
        """
        Parameters: controlled observation data
        
        Description: Check if the observation is not too long.
        If so, truncate the beginning of the observation.
        This limitation is due to an array size hardcoded in the fortran code. 
        """

        # Check the length of observation
        npOT = observation_data.get_matrix_col('OBSERVATION_TIME')
        fLast_observation_date = npOT[len(npOT)-1]
        fFirst_observation_date  = npOT[0]

        fLenght_observation_seconds = fLast_observation_date -\
                                      fFirst_observation_date
        nNbr_30_seconds_step_in_obs = fLenght_observation_seconds/30

        # Check if the length of observation is too high for the fortran code
        if nNbr_30_seconds_step_in_obs > metro_constant.nNL:
            nStepsToRemove = nNbr_30_seconds_step_in_obs -  metro_constant.nNL

            # Format the strings for warning message
            nNumberSecondsToRemove = nStepsToRemove*30
            fNumberHourToRemove = nNumberSecondsToRemove/3600.0
            fNewStartTime = fFirst_observation_date + nNumberSecondsToRemove
            sNewStartTime = metro_date.seconds2iso8601(fNewStartTime)
            # Retrieve the first time in observation that is after this date
            #  numpy trick. Put 0 where the time is under fNewStartTime
            npNumberOfItemToRemove = numpy.where(npOT <fNewStartTime, 1, 0)
            #  Get the indice of the last indice that is not zero
            tNonZero = numpy.nonzero(npNumberOfItemToRemove)
            nRemoveUntilIndice = tNonZero[0][-1]+1
            
            sOldStartTime = metro_date.seconds2iso8601(fFirst_observation_date)
            sMessage = _("Too many observation. Removing the %s seconds ") % \
                       (nNumberSecondsToRemove) + \
                       _("i.e. %s hour(s)\n")   % (fNumberHourToRemove) + \
                       _("Old start time is %s\n") % (sOldStartTime) + \
                       _("New start time is %s") % (sNewStartTime)
            metro_logger.print_message(
                metro_logger.LOGGER_MSG_WARNING, sMessage)

            # Warning is done, remove the data
            observation_data.del_matrix_row(range(nRemoveUntilIndice))


    def __validate_last_observation_date(self, observation_data):
        """
        Description: Set the date of the last observation.

        Notes: 

        Revision History:
        Author		Date		Reason
        Miguel Tremblay      August 4th 2004
        """

        # Get the last observation
        npOT = observation_data.get_matrix_col('OBSERVATION_TIME')
        fLast_observation_date = npOT[len(npOT)-1]
        sStart_date = metro_date.seconds2iso8601(fLast_observation_date)
        metro_config.set_value('DATA_ATTRIBUTE_LAST_OBSERVATION', sStart_date)
        sMessage = _("Last observation date is: '%s'") % (sStart_date)
        metro_logger.print_message(metro_logger.LOGGER_MSG_INFORMATIVE,\
                                   sMessage)            
        

    def __validate_overlap( self, forecast_data, observation_data ):
        """        
        Parameters: forecast_data, observation_data

        Description: Make sure forecast and observation overlap, if it's
                     not the case abort METRo

        """

        fForecast_start = forecast_data.get_matrix_col('FORECAST_TIME')[0]
        npObservation = observation_data.get_matrix_col('OBSERVATION_TIME')
        fObservation_end = npObservation[len(npObservation)-1]

        if fForecast_start > fObservation_end:
            sForecast_start = metro_date.seconds2iso8601(fForecast_start)
            sObservation_end = metro_date.seconds2iso8601(fObservation_end)
            sError = _("Forecast and observation don't overlap. The date\n") +\
            _("of the first forecast must be before the last date of ") +\
            _("observation.\nFirst Forecast='%s'\nLast Observation='%s'") \
            %(sForecast_start,sObservation_end)

            metro_logger.print_message(metro_logger.LOGGER_MSG_STOP, sError)
