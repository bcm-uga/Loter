#ifndef PARAMETER_OPTI_HPP
#define PARAMETER_OPTI_HPP

#include "../parameter/parameter.h"

#include <string>

struct ParameterOptimization : public Parameter<ParameterOptimization> {
  float penalty;
  int nbclust;
  float w_h;
  int nb_iter;

  ParameterOptimization(float penalty = 2.0, int nbclust = 10, float w_h = 100, int nb_iter = 20) {
    this->penalty = penalty;
    this->nbclust = nbclust;
    this->w_h = w_h;
    this->nb_iter = nb_iter;
    DECLARE_FIELD(penalty, ParameterOptimization);
    DECLARE_FIELD(nbclust, ParameterOptimization);
    DECLARE_FIELD(w_h, ParameterOptimization);
    DECLARE_FIELD(nb_iter, ParameterOptimization);
  }
};

#endif
