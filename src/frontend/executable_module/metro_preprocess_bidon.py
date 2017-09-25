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

from metro_preprocess import Metro_preprocess

import sys
import time
import os
import numpy

from toolbox import metro_date


class Metro_preprocess_bidon(Metro_preprocess):

    def start(self):        
        Metro_preprocess.start(self)
#        self.__test_xrdb()
#        self.__append_matrix_col(self.observation_data.get_original_data(),
#                                 self.observation_data.get_controlled_data(),
#                                 self.observation_data.get_interpolated_data())
#        self.__test_data(self.station_data)
#        self.__test_attribute(self.forecast_data)
#        self.__append_attribute(self.forecast_data)
#        self.__test_readonly(self.forecast_data.get_original_data())
#        self.__append_attribute(self.observation_data)
#        self.__test_attribute(self.observation_data)
#        self.__wf_set_gmt_time(self.forecast_data.get_processed_data())
#        self.__test_time(self.forecast_data.get_processed_data())
#        self.__test_matrix_col(self.forecast_data.get_original_data())
#        self.__test_infdata()

    def __test_infdata( self ):
        pForecast = self.get_infdata_reference('FORECAST')
        print pForecast.get_data_collection().get_original_data().get_header()

    def __test_xrdb( self ):
        os.system('echo "xclock*background: green" | xrdb -merge')
        os.system("xclock")

        
    def __test_matrix_col(self, wf_data): 
        npAT = wf_data.get_matrix_col('AT')

    def __test_data(self, data):
        print data.get_header()
        print data.get_matrix()
        print data.get_header_value('COORDINATE')
        sys.exit(3)

    def __test_readonly( self, odata ):
        odata.append_matrix_col('YY',67)

    def __test_attribute( self, data ):
        data.set_attribute('TEST', True)
        print data.get_attribute('TEST')

    def __append_attribute( self, data ):
        print "append attribute"
        data.append_attribute('TOTO',76)
        print data.set_attribute('TEST',66)
        print data.get_attribute_list()
        print data.get_attribute('TEST')
        sys.exit(4)
        
    def __test_time(self, wf_data_object):

        dWf_header = wf_data_object.get_header()

        fDate = dWf_header['PRODUCTION_DATE']

        print "***********datef =" + str(fDate)
        print "ctime=" + str(time.ctime(fDate))

        print time.gmtime(fDate)

        print metro_date.get_year(fDate)
        print metro_date.get_hour(fDate)
        sys.exit()

    def __wf_set_gmt_time(self, wf_data_object):

        npWf_data = wf_data_object.get_matrix_col('FORECAST_TIME')
        npWf_data[0] = 12.0
        npWf_data[1] = 56.0
        wf_data_object.append_matrix_col("YY",npWf_data)
        npWf_data = wf_data_object.get_matrix_col('YY')



















