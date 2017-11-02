import numpy as np
import functools
import operator
import loter.utils as utils

def unpack_data_from_input(l_input):
    return [data for data, param in l_input]

def compress_H(H):
    H1, H2 = np.copy(H[::2]).astype(np.int), np.copy(H[1::2]).astype(np.int)
    H1[H1 == 1] = 4
    H2[H2 == 1] = 5
    return H1 + H2

def build_H1(H):
    r = np.copy(H)
    r[r == 4] = 1
    r[r == 9] = 1
    r[r == 5] = 0
    return r

def build_H2(H):
    r = np.copy(H)
    r[r == 4] = 0
    r[r == 9] = 1
    r[r == 5] = 1
    return r

def pipeline_H_mean(l_H, heter):
    def treat_H(H):
        H_res = compress_H(H)
        homozygous = ~heter
        H_res[homozygous] = 0
        # compute if the switches by compute differences
        H_res[heter] = np.absolute(np.ediff1d(H_res[heter], to_begin=0))
        # set the first heterozygous to 0
        H_res[range(H_res.shape[0]), np.argmax(heter, axis=1)] = 0
        # For the accumulator with set the non-switches to -1 instead of 0
        H_res[np.logical_and(heter, H_res == 0)] = -1
        return H_res
    l_H_treated = map(treat_H, l_H)
    hn, hm = l_H[0].shape
    acc = functools.reduce(operator.add, l_H_treated, np.zeros((hn/2, hm), dtype=int))

    # Prepare the result for the output
    acc[np.logical_and(acc >= 0, heter)] = 1
    acc[np.logical_and(acc < 0, heter)] = 0
    acc[heter] = np.cumsum(acc[heter]) % 2
    acc[np.logical_and(acc == 1, heter)] = 5
    acc[np.logical_and(acc == 0, heter)] = 4

    result = np.copy(l_H[0])
    result[::2][heter] = build_H1(acc)[heter]
    result[1::2][heter] = build_H2(acc)[heter]

    return result

def pipeline_H_weighted_mean(l_SA, heter):
    l_mat_p10 = []
    for SA in l_SA:
        A1, A2 = SA[::2] + SA[1::2]
        mat_p10 = A1 * (1 - A2) / (A1 * (1 - A2) + A2 * (1 - A1))

def combine_H_mean(l_input):
    l_data = unpack_data_from_input(l_input)
    l_H = [elem["H"] for elem in l_data]
    G = l_data[0]["G"]
    heter = (G == 1)
    return pipeline_H_mean(l_H, heter)

def combine_G_mean(l_input):
    l_data = unpack_data_from_input(l_input)
    l_H = [elem["H"] for elem in l_data]
    list_G = [H[::2] + H[1::2] for H in l_H]
    mean_G = np.mean(list_G, axis=(0))
    return np.around(mean_G)

def combine_G_mode(l_input):
    l_data = unpack_data_from_input(l_input)
    l_H = [elem["H"] for elem in l_data]
    list_G = [H[::2] + H[1::2] for H in l_H]
    mode_G = utils.mode(np.dstack(list_G), axis=2)[0]
    res = np.reshape(mode_G, mode_G.shape[:-1])
    return res.astype(np.uint8)

combiner_H = {
    "H mean": combine_H_mean
}
combiner_G = {
    "G mean": combine_G_mean,
    "G vote": combine_G_mode
}
