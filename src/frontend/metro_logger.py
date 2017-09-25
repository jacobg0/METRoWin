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

import time
import sys
import string

import metro_config
from toolbox import metro_date
from toolbox import metro_util

_ = metro_util.init_translation('metro_logger')

"""
Name:         metro_logger
Author:      Francois Fortin
Date:        30/03/2004

Description:  Module used to centralize the writing of METRo error
               message. This logger as many verbosity level.
"""

# niveau de verbositer du logger
LOGGER_VERBOSE_LEVEL_NOLOG   = 9999 # setting special pour desactiver le logger
LOGGER_VERBOSE_LEVEL_MINIMAL = 20
LOGGER_VERBOSE_LEVEL_NORMAL  = 10
LOGGER_VERBOSE_LEVEL_FULL    = 5
LOGGER_VERBOSE_LEVEL_DEBUG   = 0

iLogger_verbose_level = LOGGER_VERBOSE_LEVEL_NOLOG 

# categorie du message
LOGGER_MSG_DEBUG         = 1   # show if verbosity = DEBUG
LOGGER_MSG_INFORMATIVE   = 6   # show if verbosity = FULL
LOGGER_MSG_EXECSECONDARY = 2   # show if verbosity = FULL
LOGGER_MSG_WARNING       = 11  # show if verbosity = ( FULL || NORMAL )
LOGGER_MSG_EXECPRIMARY   = 12  # show if verbosity = ( FULL || NORMAL )
LOGGER_MSG_CRITICAL      = 21  # always displayed
LOGGER_MSG_STOP          = 22  # alwayds displayed

LOGGER_MSG_DEBUG_TXTID         = _("DEBUG      ")
LOGGER_MSG_INFORMATIVE_TXTID   = _("INFORMATIVE")
LOGGER_MSG_EXECSECONDARY_TXTID = _("EXECUTION  ")
LOGGER_MSG_WARNING_TXTID       = _("WARNING    ")
LOGGER_MSG_EXECPRIMARY_TXTID   = _("EXECUTION  ")
LOGGER_MSG_CRITICAL_TXTID      = _("CRITICAL   ")
LOGGER_MSG_STOP_TXTID          = _("STOP       ")
LOGGER_MSG_UNDEFINED_TXTID     = _("UNDEFINED  ")
LOGGER_MSG_EMPTY_TXTID         = "             "

#Condition for a message to be displayed:
# message's category > logger verbosity level

# Message's type for the message to be print before
# METRo initialization phase
LOGGER_INIT_MESSAGE = 0
LOGGER_INIT_SUCCESS = 1
LOGGER_INIT_ERROR   = 2
LOGGER_INIT_BLANK   = 3



bIs_initialised = False

def write_log_header( fLog_file, iVerbosity ):
    """
    Name:          write_log_header

    Parametres:   I fLog_file  : fichier de log
                  I iVerbosity : niveau de verbosite

    Return:     none

    Description: Write an header for a new log session.
                  The header includes:
                    * METRo's version number
                    * Starting time
                    * Complete command line to initiate METRo
                    * Verbosity level
    """    

    fLog_file.write("\n\n============================================\n")

    fLog_file.write(_("METRo version   : "))
    fLog_file.write(metro_config.get_metro_version())
    fLog_file.write("\n")

    line = _("METRo started   : %s %s") \
           % (time.asctime(time.localtime(time.time())),
              metro_date.get_system_tz())
    fLog_file.write(line)
    fLog_file.write("\n")

    fLog_file.write(_("command line    : "))
    fLog_file.write(string.join(sys.argv,' '))
    fLog_file.write("\n")

    fLog_file.write(_("logger verbosity: "))
    if iVerbosity == LOGGER_VERBOSE_LEVEL_NOLOG:
        fLog_file.write(_("No Log"))
    elif iVerbosity == LOGGER_VERBOSE_LEVEL_MINIMAL:
        fLog_file.write(_("Minimal"))
    elif iVerbosity == LOGGER_VERBOSE_LEVEL_NORMAL:
        fLog_file.write(_("Normal"))
    elif iVerbosity == LOGGER_VERBOSE_LEVEL_FULL:
        fLog_file.write(_("Full"))
    elif iVerbosity == LOGGER_VERBOSE_LEVEL_DEBUG:
        fLog_file.write(_("Debug"))
    else:
        fLog_file.write(_("Undefined"))
    fLog_file.write("\n")

    fLog_file.write("\n============================================\n")


def init( ):
    """
    Name: init
    Parameters: none
    Return: none
    Description: Logger verbosity level initialization.
    """
    
    global iLogger_verbose_level
    global bLogger_shell_display
    global sLogger_filename
    global fLogger_file
    global bIs_initialised

    # Pre-initialization in order to not log logger init...
    iLogger_verbose_level     = LOGGER_VERBOSE_LEVEL_NOLOG
    bLogger_shell_display     = False

    sMessage = _("Starting METRo logger")
    print_init_message(LOGGER_INIT_MESSAGE,sMessage)

    # Retrieve configuration values
    sTmp_logger_filename      = metro_config.get_value("FILE_LOGGER_FILENAME")
    iTmp_logger_verbose_level = \
        metro_config.get_value("INIT_LOGGER_VERBOSE_LEVEL")
    bTmp_logger_shell_display = \
        metro_config.get_value("INIT_LOGGER_SHELL_DISPLAY")

    # Initialization
    sLogger_filename      = sTmp_logger_filename
    iLogger_verbose_level = iTmp_logger_verbose_level
    bLogger_shell_display = bTmp_logger_shell_display

    # Open log file
    try:
        fLogger_file = open(sLogger_filename,'a')
    except IOError:
        fLogger_file = None
        sError_message = _("can't open/create logger file:'%s'") \
                         % (sLogger_filename)
        print_init_message(LOGGER_INIT_ERROR,
                           sError_message)
    else:
        # Log header writing
        write_log_header(fLogger_file, iLogger_verbose_level)
        
        sSuccess_message = _("METRo logger started, log file:'%s'") \
                           % (sLogger_filename)
        print_init_message(LOGGER_INIT_SUCCESS,
                           sSuccess_message)

    bIs_initialised = True

        
def stop():
    """
    Name: stop
    Parameter: none
    Return: none
    Description: Log closure.
    """
    if fLogger_file:
        fLogger_file.close()

#-------------------------------------------------------------------------------
#
# Nom:          print_message
#
# Parametres:   I iMessage_category : categorie du message
#               I sMessage          : message
#
# Retourne:     aucun
#
# Descriptions: sauvegarde d'un message dans le fichier log. Un message est
#               sauvegarde seulement si sont niveau de gravite est superieur
#               au niveau de verbosite du logger. De facon optionnel, le message
#               peut etre aussi affiche dans le shell.
#
#-------------------------------------------------------------------------------
def print_message( iMessage_category, sMessage ):
    """
    Name: print_message

    Parameter:  I iMessage_category : message category
                I sMessage          : message

    Return: none

    Description: Write a message in the log file. A message is written only
                  if it's verbosity level is superior from the logger verbosity.
                  In option, the message can be displayed in shell.
   """

    # Determine the text identifier for the category of the message
    if iMessage_category == LOGGER_MSG_DEBUG:
        sMessage_category_string = LOGGER_MSG_DEBUG_TXTID
    elif iMessage_category == LOGGER_MSG_INFORMATIVE:
        sMessage_category_string = LOGGER_MSG_INFORMATIVE_TXTID
    elif iMessage_category == LOGGER_MSG_EXECSECONDARY:
        sMessage_category_string = LOGGER_MSG_EXECSECONDARY_TXTID
    elif iMessage_category == LOGGER_MSG_WARNING:
        sMessage_category_string = LOGGER_MSG_WARNING_TXTID
    elif iMessage_category == LOGGER_MSG_EXECPRIMARY:
        sMessage_category_string = LOGGER_MSG_EXECPRIMARY_TXTID
    elif iMessage_category == LOGGER_MSG_CRITICAL:
        sMessage_category_string = LOGGER_MSG_CRITICAL_TXTID
    elif iMessage_category == LOGGER_MSG_STOP:
        sMessage_category_string = LOGGER_MSG_STOP_TXTID
    else:
        sMessage_category_string = LOGGER_MSG_UNDEFINED_TXTID


    # Check if the message should be logged
    if iMessage_category > iLogger_verbose_level:

        # Linefeed adjustment for the text in the file to be correctly aligned.
        sMessage = string.replace(sMessage,
                                  "\n",
                                  "\n" + LOGGER_MSG_EMPTY_TXTID)

        if fLogger_file:
            try:
                fLogger_file.write(sMessage_category_string + ": "+ sMessage + '\n')
            except:
                sLine = _("%s unexpected error, can't write message in the log file: %s") \
                        % (LOGGER_MSG_CRITICAL_TXTID,sLogger_filename)
                print sLine

        # Control if the message should be displayed in the shell
        if bLogger_shell_display == True:
            print (sMessage_category_string + ": " + sMessage).encode('ISO-8859-1')

    # Warn the user in the case of an error asking the execution to be stopped.
    if iMessage_category == LOGGER_MSG_STOP:
        print "\n\n------------------------------------------------------------------------"
        print _("An unrecoverable error has occured, see details in the log file: ")
        print sLogger_filename.encode('ISO-8859-1')

        if iLogger_verbose_level != LOGGER_VERBOSE_LEVEL_FULL:
            print "\n"
            print _("Lauching METRo with full logging capability may help you trace the error.")

        print "-------------------------------------------------------------------------"
        sys.exit(1)

def print_blank_line(iMessage_category):
     # Control if the message should be logged.
    if iMessage_category > iLogger_verbose_level:
        if fLogger_file:
            fLogger_file.write("\n")

        #  Control if the message should be displayed in the shell
        if bLogger_shell_display == True:
            print ""

def print_init_message( iType, sMessage="" ):
    """
    Print the message on the shell only.
    """

    if iType == LOGGER_INIT_ERROR:
        sMessage_leading_id = "[!!] "
    elif iType == LOGGER_INIT_SUCCESS:
        sMessage_leading_id = "[ok] "
    elif iType == LOGGER_INIT_MESSAGE:
        sMessage_leading_id = "* "
    elif iType == LOGGER_INIT_BLANK:
        sMessage_leading_id = ""
    else:
        sMessage_leading_id = ""
        
    sMessage = string.replace(sMessage,
                              "\n",
                              "\n" + "     ")

    print (sMessage_leading_id + sMessage)


def is_initialised( ):
    return bIs_initialised

