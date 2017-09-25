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
Name:	       Metro_preprocess_qa_qc_station
Description: QA and QC for the station file is made here.
Notes:  
Auteur: Miguel Tremblay
Date: September 30 2014
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

_ = metro_util.init_translation('metro_preprocess_qa_qc_station')

class Metro_preprocess_qa_qc_station(Metro_preprocess):

    def start(self):
        Metro_preprocess.start(self)

        try:        
            Metro_preprocess.start(self)

            pStation = self.get_infdata_reference('STATION')

            if self.infdata_exist('HORIZON'):
                self.__check_sunshadow(pStation)

        except metro_error.Metro_data_error, inst:
            metro_logger.print_message(metro_logger.LOGGER_MSG_STOP,\
                                       str(inst))

    def __check_sunshadow(self, station_data):
        """
        Check if all the condidations for the sun-shadow algorithm are met.
        1- Presence of the data in station config file;
        2- The last value of the azimuth is 360.
        """
        pHorizon = self.get_infdata_reference('HORIZON')
        horizon_data = pHorizon.get_data()

        # Is there the <azimuth> data in the station file?
        if horizon_data == None:
            sMessage = _("Option --enable-sunshadow is given but there is no ") +\
                       _("azimuth data in station configuration file.\n ") +\
                       _("Please correct this or remove the option --enable-sunshadow")
            metro_logger.print_message(metro_logger.LOGGER_MSG_STOP,\
                                       sMessage).Metro_util_error(sMessage)


        npAzim = horizon_data.get_matrix_col('AZIMUTH')
        npElev = horizon_data.get_matrix_col('ELEVATION')

        # Verification if the array has an monotone and regular incrementation steps
        if not metro_util.is_array_uniform(npAzim):
            sMessage = _("Azimuth data in station configuration file ") +\
                       _("is not ordered by equal growing azimuths.\n ")+\
                       _("Please correct this or remove the option --enable-sunshadow")
            metro_logger.print_message(metro_logger.LOGGER_MSG_STOP,\
                                       sMessage).Metro_util_error(sMessage)


        # Check if the first item is zero degree and the last 360
        if npAzim[0] != 0 and  npAzim[-1] != 360:
                sMessage = _("Azimuth data does not have a value at 0 and/or 360 degrees. ") +\
                           _("Please add one of this value to have a complete horizon.\n ")
                metro_logger.print_message(metro_logger.LOGGER_MSG_STOP,\
                                           sMessage).Metro_util_error(sMessage)
        elif npAzim[0] == 0  and  npAzim[-1] != 360:
            horizon_data.append_matrix_row([360.0,npElev[0]]);
            

