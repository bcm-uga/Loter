import numpy as np

def generate_simple_data_param():
    G = np.array([[2,2,1,0],
                  [1,1,1,0],
                  [2,2,0,0]], dtype=np.uint8)

    H = np.array([[1,1,0,0],
                  [1,1,1,0],
                  [0,0,0,0],
                  [1,1,1,0],
                  [1,1,0,0],
                  [1,1,0,0]], dtype=np.uint8)

    A = np.array([[0,0,1,0],
                  [1,0,0,0],
                  [0,1,0,0]], dtype=np.float32)

    S = np.array([[0,0,0,0],
                  [1,1,1,1],
                  [1,1,1,1],
                  [1,1,1,1],
                  [2,2,2,2],
                  [2,2,2,2]], dtype=np.uint8)

    data = {
        "G": G,
        "H": H,
        "A": A,
        "S": S,
    }

    param = {
        "penalty": 2.0,
        "nbclust": 3,
        "nb_iter": 10,
        "w_h": 1
    }

    return (data, param)
