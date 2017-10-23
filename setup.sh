#!/bin/bash
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

# SETUP TRAP
ERRMSG="\nERR - METRo Install - $progname : Script terminated due to
error.  Correct error and restart.\n\n"

trap 'echo -e $ERRMSG; exit 1' ERR

progname=`basename $0`

# Making sure we are in the directory where the script resides
cd `dirname $0`
installation_dir=`pwd`

metro_dir=metro

bCompile=1
sVerbose=""

# 'getopts' processes command line args to script.

# Usage: scriptname -options
# Note: dash (-) necessary

# Try invoking this script with
# 'scriptname -mn'
# 'scriptname -oq qOption'
# (qOption can be some arbitrary string.)

OPTERROR=33

if [ -z $1 ]
# Exit and complain if no argument(s) given.
then
    echo ""
    echo "Usage: $progname [OPTION] destination_path"
    echo ""
    echo "-c  : Will compile the METRo physic model instead of using"
    echo "      the provided binary. Need gfortran compiler."
    echo "      DEPRECATED, no longer do anything, setup.sh will"
    echo "      always compile the METRo physic model."
    echo ""
    echo "-v  : Verbose"
    echo ""
    echo "The metro directory will be created in the destination_path"
    echo ""
    echo "Ex: ./setup.sh /usr/local/"
    echo "    ./setup.sh /home/user/program/"
    exit 0
fi  


while getopts "cv" Option
do
  case $Option in
    c     ) bCompile=1;;
    v     ) sVerbose=-v;;
    *     ) echo ""
            echo "Usage: $progname [OPTION] destination_path"
            echo ""
            echo "-c  : Will compile the METRo physic model instead of using"
            echo "      the provided binary. Need gfortran compiler." 
            echo "      DEPRECATED, no longer do anything, setup.sh will"
            echo "      always compile the METRo physic model."
 	    echo ""
	    echo "-v  : Verbose"
            echo ""
            echo "The metro directory will be created in the destination_path"
            echo ""
            echo "Ex: ./setup.sh /usr/local/"
            echo "    ./setup.sh /home/user/program/"
            exit $OPTERROR;;
  esac
done

shift $(($OPTIND - 1))
# Decrements the argument pointer
# so it points to next argument.

destination_path=$1/$metro_dir

echo "* Starting METRo Installation *"
echo ""

if [ -d $destination_path ]; then
    echo "Warning target directory: $destination_path already exist."
    echo "Installing a different version of METRo over an existing one"
    echo "is not recommanded."
    echo "Do you want to continue? [y|n]"
    read answer
    if [ ! "$answer" = y ]; then
        echo "Exiting..."
        exit 0
    fi
fi

# check if gfortran library exist on the target system
echo "* Checking for libgfortran.so.1"
if ! locate libgfortran.so.1; then
    echo "----------------------------------------------------------"
    echo "WARNING!"
    echo "Could not find gfortran library on your system."
    echo "METRo model will be recompiled."
    echo "----------------------------------------------------------"
    bCompile=1
fi
echo ""
    
mkdir -p $destination_path/usr/share/metro/model/
mkdir -p $destination_path/usr/lib/metro/
if [ $bCompile == 1 ]; then
    echo "* Building physic model..."
    if [ ! -n "$PYTHON_INCLUDE" ] ; then
        echo "----------------------------------------------------------"
        echo "WARNING!"
        echo "No python path defined. setup.sh may not be able"
        echo "to properly install METRo."
        echo "Please set environment variable PYTHON_INCLUDE to your"
        echo "python include directory."
        echo "Ex: export PYTHON_INCLUDE=\"/usr/local/include/python2.3\""
        echo "----------------------------------------------------------"
	echo ""
    fi
    cd src/model
    ../../scripts/do_macadam clean
    ../../scripts/do_macadam $destination_path
    cd $installation_dir
#else
#    echo "* Use provided binary for physic model"
#    cp $sVerbose src/model/macadam.py.prebuilt $destination_path/usr/share/metro/model/macadam.py
#    cp $sVerbose src/model/_macadam.so.prebuilt $destination_path/usr/lib/metro/_macadam.so
fi
echo ""

echo "* Creating destination directory: "$destination_path
mkdir -p $destination_path
echo ""
echo "* Copying METRo files..."
echo ""

echo  "* Copying METRo data files to: "$destination_path/usr
find usr -not -regex ".*\.po" | cpio -pmud --quiet $sVerbose $destination_path/

echo "* Copying METRo programs files to: "$destination_path/usr/share/metro
cp $sVerbose src/frontend/*.py $destination_path/usr/share/metro
cp $sVerbose -r src/frontend/data_module $destination_path/usr/share/metro
cp $sVerbose -r src/frontend/executable_module $destination_path/usr/share/metro
cp $sVerbose -r src/frontend/external_lib $destination_path/usr/share/metro
cp $sVerbose -r src/frontend/toolbox $destination_path/usr/share/metro

#echo "* Copying METRo model python file to: "$destination_path/usr/share/metro/model
#if [ $bCompile == 1 ]; then
#    cp $sVerbose src/model/macadam.py          $destination_path/usr/share/metro/model/
#else
#    cp $sVerbose src/model/macadam.py.prebuilt $destination_path/usr/share/metro/model/macadam.py
#fi

#echo "* Copying METRo model to: "$destination_path/usr/lib/metro
#if [ $bCompile == 1 ]; then
#    cp $sVerbose src/model/_macadam.so $destination_path/usr/lib/metro/
#else
#    cp $sVerbose src/model/_macadam.so.prebuilt $destination_path/usr/lib/metro/_macadam.so
#fi

mkdir -p $destination_path/usr/share/doc/metro/
echo "* Copying METRo doc files to: "$destination_path/usr/share/doc/metro/
cp $sVerbose INSTALL LICENSE README.md README.devel $destination_path/usr/share/doc/metro/

echo "* Creating METRo log directory: "$destination_path/var/log
mkdir -p $destination_path/var/log


cd $installation_dir

mkdir -p $destination_path/usr/bin
echo "* Make link to METRo executable:"
echo "  $destination_path/usr/bin/metro -> $destination_path/usr/share/metro/metro.py"
ln -sf ../share/metro/metro.py $destination_path/usr/bin/metro  

echo ""
echo "---------------------------------------------------"
echo "METRo successfully installed in '$destination_path'"
echo "---------------------------------------------------"
echo ""
echo "* Installation done *"
echo ""
echo "To test the installation of METRo"
echo "---------------------------------"
echo "Go into the METRo directory:"
echo " 'cd $destination_path/usr/bin/'" 
echo "Launch METRo selftest:"
echo " 'python metro --selftest'"
echo "Compare the files:"
echo " 'diff ../share/metro/data/selftest/roadcast.xml ../share/metro/data/selftest/roadcast_reference.xml'"
echo "They should be identical except for the production-date."

