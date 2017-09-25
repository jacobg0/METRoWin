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
import string

import metro_config
from toolbox import metro_xml
from toolbox import metro_date
from toolbox import metro_util

def write_string( sXml_tag, sString ):
    return metro_xml.create_text_node(sXml_tag, sString)

def write_integer( sXml_tag, iData ):
    return metro_xml.create_text_node( sXml_tag, str(int(iData)))

def write_real( sXml_tag, iData ):
    return metro_xml.create_text_node( sXml_tag, str(float(iData)))

def write_date( sXml_tag, fDate ):
    sDate = metro_date.seconds2iso8601(fDate)
    return metro_xml.create_text_node(sXml_tag, sDate)

def write_list( sXml_list_tag, lChildList, lValues, dWriteHandlers ):
    
    listNode = metro_xml.create_node( sXml_list_tag)

    #
    # Get handler
    #
    dDef = lChildList[0]
    sData_type_name = dDef['DATA_TYPE']
    
    sXml_tag = dDef['XML_TAG']
    
    #
    # Add value to listNode
    #
    num=0
    for val in lValues:
        #  create the node 
        nodeData = dWriteHandlers[sData_type_name](sXml_tag,val)

        metro_xml.set_attribute(nodeData,"num",str(num))
        metro_xml.append_child(listNode,nodeData)

        num+=1
    return listNode
        

def integer_to_string(iNumber, iWidth=0):
    sNumber = str(iNumber)
    if len(sNumber) < iWidth:
        sNumber = string.rjust(sNumber,iWidth)
        sNumber = string.replace(sNumber,' ','0')
    return sNumber
