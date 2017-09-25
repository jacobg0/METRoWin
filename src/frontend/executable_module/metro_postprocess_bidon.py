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

from metro_postprocess import Metro_postprocess


class Metro_postprocess_bidon(Metro_postprocess):

    def start(self):
        Metro_postprocess.start(self)

        # get roadcast
        pRoadcast = self.get_infdata_reference('ROADCAST')

        # get controlled roadcast
        roadcast_data = pRoadcast.get_data_collection()
        controlled_roadcast = roadcast_data.get_controlled_data()

        # print road station name
        print controlled_roadcast.get_header_value('ROAD_STATION')
        
        # change road station name
        controlled_roadcast.set_header_value('ROAD_STATION',"aaa")

        # print new road station name
        print controlled_roadcast.get_header_value('ROAD_STATION')        


