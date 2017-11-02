import numpy as np
import loter.locanc.local_ancestry as lc

anc_1 = np.array([[1,1,1,1,1],
                  [1,1,1,1,1]])
anc_2 = np.array([[0,0,0,0,0],
                  [0,0,0,0,0]])

met = np.array([[0,0,0,0,0],
                [1,1,1,1,1]])

res = lc.loter_smooth([anc_1, anc_2], met)

print(res)
