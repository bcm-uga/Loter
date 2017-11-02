#include <exception>
#include <string>
#include <vector>
#include <utility>
#include <iostream>

#include "estimatea.hpp"
#include "../datastruct/parameter_opti.hpp"

#include "estimatea_c_api.h"
#include "../datastruct/parameter_c_api.h"
#include "../utils/matrixtype.hpp"
#include "../utils/tostring.hpp"
#include "../errorhandler/errorhandler.h"

HEstimateAPtr estimatea_create(ErrorHandler* eh) {
  try {
    EstimateA* esta = new EstimateA();
    return reinterpret_cast<HEstimateAPtr>(esta);
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

void estimatea_destroy(HEstimateAPtr p,
                       ErrorHandler* eh) {
  try {
    delete reinterpret_cast<EstimateA*>(p);
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

void estimatea_run(HEstimateAPtr esta,
                   uint8_t* G,
                   uint8_t* H,
                   float* A,
                   uint8_t* S,
                   int n,
                   int m,
                   HParameterOptimizationPtr param,
                   ErrorHandler* eh) {
  try {
    ParameterOptimization* param_opti = reinterpret_cast<ParameterOptimization*>(param);
    int k = param_opti->nbclust;
    MapMatrixu8Row G_mat(G, n, m);
    MapMatrixu8Row H_mat(H, 2*n, m);
    MapMatrixfRow A_mat(A, k, m);
    MapMatrixu8Row S_mat(S, 2*n, m);

    EstimateA* estimatea_ptr = reinterpret_cast<EstimateA*>(esta);
    estimatea_ptr->Run(G_mat, H_mat, A_mat, S_mat, *param_opti);
  } catch (std::exception const& e) {
    if (!eh) {
      basic_eh(e.what(), NULL);
      return;
    } else {
      eh->eh(e.what(), eh->user_data);
      return;
    }
  }
}

HEstimateAGradPtr estimateagrad_create(ErrorHandler* eh) {
  try {
    EstimateAGrad* esta = new EstimateAGrad();
    return reinterpret_cast<HEstimateAGradPtr>(esta);
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

void estimateagrad_destroy(HEstimateAGradPtr p,
                           ErrorHandler* eh) {
  try {
    delete reinterpret_cast<EstimateAGrad*>(p);
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

void estimateagrad_run(HEstimateAGradPtr esta,
                       uint8_t* G,
                       uint8_t* H,
                       float* A,
                       uint8_t* S,
                       int n,
                       int m,
                       HParameterOptimizationPtr param,
                       ErrorHandler* eh) {
  try {
    ParameterOptimization* param_opti = reinterpret_cast<ParameterOptimization*>(param);
    int k = param_opti->nbclust;
    MapMatrixu8Row G_mat(G, n, m);
    MapMatrixu8Row H_mat(H, 2*n, m);
    MapMatrixfRow A_mat(A, k, m);
    MapMatrixu8Row S_mat(S, 2*n, m);

    EstimateAGrad* estimatea_ptr = reinterpret_cast<EstimateAGrad*>(esta);
    estimatea_ptr->Run(G_mat, H_mat, A_mat, S_mat, *param_opti);
  } catch (std::exception const& e) {
    if (!eh) {
      basic_eh(e.what(), NULL);
      return;
    } else {
      eh->eh(e.what(), eh->user_data);
      return;
    }
  }
}
