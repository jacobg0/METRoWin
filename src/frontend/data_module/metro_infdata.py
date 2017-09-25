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

from toolbox import metro_util

_ = metro_util.init_translation('metro_infdata')

# Exception
ERROR_INFDATA_ITEM = "MetroInfdataError"

# DATA TYPE
DATATYPE_METRO_DATA = 0
DATATYPE_METRO_DATA_COLLECTION = 1


class Metro_infdata:

    def __init__( self, sName, iData_type ):
        self.dItems = {'NAME' : sName,
                       'XML_FORMAT' : None,
                       'INPUT_INFORMATION' : None,
                       'OUTPUT_INFORMATION' : None,
                       'DATA' : None
                       }
        self.iData_type = iData_type

    # NAME
    def get_name( self ):
        return self.dItems['NAME']

    # XML FORMAT
    def get_xml_format( self ):
        return self.dItems['XML_FORMAT']

    def set_xml_format( self, value ):
        self.dItems['XML_FORMAT'] = value

    # INPUT INFORMATION
    def get_input_information( self ):
        return self.dItems['INPUT_INFORMATION']

    def set_input_information( self, value ):
        self.dItems['INPUT_INFORMATION'] = value

    # OUTPUT INFORMATION
    def get_output_information( self ):
        return self.dItems['OUTPUT_INFORMATION']

    def set_output_information( self, value ):
        self.dItems['OUTPUT_INFORMATION'] = value

    # DATA
    def get_data( self ):
        if self.iData_type == DATATYPE_METRO_DATA:
            return self.dItems['DATA']
        else:
            sMessage = _("%s object doesn't have a Metro_data item. ") \
                       % (str(self.__class__))+\
                       _("Try to use the get_data_collection() method") 
            raise ERROR_INFDATA_ITEM, sMessage
        
    def set_data( self, value ):
        if self.iData_type == DATATYPE_METRO_DATA:
            self.dItems['DATA'] = value
        else:
            sMessage = _("%s object doesn't have a Metro_data item. ") \
                       % (str(self.__class__)) +\
                       _("Try to use the set_data_collection() method") 

            raise ERROR_INFDATA_ITEM, sMessage

    # DATA COLLECTION
    def get_data_collection( self ):
        if self.iData_type == DATATYPE_METRO_DATA_COLLECTION:
            return self.dItems['DATA_COLLECTION']
        else:
            sMessage = _("%s object doesn't have a Metro_data_collection ") \
                       % (str(self.__class__)) +\
                       _("item. Try to use the get_data() method.") 
            raise ERROR_INFDATA_ITEM, sMessage

    def set_data_collection( self, value ):
        if self.iData_type == DATATYPE_METRO_DATA_COLLECTION:
            self.dItems['DATA_COLLECTION'] = value
        else:
            sMessage = _("%s object doesn't have a Metro_data_collection ") \
                         % (str(self.__class__)) +\
                       _("item. Try to use the set_data() method.")
            raise ERROR_INFDATA_ITEM, sMessage        
