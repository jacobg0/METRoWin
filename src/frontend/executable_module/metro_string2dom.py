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
import metro_error
from toolbox import metro_xml
from toolbox import metro_util

_ = metro_util.init_translation('metro_string2dom')

class Metro_string2dom(Metro_module):

    def __init__(self):
        if self.__class__ is Metro_string2dom:
            sMessage = _("class %s is a virtual class") % \
                       str(self.__class__)
            raise NotImplementedError(sMessage)

    ##
    # Redefined method
    ##
    def get_receive_type( self ):
        return Metro_module.DATATYPE_INPUT

    def get_send_type( self ):
        return Metro_module.DATATYPE_INPUT

    ##
    # Protected method
    ##
    def _convert_string2dom( self, sString ):
        if sString != None:
            try:
                return metro_xml.dom_from_string(sString)
            except:
                metro_logger.print_message(metro_logger.LOGGER_MSG_DEBUG,
                                           _("Error when converting string ") +\
                                           _("to DOM."))
                sMessage = _("Error when converting string to DOM. ") +\
                           _("The string is:\n%s") % (sString)
                raise metro_error.Metro_xml_error(sMessage)
        else:
            sMessage = _("No string to convert")
            metro_logger.print_message(metro_logger.LOGGER_MSG_DEBUG,
                                       sMessage)
            raise metro_error.Metro_xml_error(sMessage)
