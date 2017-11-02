def build_init_param(penalty=2.0, nbclust=10, w_h=100, nb_iter=10):
    def init_param(G, **kwargs):
        param = {"penalty": penalty,
                "nbclust": nbclust,
                "w_h": w_h,
                "nb_iter": nb_iter}

        for key, value in list(kwargs.items()):
            param[key] = value

        return param

    return init_param

param_initializers = {
    "classic_init": build_init_param()
}
