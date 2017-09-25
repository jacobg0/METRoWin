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


class Metro_postprocess_custom_output(Metro_postprocess):

    def start(self):
        Metro_postprocess.start(self)

        # get station data
        pStation = self.get_infdata_reference('STATION')
        station_data = pStation.get_data()

        # get roadcast data
        pRoadcast = self.get_infdata_reference('ROADCAST')
        roadcast_data = pRoadcast.get_data_collection()

        self.__add_scribe_point_to_roadcast(roadcast_data, station_data)
                
    def __add_scribe_point_to_roadcast( self, roadcast, station ):

        # get subsampled roadcast
        subsampled_roadcast = roadcast.get_subsampled_data()

        # extract scribe_point from station
        sScribe_point = station.get_header_value('SCRIBE_POINT')

        # add scribe_point to roadcast
        subsampled_roadcast.set_header_value('SCRIBE_POINT',sScribe_point)

        
