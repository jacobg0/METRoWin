#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
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
 Nom:         copy_msgid_msgstr

 Auteur:      Miguel Tremblay

 Date:        November 10th  2004

 Description: Prend un fichier .po et copy le contenu de chaque msgid dans
  le msgstr en bas de lui.
"""

import os
import sys

def copy_msgid_msgstr(sFilename):

    ######## Open file ##############################
    file_original_po = open(sFilename)
    sFile_ori_po = file_original_po.read()
    file_original_po.close()

    ######## Split the file to msgid ##########################
    l_msgid = sFile_ori_po.split('msgid')
    l_msgstr = sFile_ori_po.split('msgstr')
    l_file = l_msgstr
    # Display the msgid until msgstr is encontered
    for i in range(1,len(l_msgid)):
        sItem_msgid = l_msgid[i]
        sItem_msgstr = l_msgstr[i]
#        print sItem_msgid
#        print sItem_msgstr
        sReplace = sItem_msgid[:sItem_msgid.find('msgstr')]
#        print sReplace
        # Replace "" in msgstr by this string
        sItem_msgstr = sItem_msgstr.replace('""', 'msgstr' + sReplace,1)
        sItem_msgstr = sItem_msgstr[1:len(sItem_msgstr)]
        
#        print "---"
#        continue
        l_file[i] = sItem_msgstr
#        print "-----"


    file_translated_po = open(sFilename, 'w')
    file_translated_po.writelines(l_file)

    return

def main():
    if len(sys.argv) != 2:
        print "Usage: copy_msgid_msgstr.py filename.po"
        return
    
    copy_msgid_msgstr(sys.argv[1])
    
    
if __name__ == "__main__":
    main()



