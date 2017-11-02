from __future__ import division

import unittest
import numpy as np

import loter.estimateh as estimateh
import tests.generate_input as gen

class EstimateHTest(unittest.TestCase):

    def setUp(self):
        self.data, self.param = gen.generate_simple_data_param()

    def test_estimateh(self):
        esth = estimateh.EstimateH()
        l_H = []
        for i in range(10000):
            esth.run(self.data, self.param)
            l_H.append(self.data["H"].astype(np.float32))

        mean_H = np.average(np.dstack(l_H), axis=2)

        res = np.array([[1,1,1,0],
                        [1,1,0,0],
                        [0.5,0.5,0.5,0],
                        [0.5,0.5,0.5,0],
                        [1,1,0,0],
                        [1,1,0,0]
        ])

        self.assertTrue(np.allclose(res, mean_H, atol=0.01))

    def test_estimateh_nan(self):
        self.data["G"][0,0] = 3
        self.data["G"][1,2] = 3
        self.data["G"][2,1] = 3
        esth = estimateh.EstimateH()
        l_H = []
        for i in range(10000):
            esth.run(self.data, self.param)
            l_H.append(self.data["H"].astype(np.float32))

        mean_H = np.average(np.dstack(l_H), axis=2)

        res = np.array([[0,1,1,0],
                        [1,1,0,0],
                        [0.5,0.5,0,0],
                        [0.5,0.5,0,0],
                        [1,1,0,0],
                        [1,1,0,0]
        ])

        self.assertTrue(np.allclose(res, mean_H, atol=0.01))
