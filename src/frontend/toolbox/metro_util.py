# -*- coding: iso-8859-15 -*-
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

"""
 Name:	 metro_util.py
 Description: Miscelleneous functions for METRo
 Notes: The language is set here because metro can be used
 as a library and metro_util is the module that every other module loads.
 Thus, the language setting that are used through metro is always set if
 this code is in the metro_util module.

 metro_logger cannot be invoked here since this module is imported in
 metro_logger. Errors must raised here must be catched elsewhere and then
 be logged through this module, if possible.
"""

import os
import metro_error

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


import sys
import string
import math

from distutils.version import LooseVersion
from gettext import gettext as _
import gettext
import numpy

import metro_constant

def import_name( module_path, module_name ):
    """
    return a module object import from module_path.
    """
    try:
        module = __import__(module_path, globals(), locals(), [module_name])
    except ImportError:
        return None
    return vars(module)[module_name]


def get_metro_root_path( ):
    """
    Return the root path of METRo package.
    """
    lPath = string.split(sys.path[0],"/")
    if lPath[-1] == "frontend":
        sRoot_path = string.join(lPath[:-2],"/")
    elif lPath[-1] == "bin":
        sRoot_path = string.join(lPath[:-1],"/")
    elif lPath[-1] == "metro":
        sRoot_path = string.join(lPath[:-3],"/")
    else: # Check if metro_util is used as a library
        lPythonPath =  string.split(os.environ['PYTHONPATH'], ":")
        for sPath in lPythonPath:
            lPath = string.split(sPath,"/")
            if lPath[-2] == "frontend":
                sRoot_path = string.join(lPath[:-3],"/")
                return sRoot_path
        # Nothing have been found
        sError = _("The executable 'metro.py' must be in one of the following directory:\n") +\
                 _("metro_directory/src/frontend' or 'metro_directory/usr/lib/metro'.\n") +\
                 _("The following path is not valid: '%s'.\n\n") % (sys.path[0]) +\
                 _("Aborting execution of METRo.\n")
        print sError
        sys.exit(1)
   
    return sRoot_path

def get_exec_root_path( ):
    return sys.path[0]

#########
# Ugly way done in order to use the function get_metro_root_path.
#  We can then use the underscore for the translation with gettext.
#########
t = gettext.translation('metro_util', get_metro_root_path() +\
                        '/usr/share/locale')
_ = t.gettext
    

def test_import( sModule_name ):
    """
    Used to test check if a module is present.
    """

    try:
        sCode = "import " + sModule_name
        exec sCode
    except (SyntaxError, ImportError, EOFError), inst:
        raise metro_error.Metro_import_error(str(inst))

def test_function_existence( sModule_name, sFunction_name ):
    """
    Utiliser pour tester la presence d'une fonction dans un module.
    """
    
    try:
        sCode_import = "import " + sModule_name
        exec sCode_import
        sCode_function = "func_object = " + sModule_name + "." + sFunction_name
        exec sCode_function
    except (SyntaxError, ImportError, AttributeError), inst:
        raise metro_error.Metro_import_error(inst)

    
def join_dictionaries(dDict1, dDict2):
    lKeys = dDict1.keys() + dDict2.keys()
    lValues = dDict1.values() + dDict2.values()

    i = 0
    dDict3 = {}
    while i < len(lKeys):
        dDict3[lKeys[i]] = lValues[i]
        i = i + 1

    return dDict3



def list2string( lList ):

    if len(lList) > 0:
        rslt =  str(lList[0])

        for element in lList[1:]:
            rslt = rslt + ", " + str(element)

    else:
        rslt = ""

    return rslt



def interpolate(xArray, yArray):
    """
     Name: interpolate

     Parameters: [[I] Numeric.Array lXArray : The value of x to
                      interpolate.  Must be of constant distance between
                      two consecutives X.]
                 [[I] Numeric.Array lYArray: The value of y to
                      interpolate.]
                 [[I] int iIncrement: The increment to use
                      between two X consecutes values to get the new X

     Returns: list The interpolate Y value. Throw an exception in case
               of error.

     Functions Called: [interp() ]
 
     Description: This function do the interpolation of a one dimension
                  function.  The x and the corresponding y value are given
                  (i.e. y[n] correspond to x[n]) The value of x must be
                  evenly spaced.
                  The increment value is set in metro_constant by the
                  value of fTimeStep and tells how to
                  increment the value between two consecutive x.

     Notes: This function needs the NumArray package. We assume that
              the values do no need to be sorted (i.e. they are in order).

     Revision History:
     Author		Date		Reason
     Miguel Tremblay      June 30th 2004   To replace the linear
     interpolation of fortran code
    """
    iIncrement = metro_constant.fTimeStep
    # Check if the size of the array is ok.
    iLenXArray = len(xArray)
    iLenYArray = len(yArray)
    if ( iLenXArray != iLenYArray):
        sMetroUtilWarning = _("In interpolate, the arrays does not") +\
                            _("have the same length. %d != %d\n") %\
                              (iLenXArray, iLenYArray )
        # Error should be thrown ? Text won't be in metro_logger...
        print sMetroUtilWarning
        if  iLenYArray < iLenXArray:
            sMetroUtilWarning = _("Padding Y array with average at the end.")
            npPadd = numpy.zeros(iLenXArray - iLenYArray)+yArray.mean()
            yArray = numpy.concatenate((yArray,npPadd))
        else:
            raise metro_error.Metro_util_error(sMetroUtilWarning)
        
    elif (iLenXArray < 2):
        sMetroUtilError = _("In interpolate, the arrays have only one value (1)")
        raise  metro_error.Metro_util_error(sMetroUtilError)
    elif (xArray[1]-xArray[0] < iIncrement):
        sMetroUtilError = _("In interpolate, iIncrement is too big. \n")+\
                          _("Space between two values in xArray:")+\
                          "xArray[0]: %f xArray[1]:%f \n Increment=%f" \
                          % (xArray[0], xArray[1], iIncrement)
        raise metro_error.Metro_util_error(sMetroUtilError)

    # Build the new x
    xArrayInt = numpy.arange(xArray[0],xArray[iLenXArray-1],iIncrement)
    yArrayInt = interp(yArray,xArray, xArrayInt)

    return numpy.array(yArrayInt)


def shift_left(npInput, fValueAdded=0):
    """
    Name: shift_left
    
    Parameters: [[I] numpy npInput : The array that the value will be
                                     be shifted left]
                [[I] double fValueAdded=0 : The value to be added at left

    Returns: numpy npOutput: The array with the value shifted

    Functions Called:  numpy.take
                       numpy.concatenate

    Description: This method shift the value of the array at left, i.e.
                 npInput[n] becomes npInput[n-1] for all n in [1..len(npInput)-1].  The
                 value fValueAdded is added at the end,
                 i.e. npInput[len(npInput)-1]=fValueAdded

     Notes: npInput must be one dimension.

     Revision History:
     Author		Date		Reason
     Miguel Tremblay    July 2nd         Tired of always doing the same thing.

     """
    # Check the dimension
    if (npInput.shape <= 0):
        sMetroUtilError = _("In shift_left, npInput is not of size (1,).\n")+\
                          "len(npInput.shape)=%s"\
                          % (len(npInput.shape))
        raise metro_error.Metro_util_error(sMetroUtilError)

    # Cut the first value
    npOutput  = numpy.take(npInput,\
                              numpy.arange(1, len(npInput)))
    npToBeCat = numpy.array([fValueAdded])
    npOutput = numpy.concatenate((npOutput, npToBeCat))

    return npOutput


def shift_right(npInput, fValueAdded=0):
    """
    
    Name: shift_right

    Parameters: [[I] numpy npInput : The array that the value will be
                                     be shifted right]
                [[I] double fValueAdded=0 : The value to be added at the
                                            beginning of the array

     Returns: numpy npOutput: The array with the value shifted

     Functions Called:  numpy.take
                        numpy.concatenate

     Description: This method shift the value of the array at right, i.e.
       npInput[n] becomes npInput[n+1] for all n in [0..len(npInput)-2].  The
       value fValueAdded is added at the begining, i.e. npInput[0]=fValueAdded

     Notes: npInput must be one dimension.

     Revision History:
     Author		Date		Reason
     Miguel Tremblay       July 2nd     Tired of always do the same thing.
     
     """
    
    # Check the dimension
    if (npInput.shape[0]  <= 0):
        sMetroUtilError = _("In shift_right, npInput is not of size (1,).\n")+\
                          "len(npInput.shape)=%s"\
                          % (len(npInput.shape))
        raise  metro_error.Metro_util_error(sMetroUtilError)
    npToBeCat = numpy.array([fValueAdded])
    # Cut the trailing value
    npOutput  = numpy.take(npInput,\
                              numpy.arange(0, len(npInput)-1))
    npOutput = numpy.concatenate((npToBeCat, npOutput))

    return npOutput


def get_indice_of(npInput, fValue=0):
    """
    Name: get_indice_of

    Parameters: [[I] numpy npInput : The array to search in.
                [[I] double fValue : The value to "insert" in the array

    Returns: int nIndice : The indice of the array where fValue belongs.

    Functions Called:  

    Description: The numpy must be ordered.  Returns the indices where
        npInput[nIndice-1] <= fValue <= npInput[nIndice]

    Notes: npInput must be one dimension.

    Revision History:
    Author		Date		Reason
    Miguel Tremblay   July 2nd         Tanne de toujours faire la meme chose
    """
    if type (npInput) != type(numpy.array([])):
        npInput = numpy.array(npInput)
    if fValue < npInput.min():
        return 0
    elif fValue > npInput.max():
        return len(npInput)
    for i in range(1, len(npInput)):
        if npInput[i-1] <= fValue and fValue <= npInput[i]:
            return i

    sMetroUtilError = _("No indice with this value: %d") %(fValue)
    raise metro_error.Metro_util_error(sMetroUtilError)



def get_difference_array(npInput, bPrevious=False):
    """
    Name: get_difference_array

    Parameters: [[I] numpy npInput :

    Returns: numpy npOutput : An array storing the difference.
            bool bPrevious : If True , get the difference
                              between the indice i and the indice i-1.
                             If False (default), get the difference between
                              the indice i and indice i+1.
          

    Functions Called:  

    Description: This method compute the difference between consecutive value
      in a numarrray.
      npOutput[0] = npInput[1]-npInput[0]
      npOutput[i] = npInput[1+1]-npInput[i]
      npOutput[len(npOutput)-1] = npInput[0]-npInput[len(npInput)-1]
      
    Notes: npInput must be one dimension.

    Revision History:
    Author		Date		Reason
    Miguel Tremblay       August 4th 2004     Compute time in observation
    """
    
    if bPrevious:
        npShiftRight = shift_right(npInput,npInput[len(npInput)-1])
        npOutput = npShiftRight - npInput
        return npOutput
    else:
        npShiftLeft = shift_left(npInput,npInput[0])
        npOutput = npShiftLeft - npInput
        return npOutput


def sign(dResult, dSign):
    """
    Name: sign

    Parameters:   [I double  dResult : 
                  [I double  dSign : 

    Returns:  - abs(dResult) if dSign < 0
                abs(dResult) if dSign > 0
           

    Functions Called:  abs

    Description:  See "Returns"

    Notes: This is the equivalent of SIGN in fortran.  And no,
    there is no built-in function in python that does that.

    Revision History:
    Author		Date		Reason
    Miguel Tremblay       August 24th 2004
    """
    
    if dSign >= 0:
        return abs(dResult)
    else:
        return -abs(dResult)
    

def subsample(npInput, nSubsamplingIndice):
    """
     Name: subsample

     Parameters:   numpy npInput : array to subsample
                   integer nSubsamplingIndice : if == 2, only take one element
                   out of two.

     Returns:  numpy npOutput : subsampled array

     Functions Called: 

     Description:  

     Notes: 

     Revision History:
     Author		Date		Reason
     Miguel Tremblay       September 20th 2004
     """
    # Check if there is an error
    if len(npInput) < nSubsamplingIndice:
        sMetroUtilError = _("In metro_util.subsample, subsampling rate")+\
                          _("is higher than array size: %d > %d") %\
                          (nSubsamplingIndice, len(npInput ))
        raise metro_error.Metro_util_error(sMetroUtilError)

    # Perform the subsampling
    npSub = numpy.arange(0, len(npInput), nSubsamplingIndice)
    npOutput = numpy.take(npInput, npSub)

    return npOutput


def concat_array(npArray1, npArray2):
    """
    Name: concat_array

    Parameters:   numpy npArray1 : array to put in the first column
                  numpy npArray2 : array to put in the second column

    Returns:  numpy npConcat : 

    Functions Called: numpy.concatenate numpy.setshape

    Description: Take two arrays, transform then in column and then form
     a couple of number in each position.  Usefull to create graphics.

    x = [x1, x2, ..., xn]
    y = [y1, y2, ..., yn]
    concat_array(x,y) return [[x1,y1],
                              [x2,y2],
                              ...,
                              [xn,yn]],
                             

    Notes: 

    Revision History:
    Author		Date		Reason
    Miguel Tremblay       September 20th 2004
    """
    nLen1 = len(npArray1)
    nLen2 = len(npArray2)
    if nLen2 < nLen1:
        sMetroUtilWarning = _("Array are not of the same size") +\
                            _("cutting the first one")
        print sMetroUtilWarning
        npPadd = numpy.zeros(nLen1 - nLen2)+npArray2.mean()
        npArray2 = numpy.concatenate((npArray2,npPadd))
        nLen2 = nLen1
    elif nLen1 < nLen2:
        sMetroUtilError = _("In metro_util.concat_array, array must be") +\
                          _(" of the same dimension: %d != %d") % \
                          ((nLen1, nLen2))
        raise metro_error.Metro_util_error(sMetroUtilError)

    # First, rotate the axis
    npArray1.setshape(nLen1,1)
    npArray2.setshape(nLen2,1)

    # Then concatenate
    npConcat = numpy.concatenate((npArray1,npArray2),1)

    return npConcat


def cut_indices(npArray, x0, xn):
    """
    Name: cut_indices

    Parameters:   numpy npArray : array to be cut
                  float x0 : The minimum from with the left will be cut.
                  float  xn:  The maximum from with the right will be cut.

    Returns:  [indiceLeft, indiceRight]

    Functions Called: 

    Description:  Reduce an array to the value between x0 and xn


    Notes: Array should be monotone 

    Revision History:
    Author		Date		Reason
    Miguel Tremblay       September 20th 2004
    """
    nFirstValidIndice = get_indice_of(npArray, x0)
    nLastValidIndice = get_indice_of(npArray, xn)

    lRes = [nFirstValidIndice,nLastValidIndice]
    return lRes

    
def cut(npArray, x0, xn):
    [left,right] = cut_indices(npArray, x0, xn)

    npRes = npArray[left:right]
    return npRes


def sum_array(npInput):
    """
     Name: sum_array

     Parameters:   numpy npInput : array to be sum

     Returns:   numpy npOutput 

     Functions Called: 

     Description:  Put the sum of npInput[0:i].sum() in npOuput[i]


     Notes: Array should be 1-dimension

     Revision History:
     Author		Date		Reason
     Miguel Tremblay       January 18th 2005
     """

    npOutput = numpy.array([])

    for i in range(0,len(npInput)):
        npOutput = numpy.concatenate((npOutput, \
                           numpy.array([npInput[0:i].sum()])),1)

    return npOutput


def validate_version_number(sVersion, sMin_version, sMax_version ):

    min_version = LooseVersion(sMin_version)
    max_version = LooseVersion(sMax_version)

    
    if sVersion != None:
        version = LooseVersion(sVersion)
        
        if version < min_version:
            sMessage = _("Version number:'%s' is too old. Version from '%s' ")\
                       % (version, min_version) +\
                       _("to '%s' inclusively are supported") \
                       % (max_version)
            raise metro_error.Metro_version_error(sMessage)                
        elif  version > max_version:
            sMessage = _("Version number:'%s' is not yet supported. Version ")\
                       % (version) +\
                       _("from '%s' to '%s' inclusively are supported") \
                       % (min_version,max_version)
            raise metro_error.Metro_version_error(sMessage)

    else:
        sMessage = _("Can't find version number. Version from '%s' ") \
                   % (min_version) +\
                   _("to '%s' inclusively are supported") \
                   % (max_version)
        raise metro_error.Metro_version_error(sMessage)


def init_translation(sFilename):
    """
    Name: init_translation

    Parameters:   string sFilename :

    Functions Called: gettext.translation

    Description:  Indication which file should be use for translation.


    Notes:

    Revision History:
    Author		Date		Reason
    Miguel Tremblay       November 8th 2004
    """
    t = gettext.translation(sFilename, get_metro_root_path() +\
                            '/usr/share/locale')
    _t_ = t.gettext

    return _t_


def interp(y_values, x_values, new_x_values):
  """
  Perform interpolation similar to deprecated arrayfns.interp in Numeric.

  interp(y, x, z) = y(z) interpolated by treating y(x) as piecewise fcn.

  Comes from http://projects.scipy.org/pipermail/scipy-user/2007-March/011479.html
  Thank you Stephen
  """
  x = numpy.array(x_values, dtype='float')
  y = numpy.array(y_values, dtype='float')

  xx = numpy.array(new_x_values, dtype='float')
  # High indices
  hi = numpy.searchsorted(x, xx)

  # Low indices
  lo = hi - 1

  slopes = (y[hi] - y[lo])/(x[hi] - x[lo])

  # Interpolated data
  yy = y[lo] + slopes*(xx - x[lo])
  return yy

def is_array_uniform(npArray):
  """
  Check if the array has an monotone and regular incrementation steps.

  Return a boolean value indicating if yes or no, the array is regular.
  """

  dStartValue = npArray[0]
  dEndValue = npArray[-1]
  nLen =  len(npArray)

  npRegularArray = numpy.linspace(dStartValue, dEndValue,nLen)
  npZeros = numpy.zeros(nLen)

  return ((npRegularArray-npArray) == npZeros).all()

