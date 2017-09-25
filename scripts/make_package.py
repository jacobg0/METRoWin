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


#
# Every file in the source directories is listed separatly so that we don't 
# include unwanted files.  This way, we are forced to consider what goes in the 
# package and what doesn't each time we make modifications. We don't blindly 
# add a directory with all the temporary and test files and it helps us to keep
# clean the distribution package.
#

sPackage_list = \
              """
src/frontend/metro.py
src/frontend/metro_config.py
src/frontend/metro_logger.py
src/frontend/metro_error.py
src/frontend/__init__.py

src/frontend/toolbox/metro_config_validation.py
src/frontend/toolbox/metro_constant.py
src/frontend/toolbox/metro_date.py
src/frontend/toolbox/metro_dom2metro_handler.py
src/frontend/toolbox/metro_metro2dom_handler.py
src/frontend/toolbox/metro_physics.py
src/frontend/toolbox/metro_util.py
src/frontend/toolbox/metro_xml.py
src/frontend/toolbox/metro_xml_dtd.py
src/frontend/toolbox/metro_xml_libxml2.py
src/frontend/toolbox/__init__.py

src/frontend/data_module/metro_data.py
src/frontend/data_module/metro_data_collection.py
src/frontend/data_module/metro_data_collection_input.py
src/frontend/data_module/metro_data_collection_output.py
src/frontend/data_module/metro_data_station.py
src/frontend/data_module/metro_infdata.py
src/frontend/data_module/metro_infdata_container.py
src/frontend/data_module/__init__.py

src/frontend/executable_module/metro_dom2metro.py
src/frontend/executable_module/metro_metro2dom.py
src/frontend/executable_module/metro_model.py
src/frontend/executable_module/metro_module.py
src/frontend/executable_module/metro_postprocess.py
src/frontend/executable_module/metro_postprocess_round_roadcast.py
src/frontend/executable_module/metro_postprocess_subsample_roadcast.py
src/frontend/executable_module/metro_preprocess.py
src/frontend/executable_module/metro_preprocess_combine.py
src/frontend/executable_module/metro_preprocess_fsint2.py
src/frontend/executable_module/metro_preprocess_interpol_forecast.py
src/frontend/executable_module/metro_preprocess_interpol_observation.py
src/frontend/executable_module/metro_preprocess_qa_qc_observation.py
src/frontend/executable_module/metro_preprocess_qa_qc_forecast.py
src/frontend/executable_module/metro_preprocess_qa_qc_station.py
src/frontend/executable_module/metro_preprocess_sunshadw.py
src/frontend/executable_module/metro_preprocess_validate_input.py
src/frontend/executable_module/metro_read.py
src/frontend/executable_module/metro_read_forecast.py
src/frontend/executable_module/metro_read_observation.py
src/frontend/executable_module/metro_read_observation_ref.py
src/frontend/executable_module/metro_read_station.py
src/frontend/executable_module/metro_string2dom.py
src/frontend/executable_module/metro_string2dom_forecast.py
src/frontend/executable_module/metro_string2dom_observation.py
src/frontend/executable_module/metro_string2dom_observation_ref.py
src/frontend/executable_module/metro_string2dom_station.py
src/frontend/executable_module/metro_write.py
src/frontend/executable_module/metro_write_forecast.py
src/frontend/executable_module/metro_write_roadcast.py
src/frontend/executable_module/metro_validate.py
src/frontend/executable_module/metro_validate_forecast.py
src/frontend/executable_module/metro_validate_observation.py
src/frontend/executable_module/metro_validate_observation_ref.py
src/frontend/executable_module/metro_validate_station.py

src/frontend/external_lib/Sun.py
src/frontend/external_lib/W3CDate.py
src/frontend/external_lib/__init__.py
src/frontend/external_lib/Plist_config/PListReader.py
src/frontend/external_lib/Plist_config/__init__.py
src/frontend/external_lib/Plist_config/plist_reader.py
src/frontend/external_lib/Plist_config/plist_writer.py
src/frontend/external_lib/fpconst.py
src/frontend/external_lib/sunpos.py

src/model/array2matrix.f
src/model/balanc.f
src/model/constPhys.f
src/model/coupla.f
src/model/flxsurfz.f
src/model/grille.f
src/model/initial.f
src/model/lib_gen.f
src/model/lib_therm.f
src/model/macadam.c
src/model/macadam.h
src/model/macadam.i
src/model/number.h

scripts/check_translation.py
scripts/copy_msgid_msgstr.py
scripts/create_mo.py
scripts/do_macadam
scripts/make_package.py

usr

README
LICENSE
INSTALL
setup.sh

"""




import string
import sys
import os
import re
import shutil

VERSION_FILE = "../src/frontend/metro_config.py"
LINE_REGEX = 'CFG_METRO_VERSION\s*\=\s*[\"|\'][0-9]\.[0-9]\.[0-9][\"|\']'
VERSION_REGEX = '[0-9]\.[0-9]\.[0-9]'

def chomp(x):
    while x != "" and x[-1] in "\r\n":
        x = x[:-1]
    return x

def extract_version_number( sFilename ):

    sVersion_number = None
    
    file = open(sFilename)
    text = file.read()
    file.close()
    
    match_version_line =\
        re.compile(LINE_REGEX)
    
    match_version_number = re.compile(VERSION_REGEX)
    
    match_obj_version_line = match_version_line.search(text)
    
    if match_obj_version_line:
        start, stop = match_obj_version_line.span(0)
        sVersion_line = text[start:stop]
        match_obj_version_number = match_version_number.search(sVersion_line)
        if match_obj_version_number:
            start, stop = match_obj_version_number.span(0)
            sVersion_number = sVersion_line[start:stop]
    else:
        print "Could not find the line containing the version number.\n" +\
        "The regex is: '%s'." % LINE_REGEX
    return sVersion_number


sVersion_number = extract_version_number(VERSION_FILE)

if not sVersion_number:
    print "Could not find version number in file:'%s'. Aborting" % VERSION_FILE
    sys.exit(1)

sMetro_dir = "metro-" + sVersion_number

# get path of metro parent directory

lPath = string.split(sys.path[0],"/")
sSvn_root_dir = lPath[-2]
sRoot_path = string.join(lPath[:-2],"/")
sMetro_real_dir = string.join(lPath[:-1],"/")
sPackage_path = string.join(lPath[:-2],"/")

# add leading metro directory name to each filename
sPackage_list = string.replace(sPackage_list,"\n","\n" + sSvn_root_dir + "/")

# replace \n by a space character
sPackage_list = string.replace(sPackage_list,"\n"," ")

# remove any single sMetro_dir entry
sPackage_list = sPackage_list + " "

# do it 2 time (dirty hack)
sPackage_list = string.replace(sPackage_list," " + sSvn_root_dir + "/ "," ")
sPackage_list = string.replace(sPackage_list," " + sSvn_root_dir + "/ "," ")

# copy model binary to lib
#shutil.copy2( sRoot_path + "/" + sSvn_root_dir + "/usr/lib/metro/_macadam.so",
#              sRoot_path + "/" + sSvn_root_dir + "/src/model/_macadam.so.prebuilt")
#shutil.copy2( sRoot_path + "/" + sSvn_root_dir + "/usr/share/metro/model/macadam.py",
#              sRoot_path + "/" + sSvn_root_dir + "/src/model/macadam.py.prebuilt")


#tar command
sTarCommand = "tar cjvf " +  sPackage_path + "/metro-" + sVersion_number + \
           ".tar.bz2 --exclude .svn --transform 's,^%s/,%s/,' " % (sSvn_root_dir,sMetro_dir) + " -C " + \
           sRoot_path + " " + sPackage_list

#execute tar command
print 'Executing', sTarCommand
os.system(sTarCommand)

#sign command
sSignCommand = "gpg --detach-sign " + sPackage_path + "/metro-" + sVersion_number + ".tar.bz2"

#sign package
print "\nMake a detached signature: '" + sSignCommand + "'"
os.system(sSignCommand)


# cleanup
print "\n* Cleanup *"

print ""
print 
print "* Package Creation Done *\n"
print "The METRo Package is located here:"
print "'" + sPackage_path + "/metro-" + sVersion_number + ".tar.bz2" + "'"
print ""
print "The METRo Package signature is located here:"
print "'" + sPackage_path + "/metro-" + sVersion_number + ".tar.bz2.sig" + "'"
