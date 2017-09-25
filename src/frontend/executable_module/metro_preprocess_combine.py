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
Name:		Metro_preprocess_combine
 Description: Combine the observation and the atmospheric forecast.
  Relaxation is done on the 6 first hours of forecast.
 Notes: TODO MT: Enlever le -3*3600/30 ou trouver une raison satisfaisante
  pour sa presence.
 Author: Miguel Tremblay
 Date: August 19th 2004
"""

import math
import numpy

from metro_preprocess import Metro_preprocess
from toolbox import metro_constant
from toolbox import metro_physics

class Metro_preprocess_combine(Metro_preprocess):


##
# Class attributes
##

    nDeltaIndice = 0 # The number of 30 seconds steps in the observation. 
    NTP = 0 # max(self.nDeltaIndice,0)
    NTP2 = 0 # min(self.nDeltaIndice,0)
    
#####################################################
    
    def start(self):
        Metro_preprocess.start(self)

        pForecast = self.get_infdata_reference('FORECAST')
        forecast_data = pForecast.get_data_collection()
        pObservation = self.get_infdata_reference('OBSERVATION')
        observation_data = pObservation.get_data_collection()
        
        self.__set_attribute(observation_data)
        self.__combine_AT(forecast_data.get_interpolated_data(),
                          observation_data.get_interpolated_data(),
                          observation_data)
        self.__combine_TD(forecast_data.get_interpolated_data(),
                          observation_data.get_interpolated_data(),
                          observation_data)
        self.__combine_WS(forecast_data.get_interpolated_data(),
                          observation_data.get_interpolated_data(),
                          observation_data)
        self.__combine_QP(forecast_data.get_interpolated_data(),
                          observation_data.get_interpolated_data())
        self.__create_AH(forecast_data.get_interpolated_data())

        pForecast.set_data_collection(forecast_data)
        pObservation.set_data_collection(observation_data)

    def __set_attribute(self, observation_data):
        """
        Name: __set_attribute

        Parameters:
         
        Returns: None
 
        Functions Called: max, min
                   observation_data.get_attribute

        Description: Compute the number of 30 seconds step in the observation.
         Uses self.observation_data.DELTA_T, i.e. the number of hours in the
         observation to do so.
        """
        fDeltaTMetroObservation = observation_data.get_attribute('DELTA_T')
        self.nDeltaIndice = int(fDeltaTMetroObservation*3600/30.)
        self.NTP = max(self.nDeltaIndice,0)
        self.NTP2 = min(self.nDeltaIndice,0)


    def __combine_AT(self, wf_interpolated_data, \
                     ro_interpolated_data, observation_data):
        """
        Name: __combine_AT
        
        Parameters:[I] metro_data wf_interpolated_data : interpolated
                       forecast data.
                   [I] metro_data wf_interpolated_data : interpolated
                       observation data. 
        Returns: None

        Functions Called:wf_interpolated_data.get_matrix_col
                  observation_data.get_attribute
                  numpy.where

        Description: Combine the air temperature of forecast and observation.
        """

        npAT = wf_interpolated_data.get_matrix_col('AT')
        npATO = ro_interpolated_data.get_matrix_col('AT')

        nLenATO = len(npATO)
        nLenAT = len(npAT)-3*3600/30

        # Check if there is an error in the observation
        npSwo = observation_data.get_attribute('AT_VALID_INTERPOLATED')
        npSwo = npSwo[self.nDeltaIndice:nLenATO]
        npCheck = numpy.where(npSwo == 0, 1, 0)
        npBadIndices = (numpy.nonzero(npCheck))[0]
        if len(npBadIndices) == 0:
            for i in range(0, nLenATO-self.NTP):
                npAT[i-self.NTP2] = npATO[i+self.NTP-1]
            # Relaxation des observations vers la prevision.
            # Relaxation of observation to forecast.
            # Constante de 4 heures / 4 hour relaxation constant
            nFactor = nLenATO-self.NTP
            fTaCorr = npAT[nLenATO-self.NTP-self.NTP2]-npATO[nLenATO-1]
            if fTaCorr != 0:
                if self.NTP2 < 0:
                    nValueSup = nLenAT + self.NTP2
                else:
                    nValueSup = nLenAT
                for i in range(nLenATO-self.NTP, nValueSup):
                    npAT[i-self.NTP2] = npAT[i-self.NTP2]-math.exp(-(i-nFactor)\
                                               *metro_constant.fTimeStep \
                                               *metro_constant.fConst)*fTaCorr


        wf_interpolated_data.set_matrix_col('AT', npAT)  


    def __combine_TD(self, wf_interpolated_data, \
                     ro_interpolated_data, observation_data):
        """
        Name: __combine_TD
        
        Parameters:[I] metro_data wf_interpolated_data : interpolated
                         forecast data. 
                   [I] metro_data wf_interpolated_data : interpolated
                         observation data. 
        Returns: None

        Functions Called: wf_interpolated_data.get_matrix_col
                           numpy.where, nonzero

        Description: Combine the dew point of forecast and observation.
        """

        npTD = wf_interpolated_data.get_matrix_col('TD')
        npAT = wf_interpolated_data.get_matrix_col('AT')
        npTDO = ro_interpolated_data.get_matrix_col('TD')
        
        nLenTDO = len(npTDO)
        nLenTD = len(npTD)-3*3600/30

        # Check if there is an error in the observation
        npSwo = observation_data.get_attribute('TD_VALID_INTERPOLATED')
        npSwo = npSwo[self.nDeltaIndice:nLenTDO]
        npCheck = numpy.where(npSwo == 0, 1, 0)
        npBadIndices = (numpy.nonzero(npCheck))[0]
        # If there is no error in the dew point, use the observations, otherwise
        #  use the forecast for all the observation.
        if len(npBadIndices) == 0:
            for i in range(0, nLenTDO-self.NTP):
                npTD[i-self.NTP2] = npTDO[i+self.NTP-1]

            # Relaxation des observations vers la prevision.
            # Constante de 4 heures / 4 hour relaxation constant
            nFactor = nLenTDO-self.NTP
            fTdCorr = npTD[nLenTDO-self.NTP-self.NTP2]-npTDO[nLenTDO-1]
            if fTdCorr != 0:
                if self.NTP2 < 0:
                    nValueSup = nLenTD + self.NTP2
                else:
                    nValueSup = nLenTD
                for i in range(nLenTDO-self.NTP, nValueSup):
                    npTD[i-self.NTP2] = npTD[i-self.NTP2]-math.exp(-(i-nFactor)\
                                               *metro_constant.fTimeStep \
                                               *metro_constant.fConst)*fTdCorr
                    if  npTD[i-self.NTP2] >  npAT[i-self.NTP2]:
                         npTD[i-self.NTP2] =  npAT[i-self.NTP2]

        wf_interpolated_data.set_matrix_col('TD', npTD)
 

    def __combine_WS(self, wf_interpolated_data, \
                     ro_interpolated_data, observation_data):
        """
        Name: __combine_WS
        
        Parameters:[I] metro_data wf_interpolated_data : interpolated
                       forecast data. 
                   [I] metro_data wf_interpolated_data : interpolated
                       observation data. 
        Returns: None

        Functions Called: metro_data.get_matrix_col
                   collection_data.get_attribute
                   numpy.where, nonzero

        Description: Combine the wind speed of forecast and observation.
        """

        npWS = wf_interpolated_data.get_matrix_col('WS')
        
        npWSO = ro_interpolated_data.get_matrix_col('WS')
        nLenWSO = len(npWSO)
        nLenWS = len(npWS)-3*3600/30

        # Check if there is an error in the observation
        npSwo = observation_data.get_attribute('WS_VALID_INTERPOLATED')
        npSwo = npSwo[self.nDeltaIndice:nLenWSO]
        npCheck = numpy.where(npSwo == 0, 1, 0)
        npBadIndices = (numpy.nonzero(npCheck))[0]
        if len(npBadIndices) == 0:
            for i in range(0, nLenWSO-self.NTP):
                npWS[i-self.NTP2] = npWSO[i+self.NTP-1]

            # Relaxation of observation on the atmospheric forecast
            # 4 hour relaxation constant
            nTimeStepsInRelaxation = 4*3600/metro_constant.fTimeStep
            # Check if there is long enough atmospheric forecast
            if nLenWS <  nTimeStepsInRelaxation:
                nTimeStepsInRelaxation = nLenWS
            nValueSup = nLenWSO-self.NTP + nTimeStepsInRelaxation
            if self.NTP2 < 0:
                nValueSup = int(round(nValueSup + self.NTP2))
            else: # Cast anyway
                nValueSup = int(round(nValueSup))
            nFactor = nLenWSO-self.NTP
            fCurrentObs = npWSO[nLenWSO-1]
            fCurrentFor = npWS[nLenWSO-self.NTP-self.NTP2]
            if fCurrentObs < fCurrentFor:
                # The value of 0.01 is arbitrary. It is to avoid a division
                # by a value too near of zero.
                if fCurrentFor < 0.01:
                    fCurrentFor = 1.0
                if fCurrentObs == 0:
                    fCurrentObs = 1.0
                fTdCorr = fCurrentObs/fCurrentFor
                fSlope = (1-fTdCorr)*metro_constant.fConst*\
                         metro_constant.fTimeStep
                for i in range(int(round(nLenWSO-self.NTP)), nValueSup):
                    fFactor = fSlope*(i-nLenWSO+self.NTP)+fTdCorr
                    npWS[i-self.NTP2] = fFactor*npWS[i-self.NTP2]
                
            elif fCurrentFor < fCurrentObs:
                fTdCorr = fCurrentFor - fCurrentObs
                for i in range(int(round(nLenWSO-self.NTP)), nValueSup):  
                    npWS[i-self.NTP2] = npWS[i-self.NTP2]-math.exp(-(i-nFactor)\
                                           *metro_constant.fTimeStep \
                                           *metro_constant.fConst)*fTdCorr

        wf_interpolated_data.set_matrix_col('WS', npWS)
        

    def __combine_QP(self, wf_interpolated_data, \
                     ro_interpolated_data):
        """
        Name: __combine_QP

        Parameters:[I] metro_data wf_interpolated_data : interpolated
                       forecast data. 
                   [I] metro_data wf_interpolated_data : interpolated
                       observation data. 
         Returns: None

         Functions Called: metro_data.get_matrix_col
                   collection_data.get_attribute

          Description: Set the precipitation rate with the accumulations.
                       Create the road condition.
        """
        
        npQP = wf_interpolated_data.get_matrix_col('QP')

        # Create the road condition array. 0 is dry, 1 is wet
        # This is only use in the initialization of profile
        npSC = numpy.ones(len(npQP))

        # PI is equal to 1 when there is precipitation, 0 otherwise.
        npPI = ro_interpolated_data.get_matrix_col('PI')
        npSCO = ro_interpolated_data.get_matrix_col('SC')
        nLenPI = len(npPI)
        nLenQP = len(npQP)-3*3600/30

        for i in range(0, nLenPI-self.NTP):
            npQP[i-self.NTP2] = npPI[i+self.NTP-1]*\
                                (npQP[i+1-self.NTP2])
            npSC[i-self.NTP2] = npSCO[i+self.NTP-1]

        wf_interpolated_data.set_matrix_col('QP',npQP)
        wf_interpolated_data.append_matrix_col('SC',npSC)


    def __create_AH(self, wf_interpolated_data):
        """
        Parameters:[I] metro_data wf_interpolated_data : interpolated forecast data. 
        [I] metro_data wf_interpolated_data :  interpolated observation data. 
        Returns: None

        Functions Called: metro_data.get_matrix_col
                          numpy.zeros, astype
                          metro_physics.foqst
                          metro_data.append_matrix_col

        Description: Computation of the absolute humidity (g/kg)
             see http://en.wikipedia.org/wiki/Absolute_humidity for a definition.

        Notes: 

        Revision History:
        Author		Date		Reason
        Miguel Tremblay      August 24th 2004
        """
        # Get any of the interpolated forecast to retrieve the length
        npTD = wf_interpolated_data.get_matrix_col('TD')
        npAP = wf_interpolated_data.get_matrix_col('AP')

        npLenAH = len(npTD)

        # Create the array
        npAH = numpy.zeros(npLenAH)
        npAH = npAH.astype(numpy.float)

        for i in range(0,npLenAH):
            npAH[i] = metro_physics.foqst(npTD[i]+metro_constant.fTcdk,\
                                           npAP[i])
            
        wf_interpolated_data.append_matrix_col('AH', npAH)

