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

_ = metro_util.init_translation('metro_xml_dtd')

def genxml_indent( iLvl ):
    return "    " * iLvl

def genxml_xml_header( ):
    return '<?xml version="1.0"?>'

def genxml_public_doctype( sPublic_id, sBackup_id ):
    return "<!DOCTYPE catalog PUBLIC \"%s\" \"%s\">" % (sPublic_id, sBackup_id)

def genxml_tag( sTag_name, lAttribute=[] ):
    sTag = ""
    sTag += "<" + sTag_name

    if len(lAttribute) > 0: 
        for tAttribute in lAttribute :
            sTag += ' %s="%s"' % (tAttribute[0],tAttribute[1]) 

    sTag += ">"

    return sTag

def genxml_close_tag( sTag_name ):
    return "</%s>" % (sTag_name)

def genxml_public_catalog_entry( sPublic_id, sUri ):

    lAtt = [("publicId", sPublic_id),
            ("uri", sUri)]
    sRslt = genxml_indent(1) + genxml_tag("public",lAtt)
    sRslt += genxml_close_tag("public") + "\n"

    return sRslt

def generate_dtd_catalog( ):
    sMessage = _("Generating METRo DTD catalog...")
    metro_logger.print_init_message(metro_logger.LOGGER_INIT_MESSAGE,
                                    sMessage)
    
    sCatalog = genxml_xml_header()
    sCatalog += "\n"

    sCatalog += genxml_public_doctype(
        "-//OASIS//DTD Entity Resolution XML Catalog V1.0//EN",
        "http://www.oasis-open.org/committees/entity/release/1.0/catalog.dtd")
    sCatalog += "\n"

    sCatalog += genxml_tag(
        "catalog",[("xmlns","urn:oasis:names:tc:entity:xmlns:xml:catalog")])
    sCatalog += "\n"

    sMetro_root_path = metro_util.get_metro_root_path()
    sMetro_catalog_path = sMetro_root_path + "/usr/share/metro/data/DTD/"

    sCatalog += genxml_public_catalog_entry(
        "-//Apple Computer//DTD PLIST 1.0//EN",
        sMetro_catalog_path + "plist.dtd")
    
    sCatalog += genxml_public_catalog_entry(
        "-//METRo//DTD FORECAST 1.0//EN",
        sMetro_catalog_path + "forecast.dtd")

    sCatalog += genxml_public_catalog_entry(
        "-//METRo//DTD OBSERVATION 1.0//EN",
        sMetro_catalog_path + "observation.dtd")

    sCatalog += genxml_public_catalog_entry(
        "-//METRo//DTD STATION 1.0//EN",
        sMetro_catalog_path + "station.dtd")

    sCatalog += genxml_close_tag("catalog") + "\n"

    #creation du fichier catalog
    sCatalog_filename = sMetro_catalog_path + "metro_catalog.xml"
    
    try:
        fCatalog = open(sCatalog_filename,'w')
    except IOError:
        fCatalog = None
        sError_message = _("can't create METRo DTD catalog file:'%s'") \
                         % (sCatalog_filename)
        metro_logger.print_init_message(metro_logger.LOGGER_INIT_ERROR,
                                        sError_message)
    else:
        #ecrire le header du log
        fCatalog.write(sCatalog)
        fCatalog.close()
        
        sSuccess_message = _("METRo DTD catalog file created with success.\n") +\
                           _("DTD catalog file:'%s'") % (sCatalog_filename)
        metro_logger.print_init_message(metro_logger.LOGGER_INIT_SUCCESS,
                                        sSuccess_message)

