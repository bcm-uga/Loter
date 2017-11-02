import ctypes as C

import loter.errorhandler as errorhandler
from loter.find_lib import _LIB

@errorhandler.eh_fn
def ParameterOptimizationErrorHandlerFn(error_message, user_data):
    """Callback function for C api in errorhandler.c

    """
    print("Error ParameterOptimization")
    print(error_message)

class ParameterOptimizationException(Exception):
    """Exception raised for errors in input parameters

    Attributes:
        value -- input in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, value, message):
        self.value = value
        self.message = message

def _init_parameter_optimization():

    # Constructor
    _LIB.parameterOptimization_create.argtypes = [
        C.c_float,
        C.c_int,
        C.c_float,
        C.c_int,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.parameterOptimization_create.restype = C.c_void_p

    # Destructor
    _LIB.parameterOptimization_destroy.argtypes = [
        C.c_void_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.parameterOptimization_destroy.restype = None

    # Getter Penalty
    _LIB.parameterOptimization_get.argtypes = [
        C.c_void_p,
        C.c_char_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.parameterOptimization_get.restype = C.c_char_p
    
    # Setter Penalty
    _LIB.parameterOptimization_set.argtypes = [
        C.c_void_p,
        C.c_char_p,
        C.c_char_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.parameterOptimization_set.restype = None

class ParameterOptimization(object):

    def __init__(self, penalty, nbclust, w_h, nb_iter):
        self._EH = errorhandler.ErrorHandler(ParameterOptimizationErrorHandlerFn, None)

        self.obj = _LIB.parameterOptimization_create(float(penalty),
                                                     int(nbclust),
                                                     float(w_h),
                                                     int(nb_iter),
                                                     C.byref(self._EH))
    @property
    def penalty(self):
        return float(_LIB.parameterOptimization_get(self.obj,
                                                    "penalty",
                                                    C.byref(self._EH)))

    @penalty.setter
    def penalty(self, value):
        if value < 0:
            raise ParameterOptimizationException(value, "Penalty < 0")
        _LIB.parameterOptimization_set(self.obj,
                                       "penalty",
                                       str(value),
                                       C.byref(self._EH))
 
    @property
    def nbclust(self):
        return int(_LIB.parameterOptimization_get(self.obj,
                                                  "nbclust",
                                                  C.byref(self._EH)))

    @nbclust.setter
    def nbclust(self, value):
        if value < 0:
            raise ParameterOptimizationException(value, "Number of clusters < 0")
        _LIB.parameterOptimization_set(self.obj,
                                       "nbclust",
                                       str(value),
                                       C.byref(self._EH))

    @property
    def w_h(self):
        return float(_LIB.parameterOptimization_get(self.obj,
                                                    "w_h",
                                                    C.byref(self._EH)))

    @w_h.setter
    def w_h(self, value):
        if value < 0:
            raise ParameterOptimizationException(value, "Weight of homozygous < 0")
        _LIB.parameterOptimization_set(self.obj,
                                       "w_h",
                                       str(value),
                                       C.byref(self._EH))
               
    @property
    def nb_iter(self):
        return int(_LIB.parameterOptimization_get(self.obj,
                                                  "nb_iter",
                                                  C.byref(self._EH)))

    @nb_iter.setter
    def nb_iter(self, value):
        if value <= 0:
            raise ParameterOptimizationException(value, "Number of Iterations <= 0")
        _LIB.parameterOptimization_set(self.obj,
                                       "nb_iter",
                                       str(value),
                                       C.byref(self._EH))
 
    def __del__(self):
        _LIB.parameterOptimization_destroy(self.obj, self._EH)

#initialize
_init_parameter_optimization()
