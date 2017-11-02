import ctypes as C
import numpy as np

import pyhaplophase.methods.SAH_opti as sah
import pyhaplophase.dataset as dataset
import pyhaplophase.parametersopti as paramsopti
import pyhaplophase.utils as utils
import pyhaplophase.error as error
import pyhaplophase.experiments.experiment as experiment
import pyhaplophase.dumper.cout_dumper as coutdumper
import cProfile
import os
import loter.metrics as metrics
import loter.predcombine as combine
import loter.pipeline as pipeline

from loter.find_lib import _LIB

def wrapper_cpp(G, H, A, S, nb_iter, w, penalty):
    (n, m) = G.shape
    (k, _) = A.shape

    f_eigen_loter = _LIB.haplophase_cpp
    f_eigen_loter.argtypes = [np.ctypeslib.ndpointer(dtype = np.uint8,
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
                                   C.c_int, C.c_int, C.c_int, C.c_int,
                                   C.c_float, C.c_float]
    f_eigen_loter.restype = None

    return f_eigen_loter(G, H, A, S, n, m, k, nb_iter, w, penalty)

def wrapper_all(G, k, nb_iter, nb_run, w, penalty):
    (n, m) = G.shape

    f_eigen_loter = _LIB.haplophase_all
    f_eigen_loter.argtypes = [np.ctypeslib.ndpointer(dtype = np.uint8,
                                                          ndim=2,
                                                          flags='C_CONTIGUOUS'),
                                   np.ctypeslib.ndpointer(dtype = np.uint8,
                                                          ndim=2,
                                                          flags='C_CONTIGUOUS'),
                                   C.c_int, C.c_int, C.c_int, C.c_int, C.c_int,
                                   C.c_float, C.c_float]
    f_eigen_loter.restype = None

    H = np.zeros((2*n,m), dtype=np.uint8)
    f_eigen_loter(G, H, n, m, k, nb_iter, nb_run, w, penalty)
    return H

def wrapper_parallel(G, k, nb_iter, nb_run, w, penalty, num_threads):
    (n, m) = G.shape

    f_eigen_loter = _LIB.haplophase_parallel
    f_eigen_loter.argtypes = [np.ctypeslib.ndpointer(dtype = np.uint8,
                                                          ndim=2,
                                                          flags='C_CONTIGUOUS'),
                                   np.ctypeslib.ndpointer(dtype = np.uint8,
                                                          ndim=2,
                                                          flags='C_CONTIGUOUS'),
                                   C.c_int, C.c_int, C.c_int, C.c_int, C.c_int,
                                   C.c_float, C.c_float, C.c_int]
    f_eigen_loter.restype = None

    H = np.zeros((2*n,m), dtype=np.uint8)
    f_eigen_loter(G, H, n, m, k, nb_iter, nb_run, w, penalty, num_threads)
    return H

def wrapper_parallel_lambdvar(G, lambdvar, k, nb_iter, nb_run, w, penalty, num_threads):
    (n, m) = G.shape
    nb_lambdvar = len(lambdvar)

    f_eigen_loter = _LIB.haplophase_lambdvar
    f_eigen_loter.argtypes = [np.ctypeslib.ndpointer(dtype = np.uint8,
                                                     ndim=2,
                                                     flags='C_CONTIGUOUS'),
                              np.ctypeslib.ndpointer(dtype = np.uint8,
                                                     ndim=2,
                                                     flags='C_CONTIGUOUS'),
                              np.ctypeslib.ndpointer(dtype = np.uint8,
                                                     ndim=1,
                                                     flags='C_CONTIGUOUS'),
                              C.c_int,
                              C.c_int, C.c_int, C.c_int, C.c_int, C.c_int,
                              C.c_float, C.c_float, C.c_int]
    f_eigen_loter.restype = None

    H = np.zeros((2*n,m), dtype=np.uint8)
    f_eigen_loter(G, H, lambdvar, nb_lambdvar, n, m, k, nb_iter, nb_run, w, penalty, num_threads)
    return H

def create_data():
    G = np.array([[2,2,0,2],
                  [1,1,0,1]])
    H = np.array([[1,1,0,1],[1,1,0,1],[0,1,0,1],[1,0,0,0]])
    A = np.array([[0.1,0.5,0.8,0.9],
                  [0.0,0.1,0.2,0.9]], dtype=np.float32)
    S = np.array([[0,0,0,0],[0,0,0,0],[1,1,1,1],[0,0,0,0]])

    G = np.ascontiguousarray(G).astype(np.uint8)
    H = np.ascontiguousarray(H).astype(np.uint8)
    S = np.ascontiguousarray(S).astype(np.uint8)

    return {"G":G,"H":H,"A":A,"S":S}

def create_param():
    return {"penalty": 2.0,
            "nbclust": 2,
            "w_h": 100.0,
            "nb_iter": 10}

if __name__ == '__main__':
    print("Main wrapper")
