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

import string

import metro_config
import metro_logger
from toolbox import metro_xml
from toolbox import metro_util
from data_module import metro_data_collection

_ = metro_util.init_translation('metro_metro2dom')

class Metro_metro2dom( Metro_module ):

    ##
    # Class attributes
    ##
    domForecast    = None
    domRoadcast    = None

    forecast_data    = None
    observation_data = None
    station_data     = None
    roadcast_data    = None
    
    ##
    # redefined methods
    ##
    def start( self ):
        Metro_module.start(self)

        pRoadcast = self.get_infdata_reference('ROADCAST')
        roadcast_data = pRoadcast.get_data_collection()


        #
        # construct dictionnary of write handler
        #
        
        import toolbox.metro_metro2dom_handler 

        # Retrieve the informations about the data type
        dStandard_data_type = metro_config.get_value('XML_DATATYPE_STANDARD')
        dExtended_data_type = metro_config.get_value('XML_DATATYPE_EXTENDED')

        dData_type = metro_util.join_dictionaries(dStandard_data_type,
                                                  dExtended_data_type)

        dWriteHandlers = {}

        # construct dictionnary of write handlers (only done once so not expensive)
        sMessage = _("-------------------------- Write handlers available --------------------------\n")
        for dType in dData_type:
            if dData_type[dType]['WRITE'] != "":
                sCode = "handler = " + dData_type[dType]['WRITE']
                exec sCode
                dWriteHandlers[dType] = handler
                sMessage += _("TYPE: %s , HANDLER: %s\n") % (dType.ljust(15),dData_type[dType]['WRITE'])
        sMessage += "-----------------------------------------------------------------------------"        
        metro_logger.print_message(metro_logger.LOGGER_MSG_DEBUG,
                                   sMessage)                
        
        # Create roadcast
        if roadcast_data != None:
            domRoadcast = \
                self.__create_roadcast(roadcast_data.get_subsampled_data(),dWriteHandlers)

        else:
            metro_logger.print_message(metro_logger.LOGGER_MSG_WARNING,
                _("No roadcast, can't create DOM roadcast"))
            domRoadcast = None

        pRoadcast.set_output_information(domRoadcast)

    def stop( self ):
        Metro_module.stop(self)

    def get_receive_type( self ):
        return Metro_module.DATATYPE_DATA_OUT

    def get_send_type( self ):
        return Metro_module.DATATYPE_DOM_OUT


    def __create_roadcast( self, data, dWriteHandlers ):

        #
        # DOM and root element creation
        #

        sRoot_xpath = metro_config.get_value('XML_ROADCAST_XPATH_ROOT')
        domDoc = metro_xml.create_dom(sRoot_xpath)
        nodeRoot = metro_xml.get_dom_root(domDoc)

        #
        # Roadcast header creation
        #

        # Concatenation of all header keys
        lHeader_keys = \
            metro_config.get_value('XML_ROADCAST_HEADER_STANDARD_ITEMS') + \
            metro_config.get_value('XML_ROADCAST_HEADER_EXTENDED_ITEMS')

        # xpath creation
        sHeader_xpath = metro_config.get_value('XML_ROADCAST_XPATH_HEADER')

        self.__create_header(domDoc, nodeRoot, sHeader_xpath,
                             lHeader_keys, dWriteHandlers, data)


        #
        # reation of the roadcast matrix
        #

        # Concatentation of all prediction types
        lPrediction_keys = \
            metro_config.get_value('XML_ROADCAST_PREDICTION_STANDARD_ITEMS') + \
            metro_config.get_value('XML_ROADCAST_PREDICTION_EXTENDED_ITEMS')

        #  xpath creation
        sPrediction_xpath = \
            metro_config.get_value('XML_ROADCAST_XPATH_PREDICTION')

        self.__create_matrix(domDoc, nodeRoot, sPrediction_xpath,
                             lPrediction_keys, dWriteHandlers, data)

        return domDoc


    def __create_header( self, domDoc, nodeRoot, sHeader_xpath,
                         lHeader_keys, dWriteHandlers, metro_data ):

        lHeader_xpath = string.split(sHeader_xpath,"/")

        # remove root xml from xpath
        sHeader_xpath = string.join(lHeader_xpath[2:],'/')

        # If necessary, node creation to contains the header
        if sHeader_xpath != "":
            nodeHeader = metro_xml.mkdir_xpath(domDoc, nodeRoot, sHeader_xpath)
        else:
            nodeHeader = nodeRoot

        dHeader = metro_data.get_header()

        # header creation
        metro_xml.create_node_tree_from_dict(domDoc, nodeHeader,
                                             lHeader_keys, dWriteHandlers, dHeader)


    def __create_matrix( self, domDoc, nodeRoot, sPrediction_xpath,
                         lPrediction_keys, dWriteHandlers, metro_data):

        lPrediction_xpath = string.split(sPrediction_xpath,"/")

        # Creation of the branch containing the predictions
        iNb_element = len(lPrediction_xpath)
        if iNb_element > 3:
            # Keep the path between the root and the leaves.
            # ex: /niveau1/niveau2/niveau3/niveau4 -> niveau2/niveau3
            sPrediction_xpath = string.join(lPrediction_xpath[2:iNb_element-1],
                                            '/')
            # Branch creation
            nodePrediction = metro_xml.mkdir_xpath(domDoc, nodeRoot,
                                                   sPrediction_xpath)
        else:
            nodePrediction = nodeRoot

        # Extraction of the name of the prediction node
        sPrediction_node_name = string.join(lPrediction_xpath[iNb_element-1:],
                                            '/')

        #
        # Data creation
        naMatrix   = metro_data.get_matrix()
        
        metro_xml.create_node_tree_from_matrix(domDoc, nodePrediction,
                                               sPrediction_node_name,
                                               lPrediction_keys,
                                               dWriteHandlers,
                                               metro_data, naMatrix)
