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

# -*- coding: iso-8859-1 -*-

import string
import sys

import metro_config
import metro_logger
import metro_error
from toolbox import metro_util
from toolbox import metro_date

_ = metro_util.init_translation('metro_config_validation')

def config_error_string( sOption, iFrom, sError ):
    if   iFrom == metro_config.CFG_INTERNAL:
        sFrom = _("Internal METRo configuration")
    elif iFrom == metro_config.CFG_HARDCODED:
        sFrom = _("Hardcoded value")
    elif iFrom == metro_config.CFG_CONFIGFILE:
        sFrom = _("Configuration file")
    elif iFrom == metro_config.CFG_COMMANDLINE:
        sFrom = _("Command line parameter")
    else:
        sFrom = "Unknown"
        
    return _("Configuration error:\n") + \
           "------------------- \n" + \
           _("Config item: %s\n") % (sOption) + \
           _("Set from:    %s.\n") % (sFrom) + \
           _("The following error occured:\n%s") % (sError)

def validate_handler( sHandler, iFrom, sDescription ):
#    (sModule_name,sFunction_name) = string.split(sHandler,'.')
    lFunctionPart = string.split(sHandler,'.')
    sFunction_module = string.join(lFunctionPart[:-1],".")
    sFunction_name = lFunctionPart[-1]
    try:           
        metro_util.test_function_existence(sFunction_module, sFunction_name)
    except metro_error.Metro_import_error, inst:
        sMessage = config_error_string(sDescription,
                                       iFrom,
                                       str(inst))
        metro_logger.print_init_message(metro_logger.LOGGER_INIT_ERROR,
                                        sMessage)
        sys.exit(3)


def validate_xml_itemlist_def( sConfig_path, iFrom, lItems, dData_type ):
    
    # validate child structure
    for dItem in lItems:
        if not 'NAME' in dItem or \
           not 'XML_TAG' in dItem or \
           not 'DATA_TYPE' in dItem:
            sError = _("Some XML definition are not complete.\n") + \
                     _("Each definition must have the following property ") + \
                     _("set:\nNAME, XML_TAG, DATA_TYPE")
            sMessage = config_error_string(sConfig_path, iFrom, sError)
            metro_logger.print_init_message(metro_logger.LOGGER_INIT_ERROR,
                                            sMessage)
            sys.exit(3)                    

    # validate each child
    for dItem in lItems:
        sChild_type = dItem['DATA_TYPE']
        sChild_name = dItem['NAME']

        # si le type du child n'est pas un type valide
        if sChild_type not in dData_type:

            # liste de tout les types valide
            lKeys = dData_type.keys()
            lKeys.sort()            
            sType_list = metro_util.list2string(lKeys)
            
            sError = _("In item %s, '%s' is not a valid METRo data type.") \
                     % (sChild_name, sChild_type)+ \
                     _("\nValid METRo data type are:\n[%s]") \
                     % (sType_list)
    
            sMessage = config_error_string(sConfig_path, iFrom, sError)
            metro_logger.print_init_message(metro_logger.LOGGER_INIT_ERROR,
                                            sMessage)
            sys.exit(3)

def validate_xml_file_def( dConf ):

    # file definition to check
    lXML_files = ['XML_FORECAST_HEADER_STANDARD_ITEMS',
                  'XML_FORECAST_HEADER_EXTENDED_ITEMS',
                  'XML_FORECAST_PREDICTION_STANDARD_ITEMS',
                  'XML_FORECAST_PREDICTION_EXTENDED_ITEMS',
                  'XML_OBSERVATION_HEADER_STANDARD_ITEMS',
                  'XML_OBSERVATION_HEADER_EXTENDED_ITEMS',
                  'XML_OBSERVATION_MEASURE_STANDARD_ITEMS',
                  'XML_OBSERVATION_MEASURE_EXTENDED_ITEMS',
                  'XML_STATION_HEADER_STANDARD_ITEMS',
                  'XML_STATION_HEADER_EXTENDED_ITEMS',
                  'XML_STATION_ROADLAYER_STANDARD_ITEMS',
                  'XML_STATION_ROADLAYER_EXTENDED_ITEMS',
                  'XML_ROADCAST_HEADER_STANDARD_ITEMS',
                  'XML_ROADCAST_HEADER_EXTENDED_ITEMS',
                  'XML_ROADCAST_PREDICTION_STANDARD_ITEMS',
                  'XML_ROADCAST_PREDICTION_EXTENDED_ITEMS',
                  ]

    # extract all data type
    dStandard_data_type = metro_config.get_value('XML_DATATYPE_STANDARD')
    dExtended_data_type = metro_config.get_value('XML_DATATYPE_EXTENDED')
    dAll_data_type = metro_util.join_dictionaries(dStandard_data_type,
                                                  dExtended_data_type)
    
    for sXML_file in lXML_files:
        iFrom = dConf[sXML_file]['FROM']
        lXML_items = dConf[sXML_file]['VALUE']
        validate_xml_itemlist_def( sXML_file, iFrom,
                                   lXML_items, dAll_data_type )

def validate_datatype_category( sConfig_item, iFrom,
                                dData_type_category, dAll_data_type ):

    # validation de tout les types de data
    for sKey in dData_type_category.keys():
        
        # Validate data type read/write handler
        for sHandler in ['READ','WRITE']:
            if dData_type_category[sKey][sHandler]:
                sDescription = "[%s][%s][%s]" % (sConfig_item, sKey, sHandler)
                validate_handler(dData_type_category[sKey][sHandler],
                                 iFrom, sDescription)

        # Validate all child if present
        if 'CHILD' in dData_type_category[sKey]:
            sConfig_path = "[%s][%s][CHILD]" % (sConfig_item, sKey)
            validate_xml_itemlist_def(sConfig_path,
                                      iFrom,
                                      dData_type_category[sKey]['CHILD'],
                                      dAll_data_type)    

def validate_datatype( dConf ):

    # extract data type
    dStandard_data_type = metro_config.get_value('XML_DATATYPE_STANDARD')
    dExtended_data_type = metro_config.get_value('XML_DATATYPE_EXTENDED')
    dAll_data_type = metro_util.join_dictionaries(dStandard_data_type,
                                              dExtended_data_type)
    
    # validate Metro standard data type
    sConfig_item = 'XML_DATATYPE_STANDARD'
    iFrom =  dConf[sConfig_item]['FROM']
    validate_datatype_category( sConfig_item, iFrom,
                                dStandard_data_type, dAll_data_type )

    # validate User data type
    sConfig_item = 'XML_DATATYPE_EXTENDED'
    iFrom =  dConf[sConfig_item]['FROM']
    validate_datatype_category( sConfig_item, iFrom,
                                dExtended_data_type, dAll_data_type )

def validate_execution_sequence( dConf ):
    sKey = 'INIT_MODULE_EXECUTION_SEQUENCE'
    lExecutionSequence = dConf[sKey]['VALUE']
    iFrom = dConf[sKey]['FROM']
    for sModule in lExecutionSequence:
        try:           
            metro_util.test_import(sModule)
        except metro_error.Metro_import_error, inst:
            sConfig_path = "%s module:'%s'" % (sKey,sModule)
            sMessage = config_error_string(sConfig_path,
                                           iFrom,
                                           str(inst))
            metro_logger.print_init_message(metro_logger.LOGGER_INIT_ERROR,
                                            sMessage)
            sys.exit(3)

def validate_roadcast_start_time( dConf ):
    sKey = 'INIT_ROADCAST_START_DATE'
    sStart_time = dConf[sKey]['VALUE']

    if sStart_time != "":
        try:
            metro_date.parse_date_string(sStart_time)
        except metro_error.Metro_date_error, inst:
            sMessage = _("Fatal error, the date string '%s' passed to the\n ")\
                       % (sStart_time)+\
                       _("option '--roadcast-start-date' doesn't conform to ") +\
                       _("ISO 8601")
            metro_logger.print_init_message(metro_logger.LOGGER_INIT_ERROR,
                                            sMessage)
            sys.exit(3)
    else:
        sMessage = _("No roadcast start date provided. The date of the\n") + \
                   _("last observation will be used as the roadcast ") + \
                   _("start date\n")
        metro_logger.print_init_message(metro_logger.LOGGER_INIT_ERROR,
                                        sMessage)
    
    
    
def validate_config( dConf ):
    """
    Execution of the validation of the configuration files.
    """
    validate_datatype(dConf)
    validate_execution_sequence(dConf)
    validate_xml_file_def(dConf)
    validate_roadcast_start_time(dConf)
