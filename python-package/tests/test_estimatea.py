from __future__ import division

import unittest
import numpy as np

import loter.estimatea as estimatea
import tests.generate_input as gen

class EstimateATest(unittest.TestCase):

    def setUp(self):
        self.data, self.param = gen.generate_simple_data_param()

    def test_estimatea(self):
        esta = estimatea.EstimateA()
        esta.run(self.data, self.param)

        res = np.array([[1,1,0,0],
                        [2/3,2/3,2/3,0],
                        [1,1,0,0]])

        self.assertTrue(np.allclose(res,self.data["A"]))

    def test_estimatea_nan(self):
        esta = estimatea.EstimateA()
        self.data["G"][0,0] = 3
        self.data["G"][1,2] = 3
        self.data["G"][2,1] = 3
        esta.run(self.data, self.param)

        res = np.array([[0.5,1,0,0],
                        [0.5,2/3,1,0],
                        [1,0.5,0,0]])

        self.assertTrue(np.allclose(res,self.data["A"]))
