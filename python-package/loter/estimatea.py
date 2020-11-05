import ctypes as C
import numpy as np

import loter.errorhandler as errorhandler
import loter.datastruct.parameter as parameter
from loter.find_lib import _LIB

from scipy.optimize import linear_sum_assignment as linear_assignment  # Munkres Algorithm
from collections import Counter

@errorhandler.eh_fn
def EstimateAErrorHandlerFn(error_message, user_data):
    """Callback function for C api in errorhandler.c

    """
    print("Error Estimation of A")
    print(error_message)

class EstimateAException(Exception):
    """Exception raised for errors in EstimateA calls

    Attributes:
        value -- input in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, value, message):
        self.value = value
        self.message = message

def _init_estimatea():

    # Constructor
    _LIB.estimatea_create.argtypes = [
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimatea_create.restype = C.c_void_p

    # Destructor
    _LIB.estimatea_destroy.argtypes = [
        C.c_void_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimatea_destroy.restype = None

    # Getter Penalty
    _LIB.estimatea_run.argtypes = [
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
    _LIB.estimatea_run.restype = None

    # Constructor
    _LIB.estimateagrad_create.argtypes = [
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimateagrad_create.restype = C.c_void_p

    # Destructor
    _LIB.estimateagrad_destroy.argtypes = [
        C.c_void_p,
        C.POINTER(errorhandler.ErrorHandler)
    ]
    _LIB.estimateagrad_destroy.restype = None

    # Getter Penalty
    _LIB.estimateagrad_run.argtypes = [
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
    _LIB.estimateagrad_run.restype = None

class EstimateA(object):

    def __init__(self):
        self._EH = errorhandler.ErrorHandler(EstimateAErrorHandlerFn, None)
        self.obj = _LIB.estimatea_create(C.byref(self._EH))

    def run(self, data, param):

        param_opti = parameter.ParameterOptimization(param["penalty"],
                                                     param["nbclust"],
                                                     param["w_h"],
                                                     param["nb_iter"])

        G, H, A, S = data["G"], data["H"], data["A"], data["S"]
        n, m = G.shape

        _LIB.estimatea_run(self.obj,
                           G,
                           H,
                           A,
                           S,
                           n,
                           m,
                           param_opti.obj,
                           C.byref(self._EH))

    def __del__(self):
        _LIB.estimatea_destroy(self.obj, C.byref(self._EH))

class EstimateAGrad(object):

    def __init__(self):
        self._EH = errorhandler.ErrorHandler(EstimateAErrorHandlerFn, None)
        self.obj = _LIB.estimateagrad_create(C.byref(self._EH))

    def run(self, data, param):

        param_opti = parameter.ParameterOptimization(param["penalty"],
                                                     param["nbclust"],
                                                     param["w_h"],
                                                     param["nb_iter"])

        G, H, A, S = data["G"], data["H"], data["A"], data["S"]
        n, m = G.shape

        _LIB.estimateagrad_run(self.obj,
                               G,
                               H,
                               A,
                               S,
                               n,
                               m,
                               param_opti.obj,
                               C.byref(self._EH))

    def __del__(self):
        _LIB.estimateagrad_destroy(self.obj, C.byref(self._EH))

def optimize_A(data, param):
    esta = EstimateA()
    esta.run(data, param)
    return (data, param)

def optimize_A_gradcpp(data, param):
    esta = EstimateAGrad()
    esta.run(data, param)
    return (data, param)

def optimize_A_grad(data, param):
    k = param["nbclust"]
    w_h = param["w_h"]
    G = data["G"]
    H = data["H"]
    S = data["S"]

    if "eta" in param:
        eta = param["eta"]
    else:
        eta = 0.1

    for j, column in enumerate(S.T):
        n1 = np.zeros(k)
        n0 = np.zeros(k)
        n = [n0,n1]
        for i, elem in enumerate(column):
            if G[i//2,j] == 1:
                n[H[i,j]][elem] += 1
            elif G[i//2,j] == 0 or G[i//2,j] == 2:
                n[H[i,j]][elem] += w_h

        for l in range(k):
            if (n1[l] + n0[l]) == 0:
                pass
            else:
                card_ik = n1[l] + n0[l]
                #data["A"][l,j] = (1 - 2*eta*card_ik)*data["A"][l,j] + 2*eta*n1[l]
                data["A"][l,j] = (1 - eta)*data["A"][l,j] + eta*n1[l]/float(card_ik)

    return (data, param)

def balance_SA(data, param):
    (n, m) = data["G"].shape
    k = param["nbclust"]
    S = data["S"]
    A = data["A"]

    def apply_assignment_S(Sj, permutation):
        inv_permutation = np.argsort(permutation)
        for i, val_s in enumerate(Sj):
            Sj[i] = inv_permutation[val_s]
        return Sj

    def apply_assignment_A(Aj, permutation):
        Aj = Aj[permutation]
        return Aj

    for j in range(1,m):
        weights = np.zeros((k,k))
        for (x,y), c in Counter(zip(S[:,j-1], S[:,j])).iteritems():
            weights[x, y] = c
        assignment = linear_assignment(-weights)
        permutation = assignment[:,1].T

        Sj = apply_assignment_S(S[:, j], permutation)
        S[:, j] = Sj
        Aj = apply_assignment_A(A[:, j], permutation)
        A[:, j] = Aj

    return (data, param)


#initialize
_init_estimatea()
