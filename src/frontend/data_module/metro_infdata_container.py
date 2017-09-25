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

from data_module import metro_infdata
from toolbox import metro_util

_ = metro_util.init_translation('metro_infdata_container')

# Exception
ERROR_INFDATA_CONTAINER = "MetroInfdataContainerError"

class Metro_infdata_container:

    def __init__( self ):
        self.dContainer = {}

    def __getitem__( self, index ):
        return self.dContainer[self.dContainer.keys()[index]]

    def add_infdata( self, infdata_object ):
        self.dContainer[infdata_object.get_name()] = infdata_object

    def infdata_exist( self, sInfdata_name ):
        return sInfdata_name in self.dContainer

    def get_infdata_reference( self, sInfdata_name ):
        if self.infdata_exist(sInfdata_name):
            return self.dContainer[sInfdata_name]        
        else:
            lInfdata_name = self.dContainer.keys()
            sInfdata_name_list = metro_util.list2string(lInfdata_name)
            sError = _("'%s' is not a valid infdata name\n") \
                     % (sInfdata_name) +\
                     _("Try one of the following infdata name:\n%s") \
                     % (sInfdata_name_list)
            raise ERROR_INFDATA_CONTAINER, sError
            return None

