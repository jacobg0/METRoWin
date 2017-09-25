# # -*- coding:iso-8859-1  -*-

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
Name:		metro_xml_libxml2
Description:  Wrapper for libxml2 library
 
Notes:

Author: François Fortin
Date: Somewhere in the summer 2004
"""

import libxml2

import metro_logger
from toolbox import metro_util

_ = metro_util.init_translation('metro_xml_libxml2')

def noerr(ctx, str):
    sMessage =  _("XML Error!: %s") % str
    if metro_logger.is_initialised():            
        metro_logger.print_message(metro_logger.LOGGER_MSG_DEBUG,
                                   sMessage)
    else:
        metro_logger.print_init_message(metro_logger.LOGGER_INIT_ERROR,
                                        sMessage)

#def xml_error_handler(arg,msg,severity,reserved):
#    print "XML Error: severity=%s, msg=%s" % (severity,msg)


class Metro_xml_libxml2:

    def start( self ):        
        # Memory debug specific
        libxml2.debugMemory(1)

        # init error handler
        libxml2.registerErrorHandler(noerr, None)
    
    def stop( self ):
        sMessage = None
        # Memory debug specific

        libxml2.cleanupParser()
        if libxml2.debugMemory(1) != 0:
            sMessage = _("LIBXML2 Memory leak %d bytes") %\
                       (libxml2.debugMemory(1))
        libxml2.dumpMemory()
        return sMessage
    
    def get_name( self ):
        return str(self.__class__.__name__)

    
    #------------------
    # lecture d'un DOM
    #------------------
    
    def read_dom( self, sFilename ):
        return libxml2.parseFile(sFilename)    

    def read_html_dom(self, sFilename):
        return libxml2.htmlParseFile(sFilename, 'iso-8859-1')
    
    def dom_from_string( self, sXml ):
        return libxml2.parseDoc(sXml)
    
    def xpath( self, nodeBranch, sXpath ):
        try:
            node = nodeBranch.xpathEval(sXpath)
        except(IndexError):
            sMessage = "Unable to find an expression corresponding to the " +\
                       "Xpath: '%s'" %((sAllMatch))
            raise sMessage

        return node
    
    def get_node_value( self, node ):
        if type(node) == type([]) and len(node) == 1:
            return node[0].get_content()
        else:
            return node.get_content()

    def get_node_name( self, node ):
        return node.get_name()

    def get_node_type( self, node ):
        return node.get_type()
    
    #------------
    # validation 
    #------------
        
    def validate_xml_string( self, sXml_content ):
        ctxt = libxml2.createDocParserCtxt(sXml_content)

#        ctxt.validate(1)
        
        ctxt.parseDocument()

        # detecte si au moins une erreur c'est produite
        try:
            error = libxml2.lastError()
        except:
            error = None
            
        if error != None:
            sMessage = _("At least one error occured when validating XML file.")
            raise "metroValidationError", sMessage
            
        doc = ctxt.doc()
        doc.freeDoc()

    #------------------
    # creation d'un DOM
    #------------------
    
    def create_dom( self, sDoc_name ):
        """
        DOM creation.
        """
        domDoc = libxml2.newDoc("1.0")
        domDoc.newChild(None,sDoc_name,None)
        return domDoc

    def create_text_node( self, sNode_name, sNode_value ):
        """
        Create and return a text node of name sNode_name with value
         sNode_value.
        
         Note: 
        """
        nodeText = libxml2.newText(sNode_value)
        nodeTmp  = libxml2.newNode(sNode_name)
        nodeTmp.addChild(nodeText)
        return nodeTmp
    
    def create_node( self, sNode_name ):
        return libxml2.newNode(sNode_name)

    def set_attribute( self, node, sAttributeName, sAttributeValue ):
        node.setProp(sAttributeName,  sAttributeValue)
    
    def append_child( self, nodeParent, nodeChild ):
        nodeParent.addChild(nodeChild)
    
    def write_xml_file( self, domDoc, sFilename ):
        domDoc.saveFormatFileEnc(sFilename,"UTF-8",1);
    
    #------------------
    # autre
    #------------------
    
    def get_dom_root( self, doc ):
        return doc.getRootElement()
    
    def free_dom( self, doc ):
        doc.freeDoc()

    def copy_node(self, node):
        """
        Copy a node with all is content (attributes, text-value and child-nodes)
        """
        return node.copyNode(True)

    ##############################################
    # Add '//' on the string and return a copy of the node
    #  of the node result.
    ##############################################
    def all_matching_xpath(self, dom, sXpath):
        sAllMatch = '//' + sXpath
        node = self.xpath(dom, sAllMatch)[0]
        node_copy = self.copy_node(node)
        return node_copy

    def get_nodes_in_list(self, dom, sXPath):
        """
        Returns all the node of the xpath in a list
        """
        lNode = []
        nodes = self.xpath(dom, sXPath)
        for node in nodes:
            lNode.append(self.get_node_value(node))
        return lNode

    def set_prop(self, node, sName, value):
        """
         Set an attribute to a node.
         'value' can be a string or a list of string
         """
        
        node.setProp(sName, value)

        return node

    def get_childNodes(self, node):
        """
        Returns a list of node that contains all children of a node.
        """
        lChildNode = []

        node_child = node.get_children()

        while node_child:
            if node_child.get_type() != 'text':
                lChildNode.append(node_child)      
            node_child = node_child.get_next()

        return lChildNode
