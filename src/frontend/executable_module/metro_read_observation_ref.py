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

import sys

import metro_logger
import metro_config
from data_module import metro_infdata
from toolbox import metro_util
from toolbox import metro_xml


_ = metro_util.init_translation('metro_read_observation_ref')

class Metro_read_observation_ref(Metro_read):

    ##
    #methodes redefinies
    ##
    def start(self):
        Metro_read.start(self)
        if metro_config.key_exist('FILE_OBSERVATION_REF_FILENAME'):
            sFilename = metro_config.get_value('FILE_OBSERVATION_REF_FILENAME')
        else:
            sFilename = ""

        if sFilename != "":
            try:
                sFile_content = self._read_input_data(sFilename)
            except IOError:
                sError_message = _("No file was read. METRo may need this ") +\
                                 _("file content later.")
                metro_logger.print_message(metro_logger.LOGGER_MSG_CRITICAL,
                                           sError_message)
            else:
                # creer et ajouter infdata
                infdata_observation_ref = metro_infdata.Metro_infdata( \
                    'OBSERVATION_REF', \
                    metro_infdata.DATATYPE_METRO_DATA_COLLECTION)
                infdata_observation_ref.set_input_information(sFile_content)
                self.add_infdata(infdata_observation_ref)
        else:
            sError_message = _("If you want to read a second observation file,")+\
                             _("\nplease use the option: ") +\
                             _("'--input-observation-ref'.") +\
                             _("\nYou can safely remove this module from the ") +\
                             _("EXECUTION SEQUENCE\nif you don't need it.") 
            metro_logger.print_message(metro_logger.LOGGER_MSG_WARNING,
                                       sError_message)            
