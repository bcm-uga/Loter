from __future__ import division

import unittest
import numpy as np

import loter.graph as estimates
import tests.generate_input as gen

class EstimateSTest(unittest.TestCase):

    def setUp(self):
        self.G = np.array([[2,2,0,0],
                           [1,1,0,0],
                           [1,1,1,1]], dtype=np.uint8)
        self.A = np.array([[1,1,0,0],
                           [0,0,1,1]], dtype=np.float32)
        self.H = np.array([[1,1,0,0],
                           [1,1,0,0],
                           [1,0,0,0],
                           [0,1,0,0],
                           [1,1,1,1],
                           [0,0,0,0]], dtype=np.uint8)
        self.S = np.zeros((6,4), dtype=np.uint8)
        self.data = {
            "G": self.G,
            "H": self.H,
            "A": self.A,
            "S": self.S,
        }
        self.param = {
            "penalty": 0.0,
            "nbclust": 2,
            "nb_iter": 10,
            "w_h": 1
        }

    def test_estimates(self):
        ests = estimates.EstimateS()
        ests.run(self.data, self.param)
        res = np.array([[ 0,  0,  0,  0],
                        [ 0,  0,  0,  0],
                        [ 0,  1,  0,  0],
                        [ 1,  0,  0,  0],
                        [ 0,  0,  1,  1],
                        [ 1,  1,  0,  0]])

        self.assertTrue(np.allclose(res, self.data["S"], atol=0.01))

    def test_estimates_penalty(self):
        self.data["A"] = np.array([[1,1,1,0],
                                   [0,0,0,1]], dtype=np.float32)
        self.param["penalty"] = 5.0

        ests = estimates.EstimateS()
        ests.run(self.data, self.param)
        res = np.array([[ 0,  0,  0,  0],
                        [ 0,  0,  0,  0],
                        [ 0,  0,  0,  0],
                        [ 0,  0,  0,  0],
                        [ 0,  0,  0,  0],
                        [ 1,  1,  1,  1]])
        self.assertTrue(np.allclose(res, self.data["S"], atol=0.01))

    def test_estimates_nan(self):
        self.data["G"][0,0] = 3
        self.data["G"][1,1] = 3
        self.data["G"][2,2] = 3
        self.param["penalty"] = 0.0


        ests = estimates.EstimateS()
        ests.run(self.data, self.param)
        res = np.array([[ 0,  0,  0,  0],
                        [ 0,  0,  0,  0],
                        [ 0,  0,  0,  0],
                        [ 1,  1,  0,  0],
                        [ 0,  0,  0,  1],
                        [ 1,  1,  1,  0]])

        self.assertTrue(np.allclose(res, self.data["S"], atol=0.01))

class EstimateSHTest(unittest.TestCase):

    def setUp(self):
        self.G = np.array([[2,2,0,0],
                           [1,1,0,0],
                           [1,1,1,1]], dtype=np.uint8)
        self.A = np.array([[1,1,0,0],
                           [0,0,1,1]], dtype=np.float32)
        self.H = np.array([[1,1,0,0],
                           [1,1,0,0],
                           [1,0,0,0],
                           [0,1,0,0],
                           [1,1,1,1],
                           [0,0,0,0]], dtype=np.uint8)
        self.S = np.zeros((6,4), dtype=np.uint8)
        self.data = {
            "G": self.G,
            "H": self.H,
            "A": self.A,
            "S": self.S,
        }
        self.param = {
            "penalty": 0.0,
            "nbclust": 2,
            "nb_iter": 10,
            "w_h": 1
        }

    def test_estimatesh_penalty(self):
        self.data["A"] = np.array([[1,1,1,0],
                                   [0,0,0,1]], dtype=np.float32)
        self.param["penalty"] = 15.0

        ests = estimates.EstimateSH()
        ests.run(self.data, self.param)
        res = np.array([[ 0,  0,  0,  0],
                        [ 0,  0,  0,  0],
                       	[ 1,  1,  1,  1],
                        [ 0,  0,  0,  0],
                        [ 1,  1,  1,  1],
                        [ 0,  0,  0,  0]])

        self.assertTrue(np.allclose(res, self.data["S"], atol=0.01))
