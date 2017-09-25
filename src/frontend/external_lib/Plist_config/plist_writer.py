import sys
import types

class Plist_writer:

    def __indent( self, iLevel, iNb_space=4 ):
        return " " * iNb_space * iLevel

    def __write_header( self ):
        self.output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        self.output.write('<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n')
        self.output.write('<plist version="1.0">\n')
        
    def __write_footer( self ):
        self.output.write("</plist>\n")     

    def __dispatch_value( self, value, iLevel ):

        valueType = type(value)
    
        if valueType == types.DictType:
            self.__dump_dict(value, iLevel)
        elif valueType == types.ListType:
            self.__dump_list(value, iLevel)
        elif valueType == types.FloatType:
            self.__dump_float(value, iLevel)
        elif valueType == types.IntType or valueType == types.LongType:
            self.__dump_int(value, iLevel)
        elif valueType == types.BooleanType:
            self.__dump_bool(value, iLevel)
        elif isinstance(value,basestring):
            self.__dump_string(value, iLevel)
        else:
            self.output.write("Type error, can't create config file")
            # TODOFF raise an exception
            print "Error when generating config file. Type error"
            sys.exit(3)

    def __dump_string( self, sString, iLevel ):
        self.output.write("%s<string>%s</string>\n" % (self.__indent(iLevel),sString))

    def __dump_float( self, fNumber, iLevel ):
        self.output.write("%s<real>%s</real>\n" % (self.__indent(iLevel),fNumber))

    def __dump_int( self, iNumber, iLevel ):
        self.output.write("%s<integer>%s</integer>\n" % (self.__indent(iLevel),iNumber))

    def __dump_bool( self, bValue, iLevel ):
        if bValue == True:
            sBool = "true"
        else:
            sBool = "false"
        
        self.output.write("%s<%s/>\n" % (self.__indent(iLevel),sBool))

    def __dump_list( self, lList, iLevel ):
        # Imprime tag list
        self.output.write(self.__indent(iLevel) + "<array>\n")
        
        for item in lList:
            self.__dispatch_value(item, iLevel+1)

        self.output.write(self.__indent(iLevel) + "</array>\n")


    def __dump_dict( self, dDict, iLevel ):

        self.output.write(self.__indent(iLevel) + "<dict>\n")

        lKeys = dDict.keys()
        lKeys.sort()
    
        for key in lKeys:
            self.output.write("%s<key>%s</key>\n" % (self.__indent(iLevel + 1),key))
            value = dDict[key]
            self.__dispatch_value(value, iLevel+1)
 
        self.output.write(self.__indent(iLevel) + "</dict>\n")

    
    def __dump_structured( self, dDict, iLevel, bDump_all ):

        if  bDump_all == True:
            iTreshold = -1
        else:
            iTreshold = 0
            
        self.output.write(self.__indent(iLevel) + "<dict>\n")
        
        lKeys = dDict.keys()
        lKeys.sort()
    
        for key in lKeys:
            if dDict[key]['FROM'] > iTreshold:
                sComments = dDict[key]['COMMENTS']
                self.output.write(self.__indent(iLevel+1) + "<!-- " + sComments + " -->\n")
                self.output.write("%s<key>%s</key>\n" % (self.__indent(iLevel + 1),key))
            
                value = dDict[key]['VALUE']
                self.__dispatch_value(value, iLevel+1)
                self.output.write("\n")

        self.output.write(self.__indent(iLevel) + "</dict>\n")

    # Si bStructured = False, tous le dictionnaire sera ecrit dans le fichier
    # de configuration
    #
    # Si bStructured = True, le premier niveau du dictionnaire doit etre
    # de la forme suivante:
    # {*key1*:{FROM:integer,
    #          COMMENTS:string,
    #          VALUE,*value*},
    #  *key2*:{FROM:integer,
    #          COMMENTS:string,
    #          VALUE,*value*}
    #  ...
    # }
    # NB: FROM    : Permet de decider si la valeur doit etre sauvegarde.
    #               Est sauvegarder si > 0 
    #     COMMENTS: Imprime un commentaire en haut de la valeur sauvegarder
    #     VALUE   : La valeur *value* sauvegarder pour la configuration
    #               identifie par *key#*
    def write( self, sFilename, dConfig, bStructured=False, bDump_all=False ):

        try:
            self.output = open(sFilename, 'w')
        except IOError, errorInfo:
            raise IOError, errorInfo

        self.__write_header()

        if bStructured == True:
            self.__dump_structured(dConfig, 0, bDump_all)
        else:
            self.__dump_dict(dConfig, 0)

        self.__write_footer()

        self.output.close()

