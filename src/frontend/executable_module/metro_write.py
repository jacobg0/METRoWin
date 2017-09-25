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

from metro_module import Metro_module

import metro_logger
from toolbox import metro_xml
from toolbox import metro_util

_ = metro_util.init_translation('metro_write')

class Metro_write(Metro_module):


    ##
    #methodes redefinies
    ##
    def start(self):
        Metro_module.start(self)

    def stop(self):
        Metro_module.stop(self)

    def get_receive_type(self):
        return Metro_module.DATATYPE_DOM_OUT

    def get_send_type(self):
        return Metro_module.DATATYPE_DOM_OUT

    ##
    # methodes privees
    ##
    def _write_dom(self, sFilename, domDoc):

        #read weather forecast
        try:
            sMessage = _("start writing file:'%s'") % (sFilename)
            metro_logger.print_message(metro_logger.LOGGER_MSG_DEBUG,
                                       sMessage)
            metro_xml.write_to_file(domDoc, sFilename)
        except:
            sMessage = _("An error occured when writing XML file: '%s' ") \
                       % (sFilename)
            metro_logger.print_message(metro_logger.LOGGER_MSG_CRITICAL,
                                       sMessage)
        else:
            sMessage = _("XML file: '%s' written with success") \
                       % (sFilename)
            metro_logger.print_message(metro_logger.LOGGER_MSG_INFORMATIVE,
                                       sMessage)            
