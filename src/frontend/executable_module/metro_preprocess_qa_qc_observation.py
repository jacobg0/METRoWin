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
Name:	       Metro_preprocess_qa_qc_observation
Description: QA and QC for the RWIS observation are performed here.
Notes: 
Auteur: Miguel Tremblay
Date: 4 aout 2004
"""

from metro_preprocess import Metro_preprocess

import numpy

import metro_config
import metro_logger
import metro_error
from toolbox import metro_constant
from toolbox import metro_date
from toolbox import metro_util

_ = metro_util.init_translation('metro_preprocess_qa_qc_observation')


class Metro_preprocess_qa_qc_observation(Metro_preprocess):

    def start(self):
        Metro_preprocess.start(self)

        try:
        
            pForecast = self.get_infdata_reference('FORECAST')
            forecast_data = pForecast.get_data_collection()
            pObservation = self.get_infdata_reference('OBSERVATION')
            observation_data = pObservation.get_data_collection()
        
            Metro_preprocess.start(self)

            self.__check_nan(observation_data.get_controlled_data())
            self.__remove_bad_surface_temperature_arg(observation_data.get_controlled_data())
            self.__set_time(observation_data.get_controlled_data())
            self.__check_time_order(observation_data.get_controlled_data(),\
                                    forecast_data.get_controlled_data())
            self.__check_TA_TD(observation_data.get_controlled_data(),
                            observation_data)
            self.__validate(observation_data.get_controlled_data(),
                            observation_data)
            self.__set_time_difference(observation_data.get_controlled_data(),\
                                       forecast_data.get_controlled_data(),
                                       observation_data)
            
            self.__set_coupling_instruction(observation_data.\
                                            get_controlled_data(),\
                                            observation_data.\
                                            get_interpolated_data(),\
                                            observation_data)
            
            self.__check_deep_soil_value()

            pForecast.set_data_collection(forecast_data)
            pObservation.set_data_collection(observation_data)

        except metro_error.Metro_data_error:
            sMessage = _("No valid observations. Halting METRo")
            metro_logger.print_message(metro_logger.LOGGER_MSG_STOP,\
                                       sMessage)



    def __set_time(self, ro_controlled_data):
        """
        Name: __set_time
        Parameters: metro_data controlled_data : controlled observation data

        Returns: None
        
        Functions Called: metro_data.get_matrix_col
                          numpy.zeros
                          metro_date.get_hour, get_minute
                          metro_date.get_elapsed_time
                          metro_data.append_matrix_col

        Description: Put the value of the time in seconds.
                      Set it in the matrix.

        Notes: 

        Revision History:
        Author		    Date		Reason
        Miguel Tremblay      August 4th 2004
        """
        
        npOT = ro_controlled_data.get_matrix_col('OBSERVATION_TIME')
        npTime = numpy.zeros(len(npOT))
        npTime[0] = metro_date.get_hour(npOT[0])*3600 + \
                    metro_date.get_minute(npOT[0])*60
        if len(npOT) == 0:
            sMessage = _("No valid observation")
            metro_logger.print_message(metro_logger.LOGGER_MSG_INFORMATIVE,\
                                       sMessage)
            return 
        for i in range(1,len(npOT)):
            fTimeElapsed =  metro_date.get_elapsed_time(npOT[i], \
                                                        npOT[i-1],\
                                                        "UTC", "seconds")
            npTime[i] = npTime[i-1]+fTimeElapsed

        # Registered.
        ro_controlled_data.append_matrix_col('Time', npTime)
    
    

    def __check_nan(self, ro_controlled_data):
        """
        Name: __check_nan
        Parameters: metro_data controlled_data : controlled observation data
        Returns: None

        Functions Called: metro_data.get_matrix_col
                          numpy.where, nonzero, isnan
                          metro_logger.print_message
                          metro_data.del_matrix_row
                          metro_date.get_hour
                          metro_config.get_value

        Description: Remove the observations containing NaN values.

        Notes: 

        Revision History:
        Author		Date		Reason
        Miguel Tremblay      February 2017
        """

        ################ Fetch all row in the observation matrix ###############
        lColumn = ro_controlled_data.get_matrix_col_list()        

        for sElement in lColumn:
            npColumn = ro_controlled_data.get_matrix_col(sElement)
            npBad = numpy.where(numpy.isnan(npColumn) == True, 1, 0)
            if len(npBad) > 0:
                npBadIndices = (numpy.nonzero(npBad))[0]
                if len(npBadIndices) > 0:
                    sMessage = _("Invalid value(s) in %s") % (sElement)
                    metro_logger.print_message(metro_logger.LOGGER_MSG_INFORMATIVE,
                                            sMessage)
                    for i in range(0,len(npBadIndices)):
                        nIndice = npBadIndices[i]
                        sMessage = _("%dth value in %s is NaN, removing") %  (nIndice, sElement) 
                        metro_logger.print_message(metro_logger.LOGGER_MSG_INFORMATIVE,
                                               sMessage)
                    ro_controlled_data.del_matrix_row(npBadIndices)
    
    def __remove_bad_surface_temperature_arg(self, ro_controlled_data):
        """
        Name: __remove_bad_surface_temperature_arg
        Parameters: metro_data controlled_data : controlled observation data
        Returns: None

        Functions Called: metro_data.get_matrix_col
                          numpy.where, nonzero
                          metro_logger.print_message
                          metro_data.del_matrix_row
                          metro_date.get_hour
                          metro_config.get_value

        Description: Remove the wrong measure of surface temperature
                     in the controlled observations.

        Notes: 

        Revision History:
        Author		Date		Reason
        Miguel Tremblay      August 4th 2004
        """

        ################ Check road surface temperature ###############
        npST = ro_controlled_data.get_matrix_col('ST')
        # More than nRoadTemperatureHigh degrees
        npBad = numpy.where(npST > metro_constant\
                               .nRoadTemperatureHigh , 1, 0)
        if len(npBad) > 0:
            npBadIndices = (numpy.nonzero(npBad))[0]
            if len(npBadIndices) > 0:
                sMessage = _("Invalid road temperature")
                metro_logger.print_message(metro_logger.LOGGER_MSG_INFORMATIVE,
                                           sMessage)
                for i in range(0,len(npBadIndices)):
                    nIndice = npBadIndices[i]
                    sMessage = _("%d th  temperature is %f") %  \
                               ( nIndice, round(npST[nIndice],2)) 
                    metro_logger.print_message(metro_logger.LOGGER_MSG_INFORMATIVE,
                                               sMessage)
                
                ro_controlled_data.del_matrix_row(npBadIndices)
        # or less than nRoadTemperatureMin
        npST = ro_controlled_data.get_matrix_col('ST')
        npBad = numpy.where(npST < metro_constant.nRoadTemperatureMin , 1, 0)
        if len(npBad) > 0:
            npBadIndices = (numpy.nonzero(npBad))[0]
            ro_controlled_data.del_matrix_row(npBadIndices)

    def __check_time_order(self, ro_controlled_data, wf_controlled_data):
        """
        Name: __check_time_order

        Parameters: metro_data controlled_data : controlled observation data

        Returns: None
        
        Functions Called: metro_data.get_matrix_col
                          metro_util.get_difference_array
                          numpy.where, nonzero, arange
                          metro_date.get_day, get_hour, get_minute
                          metro_data.del_matrix_row
                          metro_logger.print_message

        Description: Check if the time of the observation are in order.  
                     Cut the information that are spaced by more than 240 minutes.
        Notes: 

        Revision History:
        Author		Date		Reason
        Miguel Tremblay      August 4th 2004
        """
        
        npTime = ro_controlled_data.get_matrix_col('Time')
        npCheck = metro_util.get_difference_array(npTime)
        # If a gap of more than nGapMinuteObservation
        #  minutes is identify, cut the value before.
        npCheck = metro_util.get_difference_array(npTime)        
        npBad = numpy.where( npCheck > metro_constant.\
                                nGapMinuteObservation*60, 1, 0)
        npBadIndice =  (numpy.nonzero(npBad))[0]
        if len(npBadIndice) > 0:
            sMessage =  _("More than %d minutes between 2 measures")\
                          % (metro_constant.nGapMinuteObservation)
            metro_logger.print_message(metro_logger.LOGGER_MSG_INFORMATIVE,\
                                       sMessage)
            npOT = ro_controlled_data.get_matrix_col('OBSERVATION_TIME')
            for i in range(0,len(npBadIndice)):
                nIndice = npBadIndice[i]
                sMessage = _("Indice: %d") % (nIndice)
                metro_logger.print_message(metro_logger.LOGGER_MSG_DEBUG,\
                                           sMessage)
                sMessage =  _("Cutoff time: day:%d hour:%d minute:%d") %\
                      (metro_date.get_day(npOT[nIndice]),\
                       metro_date.get_hour(npOT[nIndice]),\
                       metro_date.get_minute(npOT[nIndice]))
                metro_logger.print_message(metro_logger.LOGGER_MSG_DEBUG,\
                                           sMessage)

            
            toto = numpy.arange(0,npBadIndice[len(npBadIndice)-1]+1) 
            ro_controlled_data.del_matrix_row(toto)
        npTime = ro_controlled_data.get_matrix_col('Time')
        npBad = numpy.where( npCheck < 0, 1, 0)
        npBadIndice = (numpy.nonzero(npBad))[0]
        # Accept 1 value under zero because the last value of
        #  npBadIndice = npCheck[len(npCheck)-1] - npCheck[0]
        if len(npBadIndice) > 1:
            sMessage = _("Time of observation are not in order. ") + \
                       _("Check the %d th value") %(npBadIndice[1])
            metro_logger.print_message(metro_logger.LOGGER_MSG_STOP,\
                                      sMessage )
        # Remove the values that are equal.
        npBad = numpy.where( npCheck == 0, 1, 0)
        npBadIndice = (numpy.nonzero(npBad))[0]
        ro_controlled_data.del_matrix_row(npBadIndice)


########################################################

        npFT = wf_controlled_data.get_matrix_col('FORECAST_TIME')
        
        npOT = ro_controlled_data.get_matrix_col('Time')
        nHourStart = metro_date.get_hour(npFT[0])
        npDiff = - npOT + nHourStart*3600
        npBad = numpy.where(npDiff > metro_constant.\
                               nHourForExpirationOfObservation*3600, 1, 0)
        if len(npBad) > 0:
            npBadIndices = (numpy.nonzero(npBad))[0]
            if len(npBadIndices) > 0:
                npBadIndices = (numpy.nonzero(npBad))[0]
                sMessage = _("Observation is more than %d hours")  \
                           % ( metro_constant.nHourForExpirationOfObservation)\
                           + _("before the first roadcast")
                metro_logger.print_message(metro_logger.LOGGER_MSG_INFORMATIVE,
                                           sMessage)
                for i in range(0,len(npBadIndices)):
                    nIndice = npBadIndices[i]
                    sMessage = _("Indice: %d") % (nIndice)
                    metro_logger.print_message(metro_logger.LOGGER_MSG_DEBUG,
                                               sMessage)
                    ro_controlled_data.del_matrix_row(npBadIndices)
            
        # Get start time
        sStart_time = metro_config.get_value('INIT_ROADCAST_START_DATE')
        # If start time is not specified, default will be used
        if sStart_time == "":
            return

        # Check if the observation are not before the start of the roadcast
        #  if specified.
        fStart_time = metro_date.parse_date_string(sStart_time)
        npOT = ro_controlled_data.get_matrix_col('Time')\
               +nHourStart*3600
        npDiff = - npOT + int(metro_date.get_hour(fStart_time))*3600
        npBad = numpy.where(npDiff > metro_constant\
                               .nHourForExpirationOfObservation*3600, 1, 0)
        if len(npBad) > 0:
            npBadIndices = (numpy.nonzero(npBad))[0]
            if len(npBadIndices) > 0:
                sMessage = _("Observation after the first roadcast time of METRo")
                metro_logger.print_message(metro_logger.LOGGER_MSG_DEBUG,\
                                           sMessage)
                
                sMessage = _("Threshold: %d") \
                           % (int(metro_date.get_hour(fStart_time))*3600 \
                              +  int(metro_date.get_month(fStart_time))*60)
                metro_logger.print_message(metro_logger.LOGGER_MSG_DEBUG,\
                                           sMessage)
                for i in range(0,len(npBadIndices)):
                    nIndice = npBadIndices[i]
                    sMessage = _("Time difference: %f") \
                               % (npDiff[nIndice])
                    metro_logger.print_message(metro_logger.LOGGER_MSG_DEBUG,\
                                               sMessage)
                    ro_controlled_data.del_matrix_row(npBadIndices)


    def __validate(self, ro_controlled_data, observation_data):
        """
        Name: __validate

        Parameters: metro_data road_controlled_data : controlled observation data

        Returns: None

        Functions Called: metro_data.get_matrix_col
                          numpy.where,
                          metro_data.set_attribute

        Description: Set the attributes in road_data_collection to tell if the
                     values are in accordance of the criterium.

        """
        
        npSST = ro_controlled_data.get_matrix_col('SST')
        npAT = ro_controlled_data.get_matrix_col('AT')
        npTD = ro_controlled_data.get_matrix_col('TD')
        npWS = ro_controlled_data.get_matrix_col('WS')

        # Check SST #######################################
        npCheck = numpy.where(npSST > metro_constant.nSubSurRoadTmpHigh, 0, 1)
        npCheck = numpy.where(npSST < metro_constant.nSubSurRoadTmpMin, 0,\
                                 npCheck)

        if len(npCheck) > 0:
            # Special case, first element is not valid
            if npCheck[0] == 0:
                i = 1
                while (npCheck[i] == 0):
                    i = i+1
                    if i == len(npCheck): # No valid sub surface temperature
                        sMessage = _("No valid sub-surface temperature (element <sst>) in observation file %s")  %\
                                   (metro_config.\
                                    get_value('FILE_OBSERVATION_FILENAME'))
                        metro_logger.print_message(metro_logger.LOGGER_MSG_STOP,\
                                                   sMessage)
                         
                fCurrent = npSST[i]
            for i in range(0,len(npCheck)):
                if npCheck[i] == 1: # Good value
                    fCurrent = npSST[i]
                    continue
                else:
                    npSST[i] = fCurrent

        ro_controlled_data.set_matrix_col('SST', npSST)
        observation_data.set_attribute('SST_VALID', numpy.ones(len(npSST)))
            
        # Check AT ###########################################
        npCheck = numpy.where(npAT > metro_constant.nAirTempHigh , 0, 1)
        npCheck = numpy.where(npAT < metro_constant.nAirTempMin , 0, npCheck)
        if len(npCheck) > 0:
            observation_data.set_attribute('AT_VALID', npCheck)
            
        # Check TD ##########################################
        npCheck = numpy.where(npTD > metro_constant.nAirTempHigh, 0, 1)
        npCheck = numpy.where(npTD < metro_constant.nAirTempMin, 0, npCheck)
        npCheck = numpy.where(npTD > npAT , 0, npCheck)
        if len(npCheck) > 0:
            observation_data.set_attribute('TD_VALID', npCheck)
        
        # Check WS ###########################################
        npCheck = numpy.where(npWS > metro_constant.nMaxWindSpeed, 0, 1)
        npCheck = numpy.where(npWS < 0, 0, npCheck)

        if len(npCheck) > 0:
            observation_data.set_attribute('WS_VALID', npCheck)


    def __set_coupling_instruction(self, ro_controlled_data, \
                                   ro_interpolated_data, \
                                   observation_data):
        """

        Name: __set_coupling_instruction

        Parameters: metro_data road_controlled_data : controlled observation data
        
        Returns: None
        
        Functions Called: metro_data.get_matrix_col
                          collection_data.get_attribute
                          collection_data.set_attribute

        Description: Set the boolean field that will indicate how to perform
                     the coupling stage, based on what observations are available.

        """
        
        # Take any of the column of the observation to check the dimensions.
        npAT = ro_controlled_data.get_matrix_col('AT') 
        npTime = ro_controlled_data.get_matrix_col('Time')
        nNbr30Seconds = (npTime[len(npTime)-1]-npTime[0]) \
                        /metro_constant.fTimeStep

        # Initialize the boolean field
        bNoObs = [0, 0]
        # Check if there is any data for initialisation
        fDeltaT =  observation_data.get_attribute('DELTA_T')

        # If the beginning of the 
        if fDeltaT <= 0:
            bNoObs[0] = 1
        # Less than 3 hours of observation        
        if nNbr30Seconds-fDeltaT*3600/30. < metro_constant.nThreeHours*3600/30:
            bNoObs[1] = 1
            
        # Set the variable
        observation_data.set_attribute('NO_OBS',bNoObs)

        
    def __set_time_difference(self, ro_controlled_data, wf_controlled_data, \
                              observation_data):
        """
        Parameters: metro_data road_controlled_data : controlled observation data
                    metro_data forecast_controlled_data : controlled forecast data

        Returns: None

        Functions Called: metro_data.get_controlled_data
                          collection_data.set_attribute
                          metro_date.get_elapsed_time
                          metro_date.get_hour, get_day

        Description: Set the time difference between the beginning of observation
                     and the beginnig of the roadcast.
        """
        
        # Compute the time difference between the first forecast time
        #  and the beginning of the observation        
        StartForecast = wf_controlled_data.get_matrix_col('FORECAST_TIME')[0]
        
        StartObservation = \
            ro_controlled_data.get_matrix_col('OBSERVATION_TIME')[0]
        fTimeElapsed = metro_date.get_elapsed_time(StartForecast, \
                                                   StartObservation, \
                                                   "UTC", "hours")

        observation_data.set_attribute('DELTA_T', fTimeElapsed)

        sMessage = _("First atmospheric forecast: %s")  %\
                   (metro_date.seconds2iso8601(StartForecast))
        metro_logger.print_message(metro_logger.LOGGER_MSG_INFORMATIVE,\
                                   sMessage)

        sMessage = _("First valid observation   : %s") % \
                   (metro_date.seconds2iso8601(StartObservation))
        metro_logger.print_message(metro_logger.LOGGER_MSG_INFORMATIVE,\
                                   sMessage)
        

    def __check_TA_TD(self, ro_controlled_data, observation_data):
        """
        Description: When the dew point is over the the air temperature, replace
                     it by the air temperature.
        """
        
        npTD = ro_controlled_data.get_matrix_col('TD')
        npAT = ro_controlled_data.get_matrix_col('AT')

        # First check, if TD > AT, replace TD by AT
        npTD = numpy.where(npTD > npAT, npAT, npTD)

        ro_controlled_data.set_matrix_col('TD', npTD) 


    def __check_deep_soil_value(self):
        """
        Description: Check if the value given to --fix-deep-soil-temperature
         is valid.
        """

        # If the option is not used, do not perform the check
        if not metro_config.get_value('DEEP_SOIL_TEMP'):
            return
        
        # Check if the option is given while on a bridge
        pStation = self.get_infdata_reference('STATION')
        station_data = pStation.get_data()
        if station_data.get_station_type():
            sMessage = _("Option '--fix-deep-soil-temperature' is used while ") +\
                       _("the station is of type BRIDGE. Deep soil ") +\
                       _("Temperature  will not be used.") 
            metro_logger.print_message(metro_logger.LOGGER_MSG_WARNING,\
                                       sMessage)
        else: # In case of a road verify if the value is a double
            sTemperature = metro_config.get_value('DEEP_SOIL_TEMP_VALUE')
            try:
                dTemperature = float(sTemperature)
                if dTemperature > metro_constant.nRoadTemperatureHigh or \
                   dTemperature < metro_constant.nRoadTemperatureMin:
                    sMessage = _("Deep soil temperature following the option ")+\
                               _("'-fix-deep-soil-temperature' must be between ") +\
                               _("boundaries [") +\
                               str(metro_constant.nRoadTemperatureMin)+ "," +\
                               str(metro_constant.nRoadTemperatureHigh)+ "]. '"+\
                               sTemperature + "' is not in those boundaries."
                    metro_logger.print_message(metro_logger.LOGGER_MSG_STOP,\
                                                sMessage)

                
                # If there is no error, the value is a number, we can continue
                sMessage = _("Using deep soil temperature: ") + sTemperature +\
                           _(" degree Celsius")
                metro_logger.print_message(metro_logger.LOGGER_MSG_INFORMATIVE,\
                                           sMessage)
            except ValueError:
                sMessage = _("Option '-fix-deep-soil-temperature' must be ") +\
                       _("followed by a numeric value. The given value '") +\
                       sTemperature + _("' is not a number.") 
                metro_logger.print_message(metro_logger.LOGGER_MSG_STOP,\
                                           sMessage)
            

