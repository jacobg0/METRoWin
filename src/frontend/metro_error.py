# -*- coding: UTF8 -*-
#
# METRo : Model of the Environment and Temperature of Roads
# METRo is Free and is proudly provided by the Government of Canada
# Copyright (C) Her Majesty The Queen in Right of Canada, Environment Canada, 2010

#  Questions or bugs report: metro@ec.gc.ca
#  METRo repository: https://framagit.org/metroprojects/metro
#  Documentation: https://framagit.org/metroprojects/metro/wikis/home
#
#
# Code contributed by:
#  Miguel Tremblay - Canadian meteorological center
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
Name:        metro_error
Author:      Miguel Tremblay
Date:        07/05/2010

Description: General error class for METRo.

"""

from toolbox import metro_util

_ = metro_util.init_translation('metro_error')

class Metro_error(Exception):
    """
    Base class for exceptions in this module.
    """
    def __init__(self, inst):        
        self.sError = str(inst)

class Metro_import_error(Metro_error):
    """
    Error in importing a module
    """
    def __str__(self):
        """ Put the message in string only if it is a string"""        
        self.sError = _("Error in import: ") + self.sError
        return self.sError


class Metro_util_error(Metro_error):
    """
    Error in toolbox/metro_util.py.
    """
    def __str__(self):
        """ Put the message in string only if it is a string"""        
        self.sError = "\n" +  _("Error in metro_util.py: ") + self.sError
        return self.sError

class Metro_version_error(Metro_error):
    """
    METRo's version is too low or too high, error.
    """
    def __str__(self):
        """ Put the message in string only if it is a string"""        
        self.sError = "\n" +  _("METRo's version error: ") + self.sError
        return self.sError

class Metro_date_error(Metro_error):
    """
    Something went wrong with a date
    """
    def __str__(self):
        """ Put the message in string only if it is a string"""        
        self.sError = "\n" +  _("Date error: ") + self.sError
        return self.sError

class Metro_xml_error(Metro_error):
    """
    Something went wrong in parsing the XML
    """
    def __str__(self):
        """ Put the message in string only if it is a string"""        
        self.sError = "\n" + self.sError
        return self.sError

class Metro_input_error(Metro_error):
    """
    Error with input file or data.
    """
    def __str__(self):
        """ Put the message in string only if it is a string"""        
        self.sError = "\n" + _("Input error: ") +  self.sError
        return self.sError


class Metro_data_error(Metro_error):
    """
    Error with data.
    """
    def __str__(self):
        """ Put the message in string only if it is a string"""        
        self.sError = "\n" + _("Data error: ") +  self.sError
        return self.sError

