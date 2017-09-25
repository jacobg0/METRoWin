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
Name:	      metro_read_observation.py
Description:  check if a observation file is provided. Return an error message
              if not.
              Set the last observation time.
               
Authors: Francois Fortin
         Miguel Tremblay
Date:    March 5th 2007
"""


from metro_read import Metro_read

import metro_config
import metro_logger
from data_module import metro_infdata
from toolbox import metro_util
from toolbox import metro_xml

_ = metro_util.init_translation('metro_read_observation')

class Metro_read_observation(Metro_read):

    ##
    # Methods overwritten
    ##
    def start(self):
        Metro_read.start(self)

        if metro_config.key_exist('FILE_OBSERVATION_FILENAME'):
            sFilename = metro_config.get_value('FILE_OBSERVATION_FILENAME')
        else:
            sFilename = ""

        if sFilename != "":

            try:
                sFile_content = self._read_input_data(sFilename)
            except IOError:
                sError_message = _("METRo need a valid observation file.")
                metro_logger.print_message(metro_logger.LOGGER_MSG_STOP,
                                           sError_message)
            else:
                # Create and add infdata
                infdata_observation = metro_infdata.Metro_infdata(
                    'OBSERVATION', metro_infdata.DATATYPE_METRO_DATA_COLLECTION)
                infdata_observation.set_input_information(sFile_content)
                self.add_infdata(infdata_observation)
        else:
            sError_message = _("METRo need an observation file, please use ") +\
                             _("the option: '--input-observation'")
            metro_logger.print_message(metro_logger.LOGGER_MSG_STOP,
                                       sError_message)     

