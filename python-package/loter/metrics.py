import numpy as np

import loter.predcombine as pred
import loter.utils as utils

def cost_error_l2(G, H, S, A, lambd, mask=None):
    SA = utils.build_SA(S, A)
    H_minus_SA = H - SA

    fit_error = np.sum(H_minus_SA**2)
    penalty_error = lambd * np.count_nonzero(np.diff(S) != 0)
    return (fit_error, penalty_error)

def switch_error_rate(H_found, H_truth):
    H_found_comp = pred.compress_H(H_found)
    H_truth_comp = pred.compress_H(H_truth)
    heter = np.logical_or(H_truth_comp == 4, H_truth_comp == 5)

    H_found_comp[heter] = np.absolute(np.ediff1d(H_found_comp[heter], to_begin=0))
    H_found_comp[range(H_found_comp.shape[0]), np.argmax(heter, axis=1)] = 0

    H_truth_comp[heter] = np.absolute(np.ediff1d(H_truth_comp[heter], to_begin=0))
    H_truth_comp[range(H_truth_comp.shape[0]), np.argmax(heter, axis=1)] = 0

    not_first_heter = np.copy(heter)
    not_first_heter[range(not_first_heter.shape[0]), np.argmax(heter, axis=1)] = False
    nb_possible_switches = np.count_nonzero(not_first_heter)
    nb_diff = np.count_nonzero(H_found_comp[heter] != H_truth_comp[heter])

    try:
        return nb_diff / float(nb_possible_switches)
    except ZeroDivisionError:
        return 0.0

def imputation_error_rate(G_found, G_truth, G_nan, mask=None):
    if (not(G_found.shape==G_truth.shape==G_nan.shape)):
        print("Error shape for imputation")
    if mask is None:
        mask = np.logical_and(G_nan == 3, G_truth != 3)

    nb_nan = np.count_nonzero(mask)
    nb_diff = np.count_nonzero(G_found[mask] != G_truth[mask])

    try:
        return nb_diff / float(nb_nan)
    except ZeroDivisionError:
        return 0.0

