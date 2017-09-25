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

import time
import os

import metro_config
import metro_logger
import metro_error
from toolbox import metro_date
from toolbox import metro_util
from toolbox import metro_xml

_ = metro_util.init_translation('metro_date')

def read_integer(sTag,nodeBranch):
    sRslt = metro_xml.extract_data_from_node(sTag,nodeBranch)
    return string_to_integer(sRslt)

def read_real(sTag,nodeBranch):
    sRslt = metro_xml.extract_data_from_node(sTag,nodeBranch)
    return string_to_real(sRslt)

def read_string(sTag,nodeBranch):
    return str(metro_xml.extract_data_from_node(sTag,nodeBranch))

def read_date(sTag,nodeBranch):
    sDate = metro_xml.extract_data_from_node(sTag,nodeBranch)
    try:
        fDate = metro_date.parse_date_string(sDate)
    except metro_error.Metro_date_error, inst:
        metro_logger.print_message(metro_logger.LOGGER_MSG_WARNING,
                                   str(inst))
        fDate = 0.0
    return fDate

def read_coordinate(lChild,nodeBranch,dReadHandler):
    if nodeBranch:
        lRslt = metro_xml.extract_data(lChild,dReadHandler,nodeBranch[0])
    else:
        lRslt = []

    return list_to_coordinate(lRslt)

def read_station_components(lChild,nodeBranch,dReadHandler):
    if nodeBranch:
        rslt = metro_xml.extract_data(lChild,dReadHandler,nodeBranch[0])
    else:
        rslt = None
    return rslt

def read_roadlayer_type(sTag, nodeBranch):
    sRslt = metro_xml.extract_data_from_node(sTag,nodeBranch)
    return roadlayer_type_to_roadlayer_code(sRslt)


def string_to_integer(sString):

    if sString != None:
        try:
            iRslt = int(sString)
        except ValueError:
            iRslt = None
    else:
        iRslt = None

    return iRslt


def string_to_real(sString):
    if sString != None:
        try:
            fRslt = float(sString)
        except ValueError:
            fRslt = None
    else:
        fRslt = None

    return fRslt



def list_to_coordinate(lValue):
    lat = None
    lon = None

    if lValue[0]:
        lat = lValue[0]
    if lValue[1]:
        lon = lValue[1]
    return (lat,lon)

def roadlayer_type_to_roadlayer_code(sLayerType):
    dValidLayerType = metro_config.get_value(\
        'XML_STATION_ROADLAYER_VALID_TYPE')

    sLayerType = sLayerType.upper()
    if sLayerType in dValidLayerType:
        iLayer_code = dValidLayerType[sLayerType]
    else:
        # raise an error
        sMessage = _("'%s' is not a valid road layer type. ") % (sLayerType) +\
                   _("Valid type are %s " ) % (dValidLayerType.keys()) +\
                   _("Check the station configuration file")
        metro_logger.print_message(metro_logger.LOGGER_MSG_STOP, sMessage)
        
    return iLayer_code


#-------------------------------------------------------------------------------
#
# Nom:          string_to_number
#
# Parametres:   I sString : chaine de caracteres a convertir
#
# Retourne:     nombre ( int ou float ), si impossible a convertir en nombre
#               retourne la string
#
# Descriptions: transformation d'une chaine de caracteres en nombre
#
#-------------------------------------------------------------------------------
def string_to_number(sString):
    if sString != None:
        #Essaie int
        try:
            rslt = int(sString)
        except ValueError:

            #Essaie float.
            try:
                rslt = float(sString)
            except ValueError:
                #Impossible a convertir, la chaine sera retourne
                rslt = sString
    else:
        rslt = None

    return rslt
