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
Name       : metro_postprocess_round_roadcast         
Description: Rounding of float value stocked in roadcast matrix
Work on    : roadcast_data.subsampled_data
Notes      :   
Author     : Francois Fortin
Date       : 1 September 2004
"""

from metro_postprocess import Metro_postprocess

import numpy

import metro_config
import metro_logger
from toolbox import metro_util

_ = metro_util.init_translation('metro_postprocess_round_roadcast')

class Metro_postprocess_round_roadcast(Metro_postprocess):

    def start(self):
        Metro_postprocess.start(self)

        pRoadcast = self.get_infdata_reference('ROADCAST')
        roadcast_data = pRoadcast.get_data_collection()

        iPrecision = \
            metro_config.get_value('DEFAULT_ROADCAST_PREDICTION_PRECISION')

        if roadcast_data != None:
            self.__round_roadcast_header(roadcast_data.get_subsampled_data())
            self.__round_roadcast_data(roadcast_data.get_subsampled_data())            
        else:
            metro_logger.print_message(metro_logger.LOGGER_MSG_WARNING,
                                       _("No roadcast!"))

        pRoadcast.set_data_collection(roadcast_data)


    def __round_roadcast_header( self, roadcast):
        if 'VERTICAL_LEVELS' in roadcast.get_header():
            # Get the default value for the accurary of "float" of the roadcast
            iDefault_precision = \
                metro_config.get_value('DEFAULT_ROADCAST_PREDICTION_PRECISION')

            dData_types = metro_config.get_value('XML_DATATYPE_STANDARD')
            dExtended_data_type = metro_config.get_value('XML_DATATYPE_EXTENDED')

            dData_types.update(dExtended_data_type)
            
            sCurrent_data_type = 'VERTICAL_LEVELS'

            # get precision
            if 'CHILD' in dData_types[sCurrent_data_type]:
                if len(dData_types[sCurrent_data_type]['CHILD']) == 1 and \
                   dData_types[sCurrent_data_type]['CHILD'][0]['DATA_TYPE'] == 'REAL':
                    # If the accuracy have been specified: use it.
                    # Otherwhise use the default value for the roadcast.
                    if 'PRECISION' in dData_types[sCurrent_data_type]['CHILD'][0]:
                        iPrecision = dData_types[sCurrent_data_type]['CHILD'][0]['PRECISION']
                    else:
                        iPrecision = iDefault_precision
                    
            lLevels = roadcast.get_header_value('VERTICAL_LEVELS')

            lRounded = [round(x,iPrecision) for x in lLevels]

            roadcast.set_header_value('VERTICAL_LEVELS',lRounded)


    def __round_roadcast_data( self, roadcast_data):

        # Get the matrix columns definition
        lStandard_roadcast = metro_config.get_value( \
            'XML_ROADCAST_PREDICTION_STANDARD_ITEMS')
        lExtended_roadcast = metro_config.get_value( \
            'XML_ROADCAST_PREDICTION_EXTENDED_ITEMS')        
        lRoadcast_items = lStandard_roadcast + lExtended_roadcast

        # Get the default value for the accurary of "float" of the roadcast
        iDefault_precision = \
            metro_config.get_value('DEFAULT_ROADCAST_PREDICTION_PRECISION')


        dData_types = metro_config.get_value('XML_DATATYPE_STANDARD')
        dExtended_data_type = metro_config.get_value('XML_DATATYPE_EXTENDED')

        dData_types.update(dExtended_data_type)

        # Process of each column of roadcast
        iItem_id = 0
        for dRoadcast_item in lRoadcast_items:

            sCurrent_data_type = dRoadcast_item['DATA_TYPE']
            # If this column contains float data
            if dRoadcast_item['DATA_TYPE'] == 'REAL':

                # If the accuracy have been specified: use it.
                # Otherwhise use the default value for the roadcast.
                if 'PRECISION' in dRoadcast_item:
                    iPrecision = dRoadcast_item['PRECISION']
                else:
                    iPrecision = iDefault_precision

                # Perform the round operation
                npCol = roadcast_data.get_matrix_col(dRoadcast_item['NAME'])
                npCol = numpy.around(npCol,iPrecision)
                roadcast_data.set_matrix_col(dRoadcast_item['NAME'], npCol)

            # If this column as only one child who is a REAL: its probably a list of float
            elif 'CHILD' in dData_types[sCurrent_data_type]:
                if len(dData_types[sCurrent_data_type]['CHILD']) == 1 and \
                   dData_types[sCurrent_data_type]['CHILD'][0]['DATA_TYPE'] == 'REAL':
                    # If the accuracy have been specified: use it.
                    # Otherwhise use the default value for the roadcast.
                    if 'PRECISION' in dData_types[sCurrent_data_type]['CHILD'][0]:
                        iPrecision = dData_types[sCurrent_data_type]['CHILD'][0]['PRECISION']
                    else:
                        iPrecision = iDefault_precision

                    npCol = roadcast_data.get_matrix_col(dRoadcast_item['NAME'])
            
                    npCol = numpy.around(npCol,iPrecision)
                    roadcast_data.set_matrix_multiCol(dRoadcast_item['NAME'], npCol)
