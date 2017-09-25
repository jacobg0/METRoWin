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
Name       : metro_xml.py
Description: Methods to create and manipulate xml DOM
Work on    : 
Notes      :   
Author     : Francois Fortin
Date       : 2004
"""

import sys
import string

import metro_config
import metro_logger
import metro_error
from toolbox import metro_util

_ = metro_util.init_translation('metro_xml')

def init( sMetro_xml_lib = ""):
    global metro_xml_lib
    if sMetro_xml_lib != "":
        try:
            metro_xml_lib = __import__(sMetro_xml_lib)
        except metro_error.Metro_import_error:
            sMessage =  _("Fatal error! Can't import '%s' xml library") \
                       % (sMetro_xml_lib)
            metro_logger.print_init_message(metro_logger.LOGGER_INIT_ERROR,
                                            sMessage)
        else:
            metro_logger.print_init_message( \
                    metro_logger.LOGGER_INIT_SUCCESS,
                    _("XML library '%s' will be use.") % (sMetro_xml_lib))
            metro_xml_lib = __import__(sMetro_xml_lib)
        
    else:
        metro_logger.print_init_message(metro_logger.LOGGER_INIT_MESSAGE,
                                        _("Auto configure METRo XML library"))
        try:
            metro_util.test_import("metro_xml_libxml2")
        except metro_error.Metro_import_error, inst:
            sMessage = _("Fatal error! No METRo XML library can be use. ") +\
                       _("\nMETRo need one of the following XML library ") +\
                       _("installed on the system.\nSupported library:") +\
                       "python-libxml2"
            metro_logger.print_init_message(metro_logger.LOGGER_INIT_ERROR,
                                            sMessage)
            sys.exit(3)
        else:
            metro_logger.print_init_message( \
                    metro_logger.LOGGER_INIT_SUCCESS,
                    _("metro_xml_libxml2 will be used."))
            metro_xml_libxml2 = metro_util.import_name('toolbox',
                                                       "metro_xml_libxml2")
            metro_xml_lib = metro_xml_libxml2.Metro_xml_libxml2()
                
    metro_xml_lib.start()

def stop():
    sMessage = metro_xml_lib.stop()
    if sMessage:
        metro_logger.print_message(metro_logger.LOGGER_MSG_WARNING,sMessage)

def validate_string( sXml_content ):
    if metro_xml_lib.get_name() == "Metro_xml_libxml2":
        metro_xml_lib.validate_xml_string(sXml_content)
    else:
        sMessage = _("Validation is only supported with metro_xml_libxml2")
        if metro_logger.is_initialised():
            metro_logger.print_message(metro_logger.LOGGER_MSG_WARNING,
                                       sMessage)
        else:
            metro_logger.print_init_message(metro_logger.LOGGER_INIT_ERROR,
                                            sMessage)


def xpath( domDom, sXpath ):
    nodeLeaf = metro_xml_lib.xpath(metro_xml_lib.get_dom_root(domDom),sXpath)    
    if nodeLeaf:
        sRslt = metro_xml_lib.get_node_value(nodeLeaf[0]);
    else:
        sRslt = None
    return sRslt

def extract_xpath(lDefs, dReadHandlers, domDom, sXpath, bIs_matrix=False):
    """
    Name: extract_xpath

    Arguments: [I] lDefs: list of dictionnaries containing the data definitions
                            as defined in metro_config.py
               [I] dReadHandlers: dictionnay of read handler.
                                  key = data type name (ex: INTEGER),
                                  value = handler (ex: toolbox.metro_dom2metro_handler.read_integer)
               [I] domDOM: DOM in which data has to be extracted.
               [I] sXPath: Path of the node containing all the subnodes
                            (header, prediction, etc.)
               [I] bIs_matrix: Boolean indicating if there is more than one
                               value to fetch

    Output:  llExtractedValue : A list of lists containing the expected values.

    Description: Return one or all the value contained under the xpath in the DOM.
    """

    node_items = metro_xml_lib.xpath(metro_xml_lib.get_dom_root(domDom),
                                sXpath)

    if bIs_matrix == True:
        if len(node_items) > 0:
            llExtractedValue = []
            for node_item in node_items:
                lData = extract_data(lDefs, dReadHandlers, node_item)
                llExtractedValue.append(lData)
        else:
            llExtractedValue = None
    else:
        if len(node_items) == 1:
            node_item = node_items[0]
            llExtractedValue = extract_data(lDefs, dReadHandlers, node_item)
        elif len(node_items) > 1:
            llExtractedValue = []
            for node_item in node_items:
                lData = extract_data(lDefs, dReadHandlers, node_item)
                llExtractedValue.append(lData)
        else:
            llExtractedValue = None


    return llExtractedValue

def extract_data(lDefs, dReadHandlers, nodeItems):
    """
    Name: extract_data

    Arguments:  [I] lDefs: list of dictionary containing the
                           definition of XML element in metro_config.py
                [I] dReadHandlers: dictionnay of read handler.
                                   key = data type name (ex: INTEGER),
                                   value = handler (ex: toolbox.metro_dom2metro_handler.read_integer)
                [I] nodeItems: fecth the elements in theses nodes

    Output:   lData :: list of values, one per definition in lDefs.

    Description: Extract the data from one node containing more nodes.
    """

    lData = []

    # Retrieve the informations about the data type
    dStandard_data_type = metro_config.get_value('XML_DATATYPE_STANDARD')
    dExtended_data_type = metro_config.get_value('XML_DATATYPE_EXTENDED')

    dData_type = metro_util.join_dictionaries(dStandard_data_type,
                                              dExtended_data_type)

    # For each definitions of item
    for dDef in lDefs:
        # Get the name and the type of the item
        sTag = dDef['XML_TAG']
        sData_type_name = dDef['DATA_TYPE']
        
        if dData_type[sData_type_name].has_key('CHILD'):
            #  extract the data containing a list of "sub-data"
            nodeTmp = metro_xml_lib.xpath(nodeItems,sTag)
            lChildList = dData_type[sData_type_name]['CHILD']
            data = dReadHandlers[sData_type_name](lChildList,nodeTmp,dReadHandlers)
        else:
            #  extract the data
            data = dReadHandlers[sData_type_name](sTag,nodeItems)

        lData.append(data)

    # If there is only one definition of data (lDefs), it is an "array".
    #  In this case, we must extract the "array" from the list
    #  [[1,2,3,...,N]]  ==>  [1,2,3,...,N]
    if len(lDefs) == 1:
        if lData:
            lData = lData[0]

    return lData

def extract_data_from_node(sTag,nodeBranch):

    nodeLeaf = metro_xml_lib.xpath(nodeBranch,
                                   sTag + "/text()")

    if nodeLeaf:
        sRslt = metro_xml_lib.get_node_value(nodeLeaf[0]);
    else:
        sRslt = None

    return sRslt

def read_dom( sFilename ):
    return metro_xml_lib.read_dom(sFilename)

def dom_from_string( sXml ):
    return metro_xml_lib.dom_from_string(sXml)

def free_dom( domDoc ):
    metro_xml_lib.free_dom(domDoc)

def create_dom( sDom_root_name ):
    return metro_xml_lib.create_dom(sDom_root_name)

def get_dom_root( domDoc ):
    return metro_xml_lib.get_dom_root(domDoc)

def mkdir_xpath( domDoc, nodeBranch, sXpath ):

    nodeParent = nodeBranch
    lNode_name = string.split(sXpath,'/')

    for sNode_name in lNode_name:
        nodeChild = metro_xml_lib.create_node(sNode_name)
        metro_xml_lib.append_child(nodeParent,  nodeChild)
        nodeParent = nodeChild

    return nodeParent



def cd_xpath( nodeBranch, sXpath ):
    lChild = metro_xml_lib.xpath(nodeBranch, sXpath)
    if lChild != []:
        nodeChild = lChild[0]
    else:
        nodeChild = None
    return nodeChild

def create_node( sNode_name):
    return metro_xml_lib.create_node(sNode_name)

def create_text_node(sNode_name, sNode_value ):
    return metro_xml_lib.create_text_node(sNode_name, sNode_value )

def append_child( nodeParent, nodeChild ):
    metro_xml_lib.append_child(nodeParent, nodeChild)

def set_attribute( node, sAttributeName, sAttributeValue ):
    metro_xml_lib.set_attribute(node, sAttributeName, sAttributeValue)

def write_to_file( domDoc, sFilename ):
    metro_xml_lib.write_xml_file(domDoc, sFilename)


def create_node_tree_from_dict( domDoc, nodeParent, lDefs, dWriteHandlers, dData ):

    # Retrieve the informations on the data types
    dStandard_data_type = metro_config.get_value('XML_DATATYPE_STANDARD')
    dExtended_data_type = metro_config.get_value('XML_DATATYPE_EXTENDED')

    dData_type = metro_util.join_dictionaries(dStandard_data_type,
                                              dExtended_data_type)

    for dDef in lDefs:
        # Retrieve the name and the item type
        sTag = dDef['NAME']
        sXml_tag = dDef['XML_TAG']
        sData_type_name = dDef['DATA_TYPE']

        if dData_type[sData_type_name].has_key('CHILD'):
            #  create the node containing a list of "sub-node"
            lChildList = dData_type[sData_type_name]['CHILD']
            nodeData = dWriteHandlers[sData_type_name](sXml_tag,lChildList,dData[sTag],dWriteHandlers)
        else:
            #  create the node 
            nodeData = dWriteHandlers[sData_type_name](sXml_tag,dData[sTag])

        append_child(nodeParent, nodeData)


def create_node_tree_from_matrix( domDoc, nodeParent, sPrediction_xpath,
                                  lDefs, dWriteHandlers, metro_data_object, npMatrix ):
    """
    Each prediction will be contained in a node that will have the name
    given by sPrediction_xpath.
    """


    # Retrieve the informations about the data types
    dStandard_data_type = metro_config.get_value('XML_DATATYPE_STANDARD')
    dExtended_data_type = metro_config.get_value('XML_DATATYPE_EXTENDED')
    dData_type = metro_util.join_dictionaries(dStandard_data_type,
                                              dExtended_data_type)

    for npData in npMatrix:

        # If needed, creation of a node to contain the prediction
        if sPrediction_xpath != None and sPrediction_xpath != "":
            nodePrediction = mkdir_xpath(domDoc, nodeParent, sPrediction_xpath)
        else:
            nodePrediction = nodeParent

        for dDef in lDefs:
            # Get the name and the type of the item
            sTag = dDef['NAME']
            sXml_tag = dDef['XML_TAG']
            sData_type_name = dDef['DATA_TYPE']

            # Extraction of the data from the matrix
            lIndexList = metro_data_object.index_of_matrix_col(sTag)
            if not metro_data_object.is_multi_col(sTag):
                # single col
                val = npData[lIndexList[0]]
            else:
                # multi col
                # FFTODO good candidate for optimisation
                
                val = []
                
                for i in lIndexList:
                    val.append(npData[i])
            
            if dData_type[sData_type_name].has_key('CHILD'):
                #  create the node containing a list of "sub-node"
                lChildList = dData_type[sData_type_name]['CHILD']
                nodeData = dWriteHandlers[sData_type_name](sXml_tag,lChildList,val,dWriteHandlers)
            else:
                #  create the node 
                nodeData = dWriteHandlers[sData_type_name](sXml_tag,val)

            append_child(nodePrediction, nodeData)

def get_handler(sHandlerType, dDefData, dAllDefData=None):

    if dAllDefData == None:
        # Retrieve the informations about the data types
        dStandard_data_type = metro_config.get_value('XML_DATATYPE_STANDARD')
        dExtended_data_type = metro_config.get_value('XML_DATATYPE_EXTENDED')
        dAllDefData = metro_util.join_dictionaries(dStandard_data_type,
                                              dExtended_data_type)
    
    sTag = dDefData['NAME']
    sXml_tag = dDefData['XML_TAG']
    sData_type_name = dDefData['DATA_TYPE']

    if sData_type_name not in dAllDefData.keys():
        sMessage = _("Invalid data_type: (%s) for the following ") \
                   % (sData_type_name) +\
                   _("tag:(%s). Default data type will be used.") \
                   % (sTag)
        metro_logger.print_message(metro_logger.LOGGER_MSG_WARNING,
                                           sMessage)
        sData_type_name = 'DEFAULT'
                
    # The data type needs the call of a function to create the node
    sHandler = dAllDefData[sData_type_name][sHandlerType]

    return sHandler

