import numpy as np
from itertools import product

import loter.initparam as initparam
import loter.initdata as initdata
import loter.opti as opti
import loter.estimatea as esta
import loter.estimateh as esth
import loter.graph as ests
import loter.predcombine as combiner
import loter.metrics as metrics
"""
A Pipeline is a function taking the matrix Genotype in input and
return some results.
"""
def build_pipeline(init_param, init_data, opti):
    def pipeline(G, **kwargs):
        param = init_param(G, **kwargs)
        data = initdata.create_data(G, param)
        data = init_data(data, param)
        res = opti(data, param)
        return res

    return pipeline

class Pipeline(object):

    def __init__(self, init_param, init_data, opti):
        self.init_param = init_param
        self.init_data = init_data
        self.opti = opti

    def __call__(self, G, **kwargs):
        self.pipeline = build_pipeline(self.init_param,
                                       self.init_data,
                                       self.opti)

        return self.pipeline(G, **kwargs)

    def run(self, G, nbrun=10, **kwargs):
        l_res = []

        self.pipeline = build_pipeline(self.init_param,
                                       self.init_data,
                                       self.opti)

        for i in range(nbrun):
            l_res.append(self.pipeline(G, **kwargs))

        return l_res

class PipelineCrossValidate(Pipeline):

    def __call__(self, G, **kwargs):
        param_initializer = self.init_param(G, **kwargs)
        self.pipeline = build_pipeline(param_initializer,
                                       self.init_data,
                                       self.opti)

        return self.pipeline(G, **kwargs)

    def run(self, G, nbrun=10, **kwargs):
        l_res = []

        param_initializer = self.init_param(G, **kwargs)
        self.pipeline = build_pipeline(param_initializer,
                                       self.init_data,
                                       self.opti)

        for i in range(nbrun):
            print("Run {0}".format(i))
            l_res.append(self.pipeline(G, **kwargs))

        return l_res

def cross_validate_param(G, p_sampling=0.1, w_h=100, nb_iter=20, **kwargs):

    (n, m) = G.shape
    param_cr = {
        "w_h": w_h,
        "nb_iter": nb_iter
    }

    for key, value in list(kwargs.items()):
        param_cr[key] = value


    grid = list(product(
        np.arange(1.0, 3.0, 0.2),
        np.arange(5, max(10, n/2), 10),
        (param_cr["w_h"],),
        (param_cr["nb_iter"],)
    ))

    l_error = []
    for penalty, nbclust, w_h, nb_iter in grid:
        param = {"penalty": penalty,
                "nbclust": nbclust,
                "w_h": w_h,
                "nb_iter": nb_iter}

        G_in = np.copy(G[:,:min(n,5000)])
        G_nan = np.copy(G_in)
        selected_idx = np.where(G_nan != 3)
        sample_idx = np.random.choice([True, False],
                                      size=len(selected_idx[0]),
                                      p=[p_sampling, 1.0-p_sampling])
        masked_idx = (selected_idx[0][sample_idx], selected_idx[1][sample_idx])
        G_nan[masked_idx] = 3
        G_nan.astype(np.uint8)

        method = pipelines["classic_pipeline"]
        l_res = method.run(G_nan, nbrun=20, **param)
        G_res = combiner.combiner_G["G vote"](l_res)
        error = metrics.imputation_error_rate(G_res, G_in, G_nan)
        l_error.append((param, error))
        #print(error, param)

    param_min = min(l_error, key = lambda t: t[1])[0]

    #print("Selected Parameters : ")
    #print(param_min)

    def init_param(G, **kwargs):
        param = param_min

        for key, value in list(kwargs.items()):
            param[key] = value

        return param

    return init_param

def applied_cross_validate_param(G, **kwargs):
    return cross_validate_param(G, **kwargs)(G, **kwargs)

classic_pipeline = Pipeline(
    initparam.param_initializers["classic_init"],
    initdata.data_initializers["rand"],
    opti.opti["classic_opti"]
)

tree_pipeline = Pipeline(
    initparam.param_initializers["classic_init"],
    initdata.data_initializers["a tree"],
    opti.opti["classic_opti"]
)

tree_join_pipeline = Pipeline(
    initparam.param_initializers["classic_init"],
    initdata.data_initializers["a tree"],
    opti.opti["join_opti"]
)

tree_oldh_pipeline = Pipeline(
    initparam.param_initializers["classic_init"],
    initdata.data_initializers["a tree"],
    opti.opti["opti_h_old"]
)

classic_pipeline_prob = Pipeline(
    initparam.param_initializers["classic_init"],
    initdata.data_initializers["rand"],
    opti.opti_build(
        esth.optih["opti_prob"],
        esta.optimize_A,
        ests.optimize_S
    )
)

pipeline_old_h = Pipeline(
    initparam.param_initializers["classic_init"],
    initdata.data_initializers["rand"],
    opti.opti["opti_h_old"]
)

classic_crossvalidate_pipeline = PipelineCrossValidate(
    cross_validate_param,
    initdata.data_initializers["rand"],
    opti.opti["classic_opti"]
)

classic_crossvalidate_ag_pipeline = PipelineCrossValidate(
    cross_validate_param,
    initdata.data_initializers["a with g, h rand"],
    opti.opti["classic_opti"]
)

join_ag_pipeline = Pipeline(
    initparam.param_initializers["classic_init"],
    initdata.data_initializers["a with g, h rand"],
    opti.opti["join_opti"]
)

join_then_classic_pipeline = PipelineCrossValidate(
    cross_validate_param,
    initdata.data_initializers["a with g, h rand"],
    opti.opti["join_then_classic"]
)

join_then_classic_pipeline_withsampling = PipelineCrossValidate(
    cross_validate_param,
    initdata.data_initializers["a with g, h rand"],
    opti.opti["join_then_classic_withsampling"]
)

join_then_classic_pipeline_initkmeans = PipelineCrossValidate(
    cross_validate_param,
    initdata.data_initializers["kmeans"],
    opti.opti["join_then_classic"]
)

join_initkmeans_balance = Pipeline(
    initparam.param_initializers["classic_init"],
    initdata.data_initializers["kmeans"],
    opti.opti["join_balance"]
)

classic_crosseach_pipeline = Pipeline(
    applied_cross_validate_param,
    initdata.data_initializers["rand"],
    opti.opti["classic_opti"]
)

pipelines = {
    "classic_pipeline": classic_pipeline,
    "pipeline_old_h": pipeline_old_h,
    "crossvalidate": classic_crossvalidate_pipeline,
    "cross_ag": classic_crossvalidate_ag_pipeline,
    "join_ag": join_ag_pipeline,
    "join_then_classic": join_then_classic_pipeline,
    "join_then_classic_withsampling": join_then_classic_pipeline_withsampling,
    "join_then_classic_initkmeans": join_then_classic_pipeline_initkmeans,
    "join_initkmeans_balance": join_initkmeans_balance,
    "crosseachvalidate": classic_crosseach_pipeline
}
