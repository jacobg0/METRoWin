/////////////////////////////////////////////////////////////////////
// Name: macadam.i
// Author: Miguel Tremblay
// Date: May 27 2004
// Description: Interface for SWIG to used with METRo
// Note: 2006-08-18: Updated with version 1.3.29 of SWIG - Miguel Tremblay
////////////////////////////////////////////////////////////////////

%module macadam
%{
#include "macadam.h"
  %}


////////////////////////////////////////////////////////////
// Always place the typemaps before the declaration of functions //

///////////////////////
// char 
///////////////////////
// in
//////////////////////
// Ugly way to deal with char**
// This tells SWIG to treat char ** as a special case
// From http://www.swig.org/Doc1.3/Python.html#n59
%typemap(in) char ** 
 {
  // Check if is a list 
  if (PyList_Check($input)) {
    int nSize = PyList_Size($input);
    int i = 0;
    $1 = (char **) malloc((nSize+1)*sizeof(char *));
    for (i = 0; i < nSize; i++) {
      PyObject *o = PyList_GetItem($input,i);
      if (PyString_Check(o))
	$1[i] = PyString_AsString(PyList_GetItem($input,i));
      else {
	PyErr_SetString(PyExc_TypeError,"list must contain strings");
	free($1);
	return NULL;
      }
    }// end for
    $1[i] = 0;
  }// end if 
  else {
    PyErr_SetString(PyExc_TypeError,"not a list");
    return NULL;
  }
}

////////////////////
// out
////////////////////
%typemap(out) char**
{
  int i=0;

  // Declare $result as a list with zero element
  $result = PyList_New(0);
   
  while($1[i]){
    int nCurrentStrSize;
    PyObject *o;

    nCurrentStrSize = strlen($1[i]);
    o = PyString_FromStringAndSize($1[i],nCurrentStrSize);
    PyList_Append($result, o);
    i++;
  }// end while
  if(i==0){// error message
    PyErr_SetString(PyExc_TypeError,"array must contain at least one character");
  }

}// end typemap out char**

////////////////////
// free
/////////////////////
// This cleans up the char ** array we malloc'd before the function call
%typemap(freearg) char ** {
  free((char **) $1);
}

///////////////////////////////////////////
// double
//////////////////////////////////////////
// in
/////////////////////////////////////////
%typemap(in) double *{
  long i;
// Check if is a list 
  if (PyList_Check($input)) {
    long nSize = PyList_Size($input);
    long i = 0;
    $1 = (double*) malloc((nSize+1)*sizeof(double));
    for (i = 0; i < nSize; i++) {
      PyObject *o = PyList_GetItem($input,i);
      if (PyFloat_Check(o)){
	$1[i] = PyFloat_AsDouble(o);
      }
      else{
	PyErr_SetString(PyExc_TypeError,"list must contain double numbers");
	free($1);
	return NULL;
      }
    }// end for
  }// end if
  else{   
    PyErr_SetString(PyExc_TypeError,"not a list");
    return NULL;
  }
}
%typemap(in) double **{
  printf("pointer of pointer: double.  Not implemented.  See macadam.i\n");
}

////////////////////
// out
////////////////////
%typemap(out) double*
{
  $result = PyFloat_FromDouble($1[0]);
}// end typemap out double*

////////////////////
// free
//////////////////////
// This cleans up the double * array we malloc'd before the function call
%typemap(freearg) double * {
  free((double*)$1);
}

//////////////////////
// doubleStruc
//////////////////////
#ifdef SWIGPYTHON
%typemap(out) struct doubleStruct
{
  long i;
  long nSizeArray;
  double* pdArray;

  // Store the value of struct in local variables
  nSizeArray = $1.nSize;
  pdArray = $1.pdArray;
  // Create the python list
  $result = PyList_New(nSizeArray);

  for(i=0; i<nSizeArray; i++){
    // Create the python object from double
    PyObject* o;
    o = PyFloat_FromDouble(pdArray[i]);
    // Set the variable in the list.
    PyList_SetItem($result, i, o);
  }
}
#endif 

///////////////////////////////////////////
// float
//////////////////////////////////////////
// No input for float, all numbers in python are double.
/////////////////////////////////////////

////////////////////
// out
////////////////////
%typemap(out) float*
{
  $result = PyFloat_FromDouble($1[0]);
}// end typemap out char**

////////////////////
// free
//////////////////////
// This cleans up the double * array we malloc'd before the function call
%typemap(freearg) float * {
  free((float*)$1);
}

//////////////////////
// floatStruc
//////////////////////
#ifdef SWIGPYTHON
%typemap(out) struct floatStruct
{
  long i;
  long nSizeArray;
  float* pfArray;

  // Store the value of struct in local variables
  nSizeArray = $1.nSize;
  pfArray = $1.pfArray;
  // Create the python list
  $result = PyList_New(nSizeArray);

  for(i=0; i<nSizeArray; i++){
    // Create the python object from double
    PyObject* o;
    o = PyFloat_FromDouble(pfArray[i]);
    // Set the variable in the list.
    PyList_SetItem($result, i, o);
  }
}
#endif 

///////////////////////////////////////////
// long
//////////////////////////////////////////
// in
/////////////////////////////////////////
%typemap(in) long *{
  long i;
// Check if is a list 
  if (PyList_Check($input)) {
    long nSize = PyList_Size($input);
    long i = 0;
    $1 = (long*) malloc((nSize+1)*sizeof(long));
    for (i = 0; i < nSize; i++) {
      PyObject *o = PyList_GetItem($input,i);
      if (PyInt_Check(o)){
	$1[i] = PyInt_AsLong(o);
      }
      else{
	PyErr_SetString(PyExc_TypeError,"list must contain long numbers");
	free($1);
	return NULL;
      }
    }// end for
  }// end if
  else{   
    PyErr_SetString(PyExc_TypeError,"not a list");
    return NULL;
  }
}

////////////////////
// out
////////////////////
%typemap(out) long*
{
  $result = PyInt_FromLong($1[0]);
}// end typemap out char**

////////////////////
// free
//////////////////////
// This cleans up the double * array we malloc'd before the function call
%typemap(freearg) long * {
  free((long*)$1);
}

//////////////////////
// longStruc
//////////////////////
#ifdef SWIGPYTHON
%typemap(out) struct longStruct
{
  long i;
  long nSizeArray;
  long* plArray;

  // Store the value of struct in local variables
  nSizeArray = $1.nSize;
  plArray = $1.plArray;
  // Create the python list
  $result = PyList_New(nSizeArray);
  for(i=0; i<nSizeArray; i++){
    // Create the python object from double
    PyObject* o;
    o = PyInt_FromLong(plArray[i]);
    // Set the variable in the list.
    PyList_SetItem($result, i, o);
  }
}
#endif

///////////////////////////////////////////
// short
//////////////////////////////////////////
// No input for short, all numbers in python are long.
/////////////////////////////////////////

////////////////////
// out
////////////////////
%typemap(out) short*
{
  $result = PyInt_FromLong($1[0]);
  free($1);
}// end typemap out char**

////////////////////
// free
//////////////////////
// This cleans up the double * array we malloc'd before the function call
%typemap(freearg) short* {
  free((short*)$1);
}

//////////////////////
// shortStruc
//////////////////////
#ifdef SWIGPYTHON
%typemap(out) struct shortStruct
{
  long i;
  long nSizeArray;
  short* pnArray;

  // Store the value of struct in local variables
  nSizeArray = $1.nSize;
  pnArray = $1.pnArray;
  // Create the python list
  $result = PyList_New(nSizeArray);

  for(i=0; i<nSizeArray; i++){
    // Create the python object from double
    PyObject* o;
    o = PyInt_FromLong(pnArray[i]);
    // Set the variable in the list.
    PyList_SetItem($result, i, o);
  }
  free(pnArray);
}
#endif

///////////////////////////////////////////
// int
//////////////////////////////////////////
// No input for int, all numbers in python are long.
/////////////////////////////////////////

////////////////////
// out
////////////////////
%typemap(out) int*
{
  $result = PyInt_FromLong($1[0]);
  free($1);
}// end typemap out char**

////////////////////
// free
//////////////////////
// This cleans up the double * array we malloc'd before the function call
%typemap(freearg) int* {
  free((int*)$1);
}

//////////////////////
// intStruc
//////////////////////
#ifdef SWIGPYTHON
%typemap(out) struct intStruct
{
  long i;
  long nSizeArray;
  int* pnArray;

  // Store the value of struct in local variables
  nSizeArray = $1.nSize;
  pnArray = $1.pnArray;
  // Create the python list
  $result = PyList_New(nSizeArray);

  for(i=0; i<nSizeArray; i++){
    // Create the python object from double
    PyObject* o;
    o = PyInt_FromLong(pnArray[i]);
    // Set the variable in the list.
    PyList_SetItem($result, i, o);
  }
  free(pnArray);
}
#endif

// Now a test function 
%inline %{
int print_args(char **argv) {
    int i = 0;
    while (argv[i]) {
         printf("argv[%d] = %s\n", i,argv[i]);
         i++;
    }
    return i;
}
%}
//////////////////////////////////////////////////////////////////////

  

extern void Do_Metro(long, double, double, double*,\
	 long, long*, double*, double*,\
	 double*, double*, double*, double*,\
	 double*, long*, long*, double*,\
	 double*, double*, double*, double*,\
	 long*, long*, double,\
	 long, long, long, \
	double, long, double);

extern struct doubleStruct get_ra(void);
extern struct doubleStruct get_sn(void);
extern struct longStruct get_rc(void);
extern struct doubleStruct get_rt(void);
extern struct doubleStruct get_ir(void);
extern struct doubleStruct get_sf(void);
extern struct doubleStruct get_fv(void);
extern struct doubleStruct get_fc(void);
extern struct doubleStruct get_g(void);
extern struct doubleStruct get_bb(void);
extern struct doubleStruct get_fp(void);
extern struct longStruct get_echec(void);
extern struct doubleStruct get_sst(void);
extern struct doubleStruct get_depth(void);
extern long get_nbr_levels(void);
extern struct doubleStruct get_lt(void);
