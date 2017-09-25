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

from metro_validate import Metro_validate

import metro_logger
from toolbox import metro_util

_ = metro_util.init_translation('metro_validate_observation_ref')

class Metro_validate_observation_ref(Metro_validate):

    ##
    # methodes redefinies
    ##
    def start(self):
        Metro_validate.start(self)
        if self.infdata_exist('OBSERVATION_REF'):
            self._validate('OBSERVATION_REF')
        else:
            sMessage = _("Error, no observation_ref string to validate.\n") +\
                       _("You can safely remove this module from the ") +\
                       _("EXECUTION SEQUENCE\nif you don't need it")
            metro_logger.print_message(metro_logger.LOGGER_MSG_WARNING,
                                       sMessage)            
