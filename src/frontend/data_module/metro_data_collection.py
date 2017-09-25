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

import metro_logger
from toolbox import metro_util

_ = metro_util.init_translation('metro_data_collection')



#===============================================================================
#
# Name: Metro_data_collection
#
# Description: Classe de base pour les metro_data_collection
#              Des attributs concernant l'ensemble de la collection peuvent etre
#              conserve dans l'object. La liste de ces options doit etre passe
#              au constructeur et leur contenue modifier a l'aide des methodes
#              (get/set)_attribute.
#
# Exception: AttributeError
#
#===============================================================================

ERROR_ATTRIBUTE = "Attribute_error"

class Metro_data_collection:
    """
    Basic class for data collection
    Provide the method to manipulate attributes. Attributes are stored into a
    list.
    """
    def __init__( self, lData_attribute=[] ):

        # nom des attributs
        self.lAttribute_list =  lData_attribute
        
        # valeur des attributs
        self.lAttribute = [None]*len(self.lAttribute_list)
        
    #------------------
    # Attribute method
    #------------------

    def get_attribute( self, sAttribute_name ):
        if sAttribute_name in self.lAttribute_list:
            iAttribute = self.lAttribute_list.index(sAttribute_name)
            return self.lAttribute[iAttribute]
        else:
            sMessage = _("Invalid attribute name. Valid attribute name are:\n%s") \
                       % (str(self.lAttribute_list))
            raise ERROR_ATTRIBUTE, sMessage

    def set_attribute( self, sAttribute_name, value ):
        if sAttribute_name in self.lAttribute_list:
            iAttribute = self.lAttribute_list.index(sAttribute_name)
            self.lAttribute[iAttribute] = value
        else:
            sMessage = _("Invalid attribute name. Valid attribute name are:\n%s") \
                       % (str(self.lAttribute_list))
            raise ERROR_ATTRIBUTE, sMessage

    def append_attribute( self, sAttribute_name, value ):

        if sAttribute_name not in self.lAttribute_list:
            
            # valeur presente = value
            self.lAttribute.append(value)
            
            # Ajout a la liste des options disponnibles
            self.lAttribute_list.append(sAttribute_name)
        else:
            sMessage = _("Attribute name '%s' already used") % (sAttribute_name)
            raise ERROR_ATTRIBUTE, sMessage

    def get_attribute_list( self ):
        return self.lAttribute_list
