#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
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


"""

 Nom:         check_translation

 Auteur:      Miguel Tremblay

 Date:        November 10th  2004

 Description: Créer les fichiers .po correspondant au .py .
   Ecrit ces fichiers dans /tmp/translate
   Pour chacun de ces fichiers, il faut mettre la meme string qu'il y a dans
   msgid a l'interieur de msgstr.
   Compare ensuite les fichier dans /locale/en/LC_MESSAGES/*.po avec ceux
   contenu dans /tmp/translate
   S'il y a une difference, on fait un merge avec les fichiers dans en et fr.
   Le fichier issue du merge porte le nom filename_merge.po.
   On affiche la liste des fichiers qui ont ete modifies dans le fichier
   merge.txt

"""

import os
import os.path
import sys
import filecmp
from copy_msgid_msgstr import copy_msgid_msgstr

sTemporaryDirectory = '/tmp/metro_translation/'

def main():
    # Check if the .tar of the documentation is in argument.
    if len(sys.argv) < 2:
        sMessage = 'Usage: ' + sys.argv[0] + ' ../src/frontend/'
        print sMessage
        return
    else:
        check_translation(sys.argv[1])

def check_translation(sDirectory):
    # Get a list of all the files in the directory
    lAllFiles = []
    os.path.walk(sDirectory, listAllFile_directory, lAllFiles)
    # Get the .po file
    lPoFilepath = []
    lPoFilename = []
    # List of changed files
    lPoChanged = []
    for sFile in lAllFiles:
        sExtension = sFile[-2:]
        nIndice = sFile.rfind('en/LC_MESSAGES/')
        if nIndice < 0:
            continue
        sFilename = sFile[sFile.rfind('/')+1:len(sFile)-3]
        if sExtension == 'po':
            lPoFilepath.append(sFile)
            lPoFilename.append(sFilename)
    # Take only the .py files with a corresponding po file
    lPythonFilepath = []
    lPythonFilename = []
    for sFile in lAllFiles:
        sExtension = sFile[-2:]
        sFilename = sFile[sFile.rfind('/')+1:len(sFile)-3]
        if sExtension == 'py' and sFilename in lPoFilename:
            lPythonFilepath.append(sFile)
    # Create the temporary directory
    if not os.path.exists(sTemporaryDirectory):
        os.mkdir(sTemporaryDirectory)
    # Create the .po files.    
    for sFilepath in lPythonFilepath:
        sFilename = sFilepath[sFilepath.rfind('/')+1:len(sFilepath)-3]
        sPoFile = sTemporaryDirectory+sFilename+'.po'
        sCommand = 'pygettext -o ' +sPoFile +' '+ sFilepath
        # Create po file
        os.system(sCommand)
        # Copy directly msgid in msgstr
        copy_msgid_msgstr(sPoFile)
        # Get the path of the original po file
        for sPoFilepath in lPoFilepath:
            nIndice = sPoFilepath.rfind('/')
            if nIndice < 0:
                continue
            sPoFilename = sPoFilepath[nIndice+1:len(sPoFilepath)-3]
            if sFilename == sPoFilename:
                sOriginalPoFilepath = sPoFilepath
                break
        # Compare the file with the famous command "msgcmp"
        sCommand = 'msgcmp ' +sOriginalPoFilepath +' ' +sPoFile +\
                    " > /dev/null 2>&1"
        # If the files are not compatible, the sys.command returns
        #  something that is not 0.
        if os.system(sCommand):
            # Create the merge file for english
            sMergeFilenameEn = sFilename + '_merge_en.po'
            sCommand = 'msgmerge ' +sOriginalPoFilepath +' ' +sPoFile\
                       +' -o ' +sMergeFilenameEn +\
                       " > /dev/null 2>&1"
            os.system(sCommand)
            # Get the file in french
            sMergeFilenameFr =  sFilename + '_merge_fr.po'
            sPoFileFr = sPoFile.replace('/en/','/fr/')
            sOriginalPoFilepathFr = sOriginalPoFilepath.\
                                    replace('/en/','/fr/')
            sCommand = 'msgmerge ' +sOriginalPoFilepathFr +' ' +\
                       sPoFileFr\
                       +' -o ' +sMergeFilenameFr +\
                       " > /dev/null 2>&1"
            os.system(sCommand)

            # Add the file names in the list
            lPoChanged.append(sOriginalPoFilepathFr)
            lPoChanged.append(sOriginalPoFilepath)
            
            print sMergeFilenameFr
            print sMergeFilenameEn

    # Write the file if there is any changed
    if len(lPoChanged) > 0:
        lPoChanged = map(lambda x:x+"\n", lPoChanged)
        file_with_filenames = open('changed_files', 'w')
        file_with_filenames.writelines(lPoChanged)
    
####################################
# Name listAllFile_directory
#
# Parameters: list lFileNames : list of string to be returned with new string
#                representing files.
#             string sDir : directory in which an ls is performed.
#             list lFiles : list of files to append in the directory.
# 
# Author:  Ben Park
# See post: http://groups.google.com/groups?hl=en&lr=&safe=off&selm=4cc96c48.0204031030.53bfb69f%40posting.google.com
# 
####################################
def listAllFile_directory(lFileNames, sDir, lFiles):
    def f1(a,sDir=sDir):
        return os.path.join(sDir,a)
    lFiles2 = map(f1, lFiles)
    lFileNames.extend(lFiles2)

        
if __name__ == "__main__":
    main()


