#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
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


"""

 Nom:         create_mo

 Auteur:      Miguel Tremblay

 Date:        November 17th  2004

 Description: Créer les fichiers .mo correspondant au .po
                dans un répertoire.

"""

import sys
import os

def create_mo(sFile_with_filenames):

    file_with_filenames = open(sFile_with_filenames)    
    lPoFiles = file_with_filenames.readlines()

    for sPoFile in lPoFiles:
        sMoFile = sPoFile[:-3]+'mo'
        sCommand = 'msgfmt -o ' +sMoFile +' ' +sPoFile
        print sCommand
        os.system(sCommand)



def main():
    # Check if the .tar of the documentation is in argument.
    if len(sys.argv) < 2:
        sMessage = 'Usage: ' + sys.argv[0] + ' files.txt'
        print sMessage
        return
    else:
       create_mo(sys.argv[1])

        
if __name__ == "__main__":
    main()


