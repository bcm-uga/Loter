import loter.estimatea as esta
import loter.estimateh as esth
import loter.graph as ests
import loter.toolsfunc as toolsfunc
import loter.metrics as metrics

import logging
import sys

root = logging.getLogger()
root.setLevel(logging.WARNING)

ch = logging.StreamHandler(sys.stderr)
ch.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)
logger = root

"""
An "opti" is the main function solving the problem.
Taking data and param as input
Return data and param
"""
def classic_opti(data, param):
    nb_iter = param["nb_iter"]

    for i in range(nb_iter):
        data, param = ests.optimize_S(data, param)
        data, param = esta.optimize_A(data, param)
        data, param = esth.optimize_H(data, param)


    return data, param
    #return toolsfunc.repeated(toolsfunc.compose(esth.optimize_H, esta.optimize_A, ests.optimize_S),
    #                           nb_iter)((data, param))

def classic_opti_sha(data, param):
    nb_iter = param["nb_iter"]

    for i in range(nb_iter):
        data, param = ests.optimize_S(data, param)
        data, param = esth.optimize_H(data, param)
        data, param = esta.optimize_A(data, param)


    return data, param

def grad_opti(data, param):
    nb_iter = param["nb_iter"]

    for i in range(nb_iter):
        data, param = ests.optimize_S(data, param)
        data, param = esta.optimize_A_gradcpp(data, param)
        data, param = esth.optimize_H(data, param)


    return data, param


def join_opti(data, param):
    nb_iter = param["nb_iter"]

    for i in range(nb_iter):
        data, param = ests.optimize_SH(data, param)
        data, param = esth.optimize_H_old(data, param)
        data, param = esta.optimize_A(data, param)
        logger.debug("iter {}, cost : {}".format(i, metrics.cost_error_l2(data["G"],
                                                                          data["H"],
                                                                          data["S"],
                                                                          data["A"],
                                                                          param["penalty"])))

    return data, param

def join_balance(data, param):
    nb_iter = param["nb_iter"]

    for i in range(nb_iter):
        data, param = ests.optimize_SH(data, param)
        data, param = esth.optimize_H_old(data, param)
        data, param = esta.balance_SA(data, param)
        data, param = esta.optimize_A_grad(data, param)
        logger.debug("iter {}, cost before balancing: {}".format(i, metrics.cost_error_l2(data["G"],
                                                                                          data["H"],
                                                                                          data["S"],
                                                                                          data["A"],
                                                                                          param["penalty"])))
    return data, param

def join_then_classic(data, param):
    nb_iter = param["nb_iter"]

    for i in range(1):
        data, param = ests.optimize_SH(data, param)
        data, param = esth.optimize_H_old(data, param)
        data, param = esta.optimize_A(data, param)

    for i in range(nb_iter - 1):
        data, param = ests.optimize_S(data, param)
        data, param = esta.optimize_A(data, param)
        data, param = esth.optimize_H_old(data, param)

    return data, param

def join_then_classic_withsampling(data, param):
    nb_iter = param["nb_iter"]

    for i in range(1):
        data, param = ests.optimize_SH(data, param)
        data, param = esth.optimize_H(data, param)
        data, param = esta.optimize_A(data, param)

    for i in range(nb_iter - 1):
        data, param = ests.optimize_S(data, param)
        data, param = esta.optimize_A(data, param)
        data, param = esth.optimize_H(data, param)

    return data, param

def opti_with_old_H(data, param):
    nb_iter = param["nb_iter"]

    for i in range(nb_iter):
        data, param = ests.optimize_S(data, param)
        data, param = esta.optimize_A(data, param)
        data, param = esth.optimize_H_old(data, param)
        logger.debug("iter {}, cost : {}".format(i, metrics.cost_error_l2(data["G"],
                                                                          data["H"],
                                                                          data["S"],
                                                                          data["A"],
                                                                          param["penalty"])))

    return data, param

def opti_build(h, a, s):
    def optimizer(data, param):
        nb_iter = param["nb_iter"]
        return toolsfunc.repeated(toolsfunc.compose(esth.optih["opti py old fast"],
                                                    esta.optimize_A,
                                                    ests.optimize_S),
                                  nb_iter)((data, param))
    return optimizer

opti = {
    "classic_opti": classic_opti,
    "classic_opti_sha": classic_opti_sha,
    "grad_opti": grad_opti,
    "join_opti": join_opti,
    "join_balance": join_balance,
    "opti_h_old": opti_with_old_H,
    "join_then_classic": join_then_classic,
    "join_then_classic_withsampling": join_then_classic_withsampling
}
