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

from metro_read import Metro_read

import metro_config
import metro_logger
from toolbox import metro_util
from toolbox import metro_xml
from data_module import metro_infdata

_ = metro_util.init_translation('metro_read_forecast')

class Metro_read_forecast(Metro_read):

    ##
    # Overwritten methods
    ##
    def start(self):
        Metro_read.start(self)
        
        if metro_config.key_exist('FILE_FORECAST_IN_FILENAME'):
            sFilename = metro_config.get_value('FILE_FORECAST_IN_FILENAME')
            try:
                sFile_content = self._read_input_data(sFilename)
            except IOError:
                sError_message = _("METRo need a valid forecast file.") 
                metro_logger.print_message(metro_logger.LOGGER_MSG_STOP,
                                           sError_message)
            else:
                # Create and append infdata
                infdata_forecast = metro_infdata.Metro_infdata(
                    'FORECAST', metro_infdata.DATATYPE_METRO_DATA_COLLECTION)
                infdata_forecast.set_input_information(sFile_content)
                self.add_infdata(infdata_forecast)
        else:
            sError_message = _("METRo need a forecast file, please use the ") +\
                             _("option: '--input-forecast'") 
            metro_logger.print_message(metro_logger.LOGGER_MSG_STOP,
                                       sError_message)                        

