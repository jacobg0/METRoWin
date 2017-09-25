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

import string

import metro_logger
from data_module import metro_infdata_container
from data_module import metro_infdata
from toolbox import metro_util

_ = metro_util.init_translation('metro_module')

class Metro_module:

    # module I/O type
    DATATYPE_NONE     = 0
    DATATYPE_INPUT    = 1
    DATATYPE_DATA_IN  = 2
    DATATYPE_DATA_OUT = 3
    DATATYPE_DOM_OUT  = 4
    lData_type_txtid = ["NONE","INPUT", "DATA_IN", "DATA_OUT", "DOM_OUT"]

    # infdata container
    infdata_container = metro_infdata_container.Metro_infdata_container()

    # infdata datatype
    INFDATATYPE_DATA = metro_infdata.DATATYPE_METRO_DATA
    INFDATATYPE_DATA_COLLECTION = \
        metro_infdata.DATATYPE_METRO_DATA_COLLECTION

    def __init__(self):
        if self.__class__ is Metro_module:
            sMessage = _("class %s is a virtual class") % \
                       str(self.__class__)
            raise NotImplementedError(sMessage)

    def start(self):
        metro_logger.print_blank_line(metro_logger.LOGGER_MSG_EXECPRIMARY)
        metro_logger.print_blank_line(metro_logger.LOGGER_MSG_EXECPRIMARY)
        sMessage = _("%s module: start execution") % \
                   (string.upper(self.__module__))
        metro_logger.print_message(metro_logger.LOGGER_MSG_EXECPRIMARY,sMessage)

    def stop(self):
        sMessage = _("%s module: end of execution") \
                   % (string.upper(self.__module__))
        metro_logger.print_message(metro_logger.LOGGER_MSG_EXECPRIMARY,sMessage)

    def receive_data( self, infdata_container ):
        sMessage = _("%s module: receiving data") \
                   % (string.upper(self.__module__))
        metro_logger.print_message(metro_logger.LOGGER_MSG_EXECSECONDARY,
                                   sMessage)
        self.infdata_container = infdata_container
        
    def send_data_to( self, target_module ):
        sMessage = _("%s module:\nsending data to module %s") \
                   % (string.upper(self.__module__),
                      string.upper(target_module.__module__))
        metro_logger.print_message(metro_logger.LOGGER_MSG_EXECSECONDARY,
                                   sMessage)
        target_module.receive_data(self.infdata_container)

    def get_receive_type(self):
        if self.__class__ is not Metro_module:
            sMessage = _("class %s misses method 'get_receive_type'") \
                       % str(self.__class__)
            raise NotImplementedError(sMessage)

    def get_send_type(self):
        if self.__class__ is not Metro_module:
            sMessage = _("class %s misses method 'get_send_type'") \
                       % str(self.__class__)
            raise NotImplementedError(sMessage)

    def get_receive_type_txtid(self):
        return self.lData_type_txtid[self.get_receive_type()]

    def get_send_type_txtid(self):
        return self.lData_type_txtid[self.get_send_type()]

    def add_infdata( self, infdata ):
        self.infdata_container.add_infdata(infdata)
        
    def infdata_exist( self, sInfdata_name ):
        return self.infdata_container.infdata_exist(sInfdata_name)

    def get_infdata_reference( self, sInfdata_name ):
        return self.infdata_container.get_infdata_reference(sInfdata_name)

    def get_infdata_container( self ):
        return self.infdata_container

    # XML FORMAT
    def set_xml_format( self, sContainer_id, value ):
        if self.infdata_container.infdata_exist(sContainer_id):            
            infdata = self.infdata_container.get_infdata(sContainer_id)
            infdata.set_xml_format(value)
            self.infdata_container.set_infdata(sContainer_id, infdata)
            
    def get_xml_format( self, sContainer_id ):
        if self.infdata_container.infdata_exist(sContainer_id):      
            return self.infdata_container.get_infdata(sContainer_id).\
                   get_xml_format()

    # INPUT INFORMATION
    def set_input_information( self, sContainer_id, value ):
        if self.infdata_container.infdata_exist(sContainer_id):            
            infdata = self.infdata_container.get_infdata(sContainer_id)
            infdata.set_input_information(value)
            self.infdata_container.set_infdata(sContainer_id, infdata)

    def get_input_information( self, sContainer_id ):
        if self.infdata_container.infdata_exist(sContainer_id):      
            return self.infdata_container.get_infdata(sContainer_id).\
                   get_input_information()

    # OUTPUT INFORMATION
    def set_output_information( self, sContainer_id, value ):
        if self.infdata_container.infdata_exist(sContainer_id):            
            infdata = self.infdata_container.get_infdata(sContainer_id)
            infdata.set_output_information(value)
            self.infdata_container.set_infdata(sContainer_id, infdata)

    def get_output_information( self, sContainer_id ):
        if self.infdata_container.infdata_exist(sContainer_id):      
            return self.infdata_container.get_infdata(sContainer_id).\
                   get_output_information()
        
    # DATA
    def set_data( self, sContainer_id, value ):
        if self.infdata_container.infdata_exist(sContainer_id):            
            infdata = self.infdata_container.get_infdata(sContainer_id)
            infdata.set_data(value)
            self.infdata_container.set_infdata(sContainer_id, infdata)

    def get_data( self, sContainer_id ):
        if self.infdata_container.infdata_exist(sContainer_id):      
            return self.infdata_container.get_infdata(sContainer_id).get_data()
