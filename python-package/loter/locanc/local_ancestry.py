import numpy as np
import scipy.stats as stats
import pandas as pd

import loter.pipeline as lt
import loter.initparam as initparam
import loter.initdata as initdata
import loter.opti as opti
import loter.estimatea as esta
import loter.estimateh as esth
import loter.graph as ests

##################################################################
#                                                                #
# Pipeline to optimize H (admixed haplotypes) and S (selection)  #
# given A (ancestral haplotypes) simultaneously                  #
#                                                                #
# Initialization:                                                #
# - init A with ancestral haplotypes                             #
#                                                                #
# Optimization:                                                  #
# - join optimisation of H and S                                 #
#                                                                #
# Computational Complexity:                                      #
# - n, the number of ancestral individuals                       #
# - m, the number of SNPs                                        #
# complexity -> O(n^2 * m)                                       #
#                                                                #
# Remarks:                                                       #
# In practice the pipeline is use as a phase corrector module    #
##################################################################

def init_fix_a(data, param):
    def init_a_fix(A, G):
        return param["A_in"]
    return initdata.init_data(data, init_a_fix, initdata.init_h_rand)

def opti_A_fix_join(data, param):
    data, param = ests.optimize_SHknn(data, param)
    data, param = esth.optimize_H_old(data, param)

    return data, param

fixa_pip_A_join = lt.Pipeline(
    initparam.param_initializers["classic_init"],
    init_fix_a,
    opti_A_fix_join,
)

##################################################################
#                                                                #
# Pipeline to optimize S (selection) given A                     #
# (ancestral haplotypes) and H (admixed haplotypes)              #
#                                                                #
# Initialization:                                                #
# - init A with ancestral haplotypes                             #
# - init H with admixed haplotypes                               #
#                                                                #
# Optimization:                                                  #
# - optimisation of S                                            #
#                                                                #
# Computational Complexity:                                      #
# - n, the number of ancestral individuals                       #
# - m, the number of SNPs                                        #
# complexity -> O(n * m)                                         #
#                                                                #
##################################################################

def init_fix_ah(data, param):
    def init_a_fix(A, G):
        return param["A_in"]
    def init_h_fix(H, G):
        return param["H_in"]
    return initdata.init_data(data, init_a_fix, init_h_fix)

def opti_AH_fix_knn(data, param):

    data["A"] = data["A"].astype(np.uint8)
    data["S"] = data["S"].astype(np.uint32)
    data, param = ests.optimize_Sknn(data, param)

    return data, param

fixa_pip_AH_knn = lt.Pipeline(
    initparam.param_initializers["classic_init"],
    init_fix_ah,
    opti_AH_fix_knn
)

def learn_Sknn(pop, A_in, H_in, weights, penalty=40, num_threads=10):
    G_pop = pop["G"]
    H_pop = H_in

    l_res_mix = fixa_pip_AH_knn(G_pop,
                                nb_iter=1, nbclust=len(A_in), penalty=penalty,
                                num_threads=num_threads,
                                weights=weights,
                                A_in=A_in,
                                H_in=H_pop
    )

    return l_res_mix[0]["S"]

def learn_S_join(pop, A_in, penalty=40, small_penalty=0, num_threads=10):
    G_pop = pop["G"]

    l_res_mix = fixa_pip_A_join(G_pop,
                                nb_iter=1, nbclust=len(A_in), penalty=penalty,
                                A_in=A_in,
                                small_penalty=small_penalty,
                                num_threads=num_threads
    )

    return l_res_mix[0]["S"], l_res_mix[0]["H"]

def get_items(dict_object):
    """
    Compatible Python 2 et 3 get item for dictionnary
    """
    for key in dict_object:
        yield key, dict_object[key]

def clusters_to_list_pop(S, l_k):
    """
    From a selection matrix S, compute the origin of each SNP.

    input:
    S -- matrix where we are copying
    l_k -- populations sizes
    """
    res = np.copy(S)

    a = np.repeat(np.arange(len(l_k)), l_k)
    b = np.arange(sum(l_k))
    d = {k: v for v, k in zip(a, b)}
    for k, v in get_items(d): res[S==k] = v
    return res

def locanc_g_knn(l_h, g_adm, penalty=40, small_penalty=0, num_threads=10):
    A_in = np.ascontiguousarray(np.vstack(l_h))
    S_adm, H = learn_S_join({"G": g_adm}, A_in, penalty, small_penalty, num_threads)
    result = clusters_to_list_pop(S_adm, [len(A) for A in l_h])

    return result, S_adm, H

def locanc_h_knn(l_h, h_adm, penalty=40, num_threads=10):
    A_in = np.ascontiguousarray(np.vstack(l_h))
    g_adm = h_adm[::2] + h_adm[1::2]
    n, m = h_adm.shape
    weights = np.ones(m)
    S_adm = learn_Sknn({"G": g_adm, "H": h_adm}, A_in, h_adm, weights, penalty, num_threads)
    result = clusters_to_list_pop(S_adm, [len(A) for A in l_h])

    return result, S_adm

def update_counts(counts, arr, k=2):
    for p in range(k):
        counts[p,:,:][arr == p] += 1
    return counts

def mode(counts):
    argmax = np.argmax(counts, axis=0)
    return argmax, argmax.choose(counts)

def encode_haplo(H):
    H1, H2 = H[::2], H[1::2]
    return ((np.maximum(H1, H2) * (np.maximum(H1, H2) + 1)) / 2) + np.minimum(H1, H2)

def loter_multiple_pops(l_H, h_adm, lambd, num_threads=10, default=True):
    odd = False
    if h_adm.shape[0] % 2 != 0 & default:
        odd = True
        h_adm = np.vstack([h_adm, np.repeat(0, h_adm.shape[1])])

    res_loter, _= locanc_h_knn([h.astype(np.uint8) for h in l_H],
                               h_adm.astype(np.uint8), lambd, num_threads)

    if odd & default:
        res_loter = res_loter[:res_loter.shape[0]-1]

    return res_loter

def boostrap_loter_multiple_pops(l_H, h_adm, lambd, counts, nbrun=20, num_threads=10):

    def shuffle(H):
        n, m = H.shape
        return H[np.random.randint(n, size=n), :]

    if nbrun > 1:
        for i in range(nbrun):
            shuffled_H = [shuffle(h) for h in l_H]
            counts = update_counts(counts,
                                   loter_multiple_pops(shuffled_H,
                                                       h_adm,
                                                       lambd,
                                                       num_threads,
                                                       False),
                                   len(l_H)
            )
    else:
        counts = update_counts(counts,
                               loter_multiple_pops(l_H,
                                                   h_adm,
                                                   lambd,
                                                   num_threads,
                                                   False),
                               len(l_H)
        )

    return counts

def loter_local_ancestry(l_H, h_adm, range_lambda=np.arange(1.5, 5.5, 0.5),
                         rate_vote=0.5, nb_bagging=20, num_threads=10,
                         default=True):

    odd = False
    if h_adm.shape[0] % 2 != 0 & default:
        odd = True
        h_adm = np.vstack([h_adm, np.repeat(0, h_adm.shape[1])])

    input_loter = (l_H, h_adm)
    n, m = h_adm.shape
    counts = np.zeros((len(l_H), n, m))
    for l in range_lambda:
        res_boostrap = boostrap_loter_multiple_pops(*input_loter, lambd=l,
                                                    counts=counts, nbrun=nb_bagging,
                                                    num_threads=num_threads)
    res_tmp = mode(counts)

    if default:
        if odd:
            res_loter = (res_tmp[0][:res_tmp[0].shape[0]-1],
                         res_tmp[1][:res_tmp[1].shape[1]-1])
        else:
            res_loter = res_tmp
        return res_loter
    else:
        r = vote_and_impute(res_tmp, rate_vote)
        return r, res_tmp

def diploid_sim(cluster_found, cluster_truth):
    (n,m) = cluster_found.shape
    return np.count_nonzero(cluster_found == cluster_truth) / float(n*m)

def find_lambda(s_in, threshold = 0.90, min_lambda = 1,
                max_lambda = 500, num_threads=10):
    n, m = s_in.shape
    if max_lambda - min_lambda <= 1:
        return locanc_g_knn([np.zeros((1,m)), np.ones((1,m))],
                            s_in, min_lambda, min_lambda, num_threads)
    else:
        mean = (max_lambda - min_lambda) / 2 + min_lambda
        r_g, s_g, h_g = locanc_g_knn([np.zeros((1,m)), np.ones((1,m))],
                                     s_in, mean, mean, num_threads)
        sim = diploid_sim(r_g[::2] + r_g[1::2], s_in)
        if sim > threshold:
            return find_lambda(s_in, threshold, min_lambda = (max_lambda - min_lambda) / 2 + min_lambda,
                               max_lambda = max_lambda, num_threads=num_threads)
        else:
            return find_lambda(s_in, threshold, min_lambda = min_lambda,
                               max_lambda = max_lambda  - ((max_lambda - min_lambda) / 2),
                               num_threads=num_threads)

def vote_and_impute(s, percent_threshold=0.5):
    def select_val(s, percent_threshold):
        max_s, min_s = np.max(s[1]), np.min(s[1])
        threshold = percent_threshold*(max_s - min_s) + min_s
        select = np.logical_and(s[1][::2] >= threshold,
                                s[1][1::2] >= threshold)
        arr = encode_haplo(s[0])
        arr[np.logical_not(select)] = 255
        return arr

    arr = select_val(s, percent_threshold)

    n, m = arr.shape
    res = np.copy(arr)

    for i in range(n):
        serie = pd.Series(arr[i])
        serie.loc[serie == 255] = np.nan
        try:
            res[i] = serie.dropna().reindex(range(m), method='nearest').values
        except:
            res[i] = arr[i]

    return res

def loter_smooth(l_H, h_adm, range_lambda=np.arange(1.5, 5.5, 0.5),
                 threshold=0.90, rate_vote=0.5, nb_bagging=20, num_threads=10):

    if h_adm.shape[0] % 2 != 0:
        raise ValueError("`loter_smooth` is designed to analyze haplotypes from diploid species, `l_H.shape[0]` should be an even number. In other cases, you can use the function `loter_local_ancestry`.")

    res_impute, res_raw = loter_local_ancestry(l_H, h_adm, range_lambda,
                                               rate_vote, nb_bagging, num_threads,
                                               False)
    result = np.copy(res_impute)
    result_hap = []
    for i in range(len(res_impute)):
        arr_input = np.ascontiguousarray(np.array([res_impute[i]])).astype(np.uint8)
        r, _, _ = find_lambda(arr_input, threshold=threshold, num_threads=num_threads)
        result_hap.append(r)
        result[i] = r[::2] + r[1::2]

    return np.vstack(result_hap)
