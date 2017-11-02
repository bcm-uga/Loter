import numpy as np
import itertools
import loter.tree as tree

from sklearn.cluster import KMeans

def init_data(data, inita, inith):
    data["A"] = inita(data["A"], data["G"]).astype(np.float32)
    data["H"] = inith(data["H"], data["G"])
    return data

def init_a_rand(A, G, randomstate=None,dtype=np.int):
    """Initialize the clusters randomly.

    Initialize an already allocated matrix A (ancestry,cluster,...)
    that is an numpy array with random values between 0 and 1.

    :param A:           Array to initialize
    :type A:            np array
    :param randomstate: RandomState of numpy
    :type randomstate:  np.random.Randomstate
    :param dtype:       Float or Integer values for the array
    :type dtype:        np.dtype
    :returns:           np.array -- Initialized A
    """

    if randomstate == None:
        randomstate = np.random.RandomState()

    (k,m) = A.shape
    if dtype is np.int:
        A = randomstate.randint(0,2,size=(k,m))
    else:
        A = randomstate.random_sample(size=(k,m), dtype=np.float)

    return A

def init_a_selection_g(A, G, randomstate=None, dtype=np.int):

    (k,m) = A.shape
    (n,_) = G.shape

    if randomstate == None:
        randomstate = np.random.RandomState()

    def snp_to_a(snp, dtype):
        if snp == 0:
            return 0
        elif snp == 2:
            return 1
        else:
            if dtype is np.int:
                return randomstate.randint(0,2)
            else:
                return randomstate.uniform()

    for j in range(m):
        selected_snps = randomstate.choice(n,k,replace=False)
        for i, pos_snps in enumerate(selected_snps):
            A[i,j] = snp_to_a(G[pos_snps,j], dtype)

    return A

def init_a_tree(A, G, randomstate=None, dtype=np.int):
    k, m = A.shape
    n, _ = G.shape

    if randomstate == None:
        randomstate = np.random.RandomState()

    rd_split = randomstate.randint(1, m-1)

    A = tree.mat_split(k, G, rd_split)

    return A

def init_a_kmeans(A, G):
    k, m = A.shape
    kmeans = KMeans(n_clusters=k).fit(G/2.0)

    A = np.clip(kmeans.cluster_centers_, 0, 1)
    return A

def init_a_deter(A, G):
    """Initialize the clusters deterministically.

    Initilalize an already allocated matrix A (ancestry,cluster,...)
    that is an numpy array with lines of ones and zeros.

    :param A:           Array to initialize
    :type A:            np array
    :returns:           np.array -- Initialized A
    """

    (k,m) = A.shape
    A[::2] = np.ones(m)

    return A

def init_h_deter(H,G):
    """Initialize the haplotypes deterministically.

    Initilalize an already allocated matrix H (haplotypes)
    that is an numpy array according to G.

    :param H:           Array to initialize
    :type H:            np array
    :param G:           Array of genotypes
    :type G:            np array
    :raises ValueError: Sizes are not compatible
    :returns:           np.array -- Initialized H
    """

    (n,m) = G.shape
    (hn,hm) = H.shape

    if (not hn == 2*n) or (not hm == m):
        raise ValueError("Sizes of H and G are not compatible.")

    def gi_to_hi(x,val):
        vlambd = np.vectorize(lambda xi: val if xi == 1 else xi/2)
        h_i = vlambd(x)

        return h_i

    H1 = np.apply_along_axis(gi_to_hi,1,G,val=0)
    H2 = np.apply_along_axis(gi_to_hi,1,G,val=1)

    H = np.zeros((hn,hm), dtype=np.uint8)
    H[::2] = H1
    H[1::2] = H2

    return H

def init_h_rand(H, G, randomstate=None):
    """Initialize the haplotypes randomly.

    Initilalize an already allocated matrix H (haplotypes)
    that is an numpy array such as according to G.

    :param H:           Array to initialize
    :type H:            np array
    :param G:           Array of genotypes
    :type G:            np array
    :raises ValueError: Sizes are not compatible
    :returns:           np.array -- Initialized H
    """

    if randomstate == None:
        randomstate = np.random.RandomState()

    (n,m) = G.shape
    (hn,hm) = H.shape

    if (not hn == 2*n) or (not hm == m):
        raise ValueError("Sizes of H and G are not compatible.")

    def gi_to_hi(x):
        vlambd = np.vectorize(lambda xi:
                              randomstate.randint(0,2) if xi == 1 else xi/2)
        h_i = vlambd(x)

        return h_i

    H1 = np.apply_along_axis(gi_to_hi,1,G)
    H2 = G - H1

    H = np.ascontiguousarray(np.zeros((hn,hm),dtype=np.uint8))
    H[::2] = H1
    H[1::2] = H2

    return H

def init_rand(data, param):
    return init_data(data, init_a_rand, init_h_rand)

def init_awithg_hrand(data, param):
    return init_data(data, init_a_selection_g, init_h_rand)

def init_atree_hrand(data, param):
    return init_data(data, init_a_tree, init_h_rand)

def init_deter(data, param):
    return init_data(data, init_a_deter, init_h_rand)

def init_kmeans(data, param):
    return init_data(data, init_a_kmeans, init_h_rand)

def create_data(G, param):
    n, m = G.shape
    k = param["nbclust"]
    data = {}
    data["G"] = G
    data["H"] = np.ascontiguousarray(np.zeros((2*n,m), dtype=np.uint8))
    data["S"] = np.ascontiguousarray(np.zeros((2*n,m), dtype=np.uint8))
    data["A"] = np.ascontiguousarray(np.zeros((k,m), dtype=np.float))

    return data

data_initializers = {
    "rand": init_rand,
    "deter": init_deter,
    "a with g, h rand": init_awithg_hrand,
    "a tree": init_awithg_hrand,
    "kmeans": init_kmeans
}
