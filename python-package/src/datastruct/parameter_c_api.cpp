#include <exception>
#include <string>
#include <vector>
#include <utility>
#include <iostream>

#include "parameter_opti.hpp"

#include "parameter_c_api.h"
#include "../utils/tostring.hpp"
#include "../errorhandler/errorhandler.h"

HParameterOptimizationPtr parameterOptimization_create(float penalty,
                                                       int nbclust,
                                                       float weight_homozygous,
                                                       int nb_iter,
                                                       ErrorHandler* eh) {
  try {
    ParameterOptimization* p = new ParameterOptimization();
    p->penalty = penalty;
    p->nbclust = nbclust;
    p->w_h = weight_homozygous;
    p->nb_iter = nb_iter;
    return reinterpret_cast<HParameterOptimizationPtr>(p);

  } catch (std::exception const& e) {
    if(!eh) {
      basic_eh(e.what(), NULL);
      return NULL;
    } else {
      eh->eh(e.what(), eh->user_data);
      return NULL;
    }
  }
}

void parameterOptimization_destroy(HParameterOptimizationPtr p,
                                   ErrorHandler* eh) {
  try {
    delete reinterpret_cast<ParameterOptimization*>(p);
  } catch (std::exception const& e) {
    if(!eh) {
      basic_eh(e.what(), NULL);
      return;
    } else {
      eh->eh(e.what(), eh->user_data);
      return;
    }
  }
}

void parameterOptimization_set(HParameterOptimizationPtr p,
                               const char* name,
                               const char* value,
                               ErrorHandler* eh) {
  try {
    ParameterOptimization* param = reinterpret_cast<ParameterOptimization*>(p);
    std::string n(name);
    std::string v(value);
    param->Set(n, v);
  } catch (std::exception const& e) {
    if(!eh) {
      basic_eh(e.what(), NULL);
      return;
    } else {
      eh->eh(e.what(), eh->user_data);
      return;
    }
  }
}

const char* parameterOptimization_get(HParameterOptimizationPtr p,
                                      const char* name,
                                      ErrorHandler* eh) {
  try {
    std::string n(name);
    return (reinterpret_cast<ParameterOptimization*>(p))->Get(n).c_str();
  } catch (std::exception const& e) {
    if(!eh) {
      basic_eh(e.what(), NULL);
      return "0.0";
    } else {
      eh->eh(e.what(), eh->user_data);
      return "0.0";
    }
  }
}
