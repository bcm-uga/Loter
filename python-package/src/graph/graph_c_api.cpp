#include <exception>
#include <string>
#include <vector>
#include <utility>
#include <iostream>

#include "graph.hpp"
#include "../datastruct/parameter_opti.hpp"

#include "graph_c_api.h"
#include "../datastruct/parameter_c_api.h"
#include "../utils/matrixtype.hpp"
#include "../errorhandler/errorhandler.h"

HEstimateSPtr estimates_create(ErrorHandler* eh) {
  try {
    EstimateS* ests = new EstimateS();
    return reinterpret_cast<HEstimateSPtr>(ests);
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

void estimates_destroy(HEstimateSPtr p,
                       ErrorHandler* eh) {
  try {
    delete reinterpret_cast<EstimateS*>(p);
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

void estimates_run(HEstimateSPtr ests,
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

    EstimateS* estimates_ptr = reinterpret_cast<EstimateS*>(ests);
    estimates_ptr->Run(G_mat, H_mat, A_mat, S_mat, *param_opti);
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

HEstimateSHPtr estimatesh_create(ErrorHandler* eh) {
  try {
    EstimateSH* estsh = new EstimateSH();
    return reinterpret_cast<HEstimateSHPtr>(estsh);
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

void estimatesh_destroy(HEstimateSHPtr p,
                        ErrorHandler* eh) {
  try {
    delete reinterpret_cast<EstimateSH*>(p);
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

void estimatesh_run(HEstimateSHPtr estsh,
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

    EstimateSH* estimatesh_ptr = reinterpret_cast<EstimateSH*>(estsh);
    estimatesh_ptr->Run(G_mat, H_mat, A_mat, S_mat, *param_opti);
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

HEstimateSHknnPtr estimateshknn_create(ErrorHandler* eh) {
  try {
    EstimateSHknn* estshknn = new EstimateSHknn();
    return reinterpret_cast<HEstimateSHknnPtr>(estshknn);
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

void estimateshknn_destroy(HEstimateSHknnPtr p,
                           ErrorHandler* eh) {
  try {
    delete reinterpret_cast<EstimateSHknn*>(p);
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

void estimateshknn_run(HEstimateSHknnPtr estshknn,
                       uint8_t* G,
                       uint8_t* H,
                       float* A,
                       uint8_t* S,
                       int n,
                       int m,
                       float small_penalty,
                       int num_threads,
                       HParameterOptimizationPtr param,
                       ErrorHandler* eh) {
  try {
    ParameterOptimization* param_opti = reinterpret_cast<ParameterOptimization*>(param);
    int k = param_opti->nbclust;
    MapMatrixu8Row G_mat(G, n, m);
    MapMatrixu8Row H_mat(H, 2*n, m);
    MapMatrixfRow A_mat(A, k, m);
    MapMatrixu8Row S_mat(S, 2*n, m);

    EstimateSHknn* estimateshknn_ptr = reinterpret_cast<EstimateSHknn*>(estshknn);
    estimateshknn_ptr->Run(G_mat, H_mat, A_mat, S_mat, *param_opti, small_penalty, num_threads);
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

HEstimateSknnPtr estimatesknn_create(ErrorHandler* eh) {
  try {
    EstimateSknn* estsknn = new EstimateSknn();
    return reinterpret_cast<HEstimateSknnPtr>(estsknn);
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

void estimatesknn_destroy(HEstimateSknnPtr p,
                        ErrorHandler* eh) {
  try {
    delete reinterpret_cast<EstimateSknn*>(p);
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

void estimatesknn_run(HEstimateSknnPtr estsknn,
                      uint8_t* H,
                      uint8_t* A,
                      uint32_t* S,
                      float* weights,
                      int n,
                      int m,
                      int num_threads,
                      HParameterOptimizationPtr param,
                      ErrorHandler* eh) {
  try {
    ParameterOptimization* param_opti = reinterpret_cast<ParameterOptimization*>(param);
    int k = param_opti->nbclust;
    MapMatrixu8Col H_mat(H, 2*n, m);
    MapMatrixu8Col A_mat(A, k, m);
    MapMatrixu32Row S_mat(S, 2*n, m);
    Map< VectorXf> weights_vec(weights, m);

    EstimateSknn* estimatesknn_ptr = reinterpret_cast<EstimateSknn*>(estsknn);
    estimatesknn_ptr->Run(H_mat, A_mat, S_mat, *param_opti,
                          weights_vec, num_threads);
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
