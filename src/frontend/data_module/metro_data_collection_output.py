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

import copy

import metro_data
from metro_data_collection import Metro_data_collection

#===============================================================================
#
# Name: Metro_data_collection_output
#
# Description: Groupe de 2 objects Metro_data.
#              Le premier object (raw_data) contient les donnees brut produites
#              par le modele. Le second objet (controlled_data) contient les
#              donnees complete d'un roadcast
#
#              Des attributs concernant l'ensemble de la collection peuvent etre
#              conserve dans l'object. La liste de ces options peut etre passe
#              au constructeur et leur contenue modifier a l'aide des methodes
#              (get/set)_attribute. On peut aussi en ajoute lors de l'execution.
#
#===============================================================================

class Metro_data_collection_output(Metro_data_collection):

    def __init__( self, data, lData_attribute=[] ):
        Metro_data_collection.__init__(self,lData_attribute)

        self.raw_data = copy.deepcopy(data)
        self.raw_data.set_readonly(True)
        
        self.controlled_data = copy.deepcopy(data)

        self.subsampled_data = copy.deepcopy(data)
        self.subsampled_data.init_matrix(0,
                                         self.subsampled_data.\
                                         get_real_nb_matrix_col())


    def set_raw_data( self, data ):
        self.raw_data = copy.deepcopy(data)

    def set_controlled_data( self, data ):
        self.controlled_data = copy.deepcopy(data)

    def set_subsampled_data( self, data ):
        self.subsampled_data = copy.deepcopy(data)

    def get_raw_data( self ):
        return self.raw_data

    def get_controlled_data( self ):
        return self.controlled_data

    def get_subsampled_data( self ):
        return self.subsampled_data
