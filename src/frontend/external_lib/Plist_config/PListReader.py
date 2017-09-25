"""PListReader

Reads Apple's plist XML data structure serialization format and returns a
native Python data structure. In conjunction with XMLFilter, it should
be compatible with all versions of Python from 1.5.2 up, on all platforms.

Copyright Andrew Shearer 2003-2004
<mailto:awshearer@shearersoftware.com>
For the current version, see:
    http://www.shearersoftware.com/software/developers/plist/

Revision History:
2003-08-16  ashearer  Initial version
2003-09-04  ashearer  Support getRecommendedFeatures() & the XMLFilter features
                      API, and use it to disable feature_external_ges, allowing
                      parsing to work even while disconnected from the Internet
2004-02-14  ashearer  Use native booleans if available; minor changes to
                      documentation

Dependencies:
    XMLFilter module (optional). Provides compatibility for versions
        of Python without xml.sax support, such as the version of Python
        2.2 that shipped with Jaguar (Mac OS X 10.2). If XMLFilter isn't
        found, xml.sax.handler will be tried instead. See:
        http://www.shearersoftware.com/software/developers/xmlfilter/
        
    W3CDate module. Parses the W3C Date format (a subset of ISO 8601), which
        is the standard datetime format for plists. See:
        http://www.shearersoftware.com/software/developers/w3cdate/
        

Usage:
    import XMLFilter
    reader = PListReader()
    XMLFilter.parseFilePath(filePath, reader,
        features = reader.getRecommendedFeatures())
    result = reader.getResult()
    # result could be a Python dict, list, string, number, etc.

Notes: This class assumes the target file is a valid plist file. In
particular, the root element isn't checked to make sure that it's
"plist", and unknown elements are ignored. So it's more lax than a
validating parser. If nothing in the document was recognized, the result
will be Python's None value. If the known elements are corrupt, the
error messages may not be that helpful. Exceptions will generally be
thrown at the right times, but their contents could be improved.

License: dual-licensed under the Python License and MPSL 1.1 (Mozilla License).

"""

try:
    from XMLFilter import XMLSAXHandler, \
        feature_namespaces, feature_external_ges, feature_external_pes
except ImportError:
    try:
        from xml.sax.handler import ContentHandler as XMLSAXHandler, \
            feature_namespaces, feature_external_ges, feature_external_pes
        
    except ImportError:
        raise ImportError, "PListReader requires either the XMLFilter module (available separately from www.shearersoftware.com) or a version of Python with xml.sax support."

import W3CDate
import base64

class PListReader(XMLSAXHandler):
    def __init__(self):
        XMLSAXHandler.__init__(self)        
        self._currentKey = None             # pending key; can tell us we're in a dict
        self._text = None                   # accumulated text
        self._result = None                 # parsed Python data structure
        self._stack = []                    # stack for nested arrays/dicts
    
    def getRecommendedFeatures(self):
        """The recommended features (which clients should pass along to the
        SAX parser) disable namespace parsing and external entities.
        
        If external_ges aren't disabled, xml.sax.handler may try to load the DTD
        from Apple's web server, which prevents parsing when there's no Internet
        connection.""" 
        return {feature_namespaces: 0, feature_external_ges: 0, feature_external_pes: 0}
        
    # map plist element names to functions that make an empty Python object
    complexTypeConstructors = {'dict': dict, 'array': list}
    
    def startElement(self, name, attrs):
        constructor = self.complexTypeConstructors.get(name)
        if constructor is not None:
            # call constructor func, making an empty Python dict or list
            newItem = constructor()
            # add it to the current container; it will be populated in place
            self._handleValue(newItem)
            # push onto stack, making it the new "current container"
            self._stack.append(newItem)
        else:                               # not a complex type?
            self._text = ''                 # turn on text accumulation

    # map plist element names to functions that convert text into a Python object
    simpleTypeConverterFunctions = {
        'data': base64.decodestring, 'date': W3CDate.W3CDate,
        'integer': int, 'real': float, 'string': lambda x: x, 
        'true': lambda x: 1==1, 'false': lambda x: 0==1}
    
    def endElement(self, name):
        converter = self.simpleTypeConverterFunctions.get(name)
        if converter is not None:
            self._handleValue(converter(self._text))   # call converter func on text
            self._currentKey = None
        elif name == 'key':
            self._currentKey = self._text   # stash dict key for next _endValue
        elif name in ('array', 'dict'):
            self._stack.pop()               # array or dict was already updated in place
            self._currentKey = None
        self._text = None                   # turn off text accumulation
        
    def _handleValue(self, value):
        """
        Add a parsed value to the current container.
        The container could be a dict, array, or even the root.
        """
        if self._result is None:            # first item in file (the result's root)
            self._result = value
            self._stack.append(value)
        elif self._currentKey is not None:  # put value into dict; there was a key
            self._stack[-1][self._currentKey] = value
            self._currentKey = None
        else:                               # append value to array
            self._stack[-1].append(value)   # (must be array; there was no <key>)
            
    def characters(self, content):
        if self._text is not None:          # accumulate text
            self._text = self._text + content
    
    def getResult(self):
        return self._result

