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
Name:	       Metro_preprocess_qa_qc_forecast
Description: QA and QC for the atmospheric observation are made here.
Notes:  Last difference in __check_precipitation_well_define is not checked
   because of the type of data given by SCRIBE. 
Auteur: Miguel Tremblay
Date: February 28th 2005
"""

from metro_preprocess import Metro_preprocess

import numpy
import fpconst

import metro_config
import metro_logger
import metro_error
from toolbox import metro_constant
from toolbox import metro_date
from toolbox import metro_util

_ = metro_util.init_translation('metro_preprocess_qa_qc_forecast')

class Metro_preprocess_qa_qc_forecast(Metro_preprocess):

    def start(self):
        Metro_preprocess.start(self)

        try:        
            pForecast = self.get_infdata_reference('FORECAST')
            forecast_data = pForecast.get_data_collection()
        
            Metro_preprocess.start(self)
            self.__check_if_all_value_are_numbers(forecast_data.get_controlled_data())
            self.__check_if_cloud_octal(forecast_data.get_controlled_data())
            self.__check_precipitation_well_define\
                               (forecast_data.get_controlled_data())
        except metro_error.Metro_data_error, inst:
            metro_logger.print_message(metro_logger.LOGGER_MSG_STOP,\
                                       str(inst))

    def __check_if_all_value_are_numbers(self, wf_controlled_data):
        """
        Check if all the values in the forecast are numbers.
        """
        for sElement in wf_controlled_data.get_matrix_col_list():
            if sElement.find('TIME') > 0:
                continue
            npElement = wf_controlled_data.get_matrix_col(sElement)
            # In the case of 'CC', only return an error if both SF and IR
            #  are not given
            if sElement is 'CC':
                if metro_config.get_value('SF') and metro_config.get_value('IR'):
                    continue
            for fElement in npElement:
                if fpconst.isNaN(fElement):
                    if wf_controlled_data.is_standardCol(sElement):
                        sMessage = _("Value in forecast file must be valid.\n") \
                                   + _("A value for the element <%s> is invalid")\
                                   % (sElement.lower())+\
                                   _(" in the file\n'%s'") %\
                                   (metro_config.get_value(\
                            "FILE_FORECAST_IN_FILENAME"))
                        raise metro_error.Metro_data_error(sMessage)
                    else:
                        sMessage = _("A value for the extended element <%s> is invalid") % (sElement.lower())+\
                                   _(" in the file\n'%s'") %  (metro_config.get_value("FILE_FORECAST_IN_FILENAME"))
                        metro_logger.print_message(metro_logger.LOGGER_MSG_STOP,\
                                                   sMessage)


        
    def __check_if_cloud_octal(self, wf_controlled_data):
        """        
        Name: __check_if_cloud_octal
        
        Parameters:[I] metro_data wf_controlled_data : controlled data.
                Read-only data.
        Returns: None

        Functions Called:  self.forecast_data.get_matrix_col
              
        Description: Check if all the value of the variable CC is in [0,8]

        Notes: Metro gives funny surface temperature if a strange value of CC
        is entered.  Raise an exception if this occurs.

        Revision History:
        Author		Date		Reason
        Miguel Tremblay      February 28th 2005
        """
        npCloudsOctal = wf_controlled_data.get_matrix_col('CC')

        if len(numpy.where(npCloudsOctal<0)[0]) != 0  or \
               len(numpy.where(npCloudsOctal>8)[0]) != 0 :
            import metro_config
            sMessage = _("All the clouds value (<cc>) of atmospheric forecast must be") +\
                   _(" integers in interval 0-8. See file '%s'") %\
                   (metro_config.get_value("FILE_FORECAST_IN_FILENAME"))
            
            raise metro_error.Metro_data_error(sMessage)

    def __check_precipitation_well_define(self, wf_controlled_data):
        """        
        Name: __check_precipitation_well_define

        Parameters:[I] metro_data wf_controlled_data : controlled data.
             Read-only data.
        Returns: None

        Functions Called:  self.forecast_data.get_matrix_col
              
        Description: Check if the values of precipitations represent the total
        amount of precipitation from the beginning of the period. Thus, all
        the values must monotone in the RA and SN array.

        Notes: 

        Revision History:
        Author		Date		Reason
        Miguel Tremblay      February 28th 2005
        """
        lPrecip = []
        lPrecip.append(wf_controlled_data.get_matrix_col('RA'))
        lPrecip.append(wf_controlled_data.get_matrix_col('SN'))


        for npPrecip in lPrecip:
            npDiff = npPrecip - metro_util.shift_right(npPrecip,0)
            if len(numpy.where(npDiff[:-1] < 0)[0]) != 0:
                sMessage = _("All the precipitation value (<ra> and <sn>)") +\
                           _(" of atmospheric forecast represent the TOTAL") +\
                           _(" amount of precipitation since the beginning") +\
                           _(" of the period. See file '%s'") %\
                           (metro_config.get_value("FILE_FORECAST_IN_FILENAME"))
                
                raise metro_error.Metro_data_error(sMessage)
