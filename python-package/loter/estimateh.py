import ctypes as C
import numpy as np
import random
from collections import namedtuple

import loter.errorhandler as errorhandler
import loter.datastruct.parameter as parameter
import loter.utils as utils
from loter.find_lib import _LIB

@errorhandler.eh_fn
def EstimateHErrorHandlerFn(error_message, user_data):
    """Callback function for C api in errorhandler.c

    """
    print("Error Estimation of H")
    print(error_message)

class EstimateHException(Exception):
    """Exception raised for errors in EstimateA calls

    Attributes:
        value -- input in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, value, message):
        self.value = value
        self.message = message

def _init_estimateh():

    # Constructor selectswitch
    _LIB.selectswitch_create.argtypes = [
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.selectswitch_create.restype = C.c_void_p
    # Destructor selectswitch
    _LIB.selectswitch_destroy.argtypes = [
        C.c_void_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.selectswitch_destroy.restype = C.c_void_p

     # Constructor selectswitchdeter
    _LIB.selectswitchdeter_create.argtypes = [
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.selectswitchdeter_create.restype = C.c_void_p
    # Destructor selectswitchdeter
    _LIB.selectswitchdeter_destroy.argtypes = [
        C.c_void_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.selectswitchdeter_destroy.restype = C.c_void_p

     # Constructor selectswitchprob
    _LIB.selectswitchprob_create.argtypes = [
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.selectswitchprob_create.restype = C.c_void_p
    # Destructor selectswitchprob
    _LIB.selectswitchprob_destroy.argtypes = [
        C.c_void_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.selectswitchprob_destroy.restype = C.c_void_p

   # Constructor treatnan
    _LIB.treatnan_create.argtypes = [
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.treatnan_create.restype = C.c_void_p
    # Destructor treatnan
    _LIB.treatnan_destroy.argtypes = [
        C.c_void_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.treatnan_destroy.restype = C.c_void_p


    # Constructor
    _LIB.estimateh_create.argtypes = [
        C.c_void_p,
        C.c_void_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimateh_create.restype = C.c_void_p

    # Destructor
    _LIB.estimateh_destroy.argtypes = [
        C.c_void_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimateh_destroy.restype = None

    # Getter Penalty
    _LIB.estimateh_run.argtypes = [
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
    _LIB.estimateh_run.restype = None

class SelectSwitch(object):
    def __init__(self):
        self._EH = errorhandler.ErrorHandler(EstimateHErrorHandlerFn, None)
        self.obj = _LIB.selectswitch_create(C.byref(self._EH))

    def __del__(self):
        _LIB.selectswitch_destroy(self.obj,
                                  C.byref(self._EH))

class SelectSwitchDeter(SelectSwitch):
    def __init__(self):
        self._EH = errorhandler.ErrorHandler(EstimateHErrorHandlerFn, None)
        self.obj = _LIB.selectswitchdeter_create(C.byref(self._EH))

    def __del__(self):
        _LIB.selectswitchdeter_destroy(self.obj,
                                       C.byref(self._EH))

class SelectSwitchProb(SelectSwitch):
    def __init__(self):
        self._EH = errorhandler.ErrorHandler(EstimateHErrorHandlerFn, None)
        self.obj = _LIB.selectswitchprob_create(C.byref(self._EH))

    def __del__(self):
        _LIB.selectswitchprob_destroy(self.obj,
                                      C.byref(self._EH))

class TreatNaN(object):
    def __init__(self):
        self._EH = errorhandler.ErrorHandler(EstimateHErrorHandlerFn, None)
        self.obj = _LIB.treatnan_create(C.byref(self._EH))

    def __del__(self):
        _LIB.treatnan_destroy(self.obj,
                              C.byref(self._EH))

wrapped = namedtuple("wrapped", "obj")
class EstimateH(object):

    def __init__(self, sswitch = wrapped(obj = None), ttnan = wrapped(obj = None)):
        self._EH = errorhandler.ErrorHandler(EstimateHErrorHandlerFn, None)
        self.obj = _LIB.estimateh_create(sswitch.obj,
                                         ttnan.obj,
                                         C.byref(self._EH))

    def run(self, data, param):

        param_opti = parameter.ParameterOptimization(param["penalty"],
                                                     param["nbclust"],
                                                     param["w_h"],
                                                     param["nb_iter"])

        G, H, A, S = data["G"], data["H"], data["A"], data["S"]
        n, m = G.shape

        _LIB.estimateh_run(self.obj,
                           G,
                           H,
                           A,
                           S,
                           n,
                           m,
                           param_opti.obj,
                           C.byref(self._EH))

    def __del__(self):
        _LIB.estimateh_destroy(self.obj, C.byref(self._EH))

def optimize_H(data, param):
    esth = EstimateH()
    esth.run(data, param)
    return (data, param)

def optimize_H_old(data, param):
    sswitch = SelectSwitchDeter()
    esth = EstimateH(sswitch)
    esth.run(data, param)
    return (data, param)

def optimize_H_prob(data, param):
    sswitch = SelectSwitchProb()
    esth = EstimateH(sswitch)
    esth.run(data, param)
    return (data, param)

def optimize_H_old_fast(data, param):
    random.seed()
    def H_opti(data, param):
        G = data["G"]
        (n, m) = G.shape
        A = data["A"]
        H1, H2 = data["H"][::2], data["H"][1::2]
        S1, S2 = data["S"][::2], data["S"][1::2]
        A1, A2 = utils.build_SA(S1, A), utils.build_SA(S2, A)

        mask_a1_over_a2 = np.logical_and(G == 1, A1 >= A2)
        mask_a1_under_a2 = np.logical_and(G == 1, A1 < A2)
        H1[mask_a1_over_a2] = 1
        H2[mask_a1_over_a2] = 0
        H1[mask_a1_under_a2] = 0
        H2[mask_a1_under_a2] = 1

        H1[G == 3] = np.around(A1[G == 3])
        H2[G == 3] = np.around(A2[G == 3])
        data["H"][::2] = H1
        data["H"][1::2] = H2
        return (data, param)

    return H_opti(data, param)

def optimize_H_sample_nan_prob(data, param):
    random.seed()
    def H_opti(data, param):
        G = data["G"]
        (n, m) = G.shape
        A = data["A"]
        H1, H2 = data["H"][::2], data["H"][1::2]
        S1, S2 = data["S"][::2], data["S"][1::2]
        for i in range(n):
            for j in range(m):
                if G[i,j] == 1:
                    a1, a2 =  A[S1[i,j],j], A[S2[i,j],j]
                    norm_prob = a1 + a2
                    if norm_prob == 0:
                        prob_a = 0.5
                    else:
                        prob_a = float(a1) / norm_prob
                    if self.rng.uniform(0,1) <= prob_a:
                        H1[i,j] = 1
                        H2[i,j] = 0
                    else:
                        H1[i,j] = 0
                        H2[i,j] = 1
                elif G[i,j] == 3:
                    H1[i,j] = np.around(A[S1[i,j],j])
                    H2[i,j] = np.around(A[S2[i,j],j])

        data["H"][::2] = H1
        data["H"][1::2] = H2
        return (data, param)
    return H_opti(data, param)

#initialize
_init_estimateh()

optih = {
    "opti_cpp": optimize_H,
    "opti_prob": optimize_H_prob,
    "opti py old": optimize_H_old,
    "opti py old fast": optimize_H_old_fast,
    "opti py fast": optimize_H_sample_nan_prob
}
