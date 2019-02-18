import ctypes as C
import numpy as np

import loter.errorhandler as errorhandler
import loter.datastruct.parameter as parameter
from loter.find_lib import _LIB

@errorhandler.eh_fn
def EstimateSErrorHandlerFn(error_message, user_data):
    """Callback function for C api in errorhandler.c

    """
    print("Error Estimation of S")
    print(error_message)

class EstimateSException(Exception):
    """Exception raised for errors in EstimateS calls

    Attributes:
        value -- input in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, value, message):
        self.value = value
        self.message = message

def _init_estimates():

    # Constructor
    _LIB.estimates_create.argtypes = [
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimates_create.restype = C.c_void_p

    # Destructor
    _LIB.estimates_destroy.argtypes = [
        C.c_void_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimates_destroy.restype = None

    # Getter Penalty
    _LIB.estimates_run.argtypes = [
        C.c_void_p,
        np.ctypeslib.ndpointer(dtype = np.uint8,
                               ndim=2,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype = np.uint8,
                               ndim=2,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype = np.float32,
                               ndim=2,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype = np.uint8,
                               ndim=2,
                               flags='C_CONTIGUOUS'),
        C.c_int,
        C.c_int,
        C.c_void_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimates_run.restype = None

def _init_estimatesh():

    # Constructor
    _LIB.estimatesh_create.argtypes = [
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimatesh_create.restype = C.c_void_p

    # Destructor
    _LIB.estimatesh_destroy.argtypes = [
        C.c_void_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimatesh_destroy.restype = None

    # Getter Penalty
    _LIB.estimatesh_run.argtypes = [
        C.c_void_p,
        np.ctypeslib.ndpointer(dtype = np.uint8,
                               ndim=2,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype = np.uint8,
                               ndim=2,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype = np.float32,
                               ndim=2,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype = np.uint8,
                               ndim=2,
                               flags='C_CONTIGUOUS'),
        C.c_int,
        C.c_int,
        C.c_void_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimatesh_run.restype = None

def _init_estimateshknn():

    # Constructor
    _LIB.estimateshknn_create.argtypes = [
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimateshknn_create.restype = C.c_void_p

    # Destructor
    _LIB.estimateshknn_destroy.argtypes = [
        C.c_void_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimateshknn_destroy.restype = None

    # Getter Penalty
    _LIB.estimateshknn_run.argtypes = [
        C.c_void_p,
        np.ctypeslib.ndpointer(dtype = np.uint8,
                               ndim=2,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype = np.uint8,
                               ndim=2,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype = np.float32,
                               ndim=2,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype = np.uint8,
                               ndim=2,
                               flags='C_CONTIGUOUS'),
        C.c_int,
        C.c_int,
        C.c_float,
        C.c_int,
        C.c_void_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimatesh_run.restype = None

def _init_estimatesknn():

    # Constructor
    _LIB.estimatesknn_create.argtypes = [
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimatesknn_create.restype = C.c_void_p

    # Destructor
    _LIB.estimatesknn_destroy.argtypes = [
        C.c_void_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimatesknn_destroy.restype = None

    # Getter Penalty
    _LIB.estimatesknn_run.argtypes = [
        C.c_void_p,
        np.ctypeslib.ndpointer(dtype = np.uint8,
                               ndim=2,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype = np.uint8,
                               ndim=2,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype = np.uint32,
                               ndim=2,
                               flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype = np.float32,
                               ndim=1,
                               flags='C_CONTIGUOUS'),
        C.c_int,
        C.c_int,
        C.c_int,
        C.c_void_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimatesknn_run.restype = None

class EstimateS(object):

    def __init__(self):
        self._EH = errorhandler.ErrorHandler(EstimateSErrorHandlerFn, None)
        self.obj = _LIB.estimates_create(C.byref(self._EH))

    def run(self, data, param):

        param_opti = parameter.ParameterOptimization(param["penalty"],
                                                     param["nbclust"],
                                                     param["w_h"],
                                                     param["nb_iter"])

        G, H, A, S = data["G"], data["H"], data["A"], data["S"]
        n, m = G.shape

        _LIB.estimates_run(self.obj,
                           G,
                           H,
                           A,
                           S,
                           n,
                           m,
                           param_opti.obj,
                           C.byref(self._EH))

    def __del__(self):
        _LIB.estimates_destroy(self.obj, C.byref(self._EH))

def optimize_S(data, param):
    ests = EstimateS()
    ests.run(data, param)
    return (data, param)

class EstimateSH(object):

    def __init__(self):
        self._EH = errorhandler.ErrorHandler(EstimateSErrorHandlerFn, None)
        self.obj = _LIB.estimatesh_create(C.byref(self._EH))

    def run(self, data, param):
        param_opti = parameter.ParameterOptimization(param["penalty"],
                                                     param["nbclust"],
                                                     param["w_h"],
                                                     param["nb_iter"])

        G, H, A, S = data["G"], data["H"], data["A"], data["S"]
        n, m = G.shape

        _LIB.estimatesh_run(self.obj,
                            G,
                            H,
                            A,
                            S,
                            n,
                            m,
                            param_opti.obj,
                            C.byref(self._EH))

    def __del__(self):
        _LIB.estimatesh_destroy(self.obj, C.byref(self._EH))

def optimize_SH(data, param):
    ests = EstimateSH()
    ests.run(data, param)
    return (data, param)

class EstimateSHknn(object):

    def __init__(self):
        self._EH = errorhandler.ErrorHandler(EstimateSErrorHandlerFn, None)
        self.obj = _LIB.estimateshknn_create(C.byref(self._EH))

    def run(self, data, param):
        param_opti = parameter.ParameterOptimization(param["penalty"],
                                                     param["nbclust"],
                                                     param["w_h"],
                                                     param["nb_iter"])

        G, H, A, S = data["G"], data["H"], data["A"], data["S"]
        n, m = G.shape

        _LIB.estimateshknn_run(self.obj,
                               G,
                               H,
                               A,
                               S,
                               n,
                               m,
                               param["small_penalty"],
                               param["num_threads"],
                               param_opti.obj,
                               C.byref(self._EH))

    def __del__(self):
        _LIB.estimateshknn_destroy(self.obj, C.byref(self._EH))

def optimize_SHknn(data, param):
    ests = EstimateSHknn()
    ests.run(data, param)
    return (data, param)

class EstimateSknn(object):

    def __init__(self):
        self._EH = errorhandler.ErrorHandler(EstimateSErrorHandlerFn, None)
        self.obj = _LIB.estimatesknn_create(C.byref(self._EH))

    def run(self, data, param):

        param_opti = parameter.ParameterOptimization(param["penalty"],
                                                     param["nbclust"],
                                                     param["w_h"],
                                                     param["nb_iter"])

        G, H, A, S = data["G"], data["H"], data["A"], data["S"]
        n, m = G.shape

        _LIB.estimatesknn_run(self.obj,
                              np.ascontiguousarray(H.T),
                              np.ascontiguousarray(A.T),
                              np.ascontiguousarray(S),
                              np.ascontiguousarray(param["weights"]).astype(np.float32),
                              n,
                              m,
                              param["num_threads"],
                              param_opti.obj,
                              C.byref(self._EH))

    def __del__(self):
        _LIB.estimatesknn_destroy(self.obj, C.byref(self._EH))

def optimize_Sknn(data, param):
    estsknn = EstimateSknn()
    estsknn.run(data, param)
    return (data, param)

#initialize
_init_estimates()
_init_estimatesh()
_init_estimatesknn()
_init_estimateshknn()
