#!/usr/bin/env python
# -*- coding: UTF8 -*-
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


import sys
import os
import string
import codecs

# Set encoding to latin-1.  Must reload the sys module because the
#  setdefaultencoding is deleted after the initialization of python.
#  See http://masl.gnomehack.com/?N18452CE9 for further documentation
reload(sys)
sys.setdefaultencoding('ISO-8859-1')
# Rebind standard output to support unicode caracters.
# Magic trick from the python cookbook, 3.18 Printing Unicode Characters
#  to Standard Output.
sys.stdout = codecs.lookup('ISO-8859-1')[-1](sys.stdout)

# Add the directories where we can do an import
# use of Plist_config/PListReader.py
pathInclude = sys.path[0] + '/external_lib'  
sys.path.append(pathInclude)

# use of _macadam (installed package)
pathInclude = sys.path[0] + '/../../lib/metro' 
sys.path.append(pathInclude)

# use of _macadam (devel)
pathInclude = sys.path[0] + '/../../usr/lib/metro' 
sys.path.append(pathInclude)

pathInclude = sys.path[0] + '/executable_module'
sys.path.append(pathInclude)

# set environment variable LANGUAGE and LC_ALL
if 'LANGUAGE' not in os.environ and 'LC_ALL' not in os.environ:
    os.environ['LANGUAGE'] = 'en'
# If language is set, check if its "en" or "fr"
elif 'LANGUAGE' in os.environ:
    if os.environ['LANGUAGE'] != 'en' and os.environ['LANGUAGE'] != 'fr':
        os.environ['LANGUAGE'] = 'en'
elif 'LC_ALL' in os.environ:   
    if os.environ['LC_ALL'] != 'en' and os.environ['LC_ALL'] != 'fr':
        os.environ['LC_ALL'] = 'en'

# set environment variable TZ at UTC
os.environ['TZ'] = "UTC"

import metro_logger
import metro_config
from toolbox import metro_date
from toolbox import metro_xml
from toolbox import metro_util

_ = metro_util.init_translation('metro')

def metro_execute_module(lObject_execution_sequence):
    """
    Load the module sequence for METRo execution.
    """
    
    i = 0
    iLen_object_execution_sequence = len(lObject_execution_sequence)
    while i < iLen_object_execution_sequence:
        object = lObject_execution_sequence[i]

        # module execution
        object.start()

        # send the results to the following module
        if i+1 < iLen_object_execution_sequence:
            target_object = lObject_execution_sequence[i+1]

            if object.get_send_type() == target_object.get_receive_type():
                object.send_data_to(lObject_execution_sequence[i+1])
            else:
                sMessage = _("Type mismatch between 2 metro module.\n") + \
                           _("%s is sending %s and\n") %\
                           (string.upper(object.__module__),
                            object.get_send_type_txtid()) + \
                            _("%s want to receive %s.") %\
                            (string.upper(target_object.__module__),
                             target_object.get_receive_type_txtid())
                metro_logger.print_message(metro_logger.LOGGER_MSG_STOP, \
                                           sMessage)

        # module cleanup 
        object.stop()
        i = i + 1


def metro_get_execution_sequence():
    """
    Fetch the METRo execution sequence.
    """

    metro_logger.print_init_message(metro_logger.LOGGER_INIT_MESSAGE,
                                    _("Construct METRo execution sequence:"))
    
    lModule_execution_sequence = metro_config.get_value\
                                 ("INIT_MODULE_EXECUTION_SEQUENCE")

    lObject_sequence = []

    # Creation of an object for each module and add everything
    #  in a list
    for sModule_name in lModule_execution_sequence:
        module = __import__(sModule_name)
        sClass_name = string.capitalize(sModule_name)
        #print sClass_name
        exec "tmp_object =  module." + sClass_name + "()"
        lObject_sequence.append(tmp_object)

    
    metro_logger.print_init_message(metro_logger.LOGGER_INIT_SUCCESS,
                                    _("METRo execution sequence ready"))
    return lObject_sequence


def metro_init():
    """
    Initialization of configuration.
    """
    metro_config.init()

    # Processing of command line arguments
    dCmdline_conf = metro_config.get_cmdline_conf(sys.argv)
    metro_config.process_command_line_parameter(dCmdline_conf)

    # Start METRo initialization
    sMessage = _("Initialising METRo %s") % (metro_config.CFG_METRO_VERSION)
    metro_logger.print_init_message(metro_logger.LOGGER_INIT_MESSAGE,
                                    sMessage)
    metro_logger.print_init_message(metro_logger.LOGGER_INIT_BLANK)

    # XML library initialization
    metro_xml.init()

    # Read the config file
    dFile_conf = metro_config.read_configuration_file(dCmdline_conf)

    # Combine the different configuration levels
    metro_config.overlay_configuration(dFile_conf, dCmdline_conf)

    # Configuration validation
    metro_config.validating_configuration()
    
    # Logger initialisation 
    metro_logger.init()

    # Fetch the module list that constitute de METRo
    #  execution sequence
    lObject_sequence = metro_get_execution_sequence()

    metro_logger.print_init_message(metro_logger.LOGGER_INIT_BLANK)
    metro_logger.print_init_message(metro_logger.LOGGER_INIT_MESSAGE,
                                    _("Initialisation done"))
    return lObject_sequence


def metro_start(lObject_execution_sequence):
    metro_execute_module(lObject_execution_sequence)

def metro_stop():
    metro_xml.stop()
    metro_logger.stop()


def main():

    lExec_sequence = metro_init()

    metro_start(lExec_sequence)

    metro_stop()


if __name__ == "__main__":

    main()

