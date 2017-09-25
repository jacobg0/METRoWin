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

from metro_write import Metro_write

import metro_config
import metro_logger
from toolbox import metro_util
from toolbox import metro_xml

_ = metro_util.init_translation('metro_write_roadcast')

class Metro_write_roadcast(Metro_write):

    ##
    # Redefined methods
    ##
    def start(self):
        Metro_write.start(self)

        pRoadcast = self.get_infdata_reference('ROADCAST')
        self.domRoadcast =  pRoadcast.get_output_information()
        
        if self.domRoadcast != None:
            sFilename = metro_config.get_value('FILE_ROADCAST_FILENAME')
            self._write_dom(sFilename, self.domRoadcast)
        else:
            metro_logger.print_message(metro_logger.LOGGER_MSG_WARNING,
                                       _("no DOM roadcast, nothing to write"))

        pRoadcast.set_output_information(None)
            
    def stop(self):
        Metro_write.stop(self)

        if self.domRoadcast != None:
            metro_xml.free_dom(self.domRoadcast)

