#ifndef GRAPH_C_API_H
#define GRAPH_C_API_H

#include "../errorhandler/errorhandler.h"
#include "../datastruct/parameter_c_api.h"

struct HEstimateS;
typedef struct HEstimateS* HEstimateSPtr;

struct HEstimateSH;
typedef struct HEstimateSH* HEstimateSHPtr;

struct HEstimateSHknn;
typedef struct HEstimateSHknn* HEstimateSHknnPtr;

struct HEstimateSknn;
typedef struct HEstimateSknn* HEstimateSknnPtr;

#ifdef __cplusplus
extern "C" {
#endif
  HEstimateSPtr estimates_create(ErrorHandler* eh);

  void estimates_destroy(HEstimateSPtr p,
                         ErrorHandler* eh);

  void estimates_run(HEstimateSPtr graph,
                     uint8_t* G,
                     uint8_t* H,
                     float* A,
                     uint8_t* S,
                     int n,
                     int m,
                     HParameterOptimizationPtr param,
                     ErrorHandler* eh);

  HEstimateSHPtr estimatesh_create(ErrorHandler* eh);

  void estimatesh_destroy(HEstimateSHPtr p,
                          ErrorHandler* eh);

  void estimatesh_run(HEstimateSHPtr graph,
                      uint8_t* G,
                      uint8_t* H,
                      float* A,
                      uint8_t* S,
                      int n,
                      int m,
                      HParameterOptimizationPtr param,
                      ErrorHandler* eh);

  HEstimateSHknnPtr estimateshknn_create(ErrorHandler* eh);

  void estimateshknn_destroy(HEstimateSHknnPtr p,
                             ErrorHandler* eh);

  void estimateshknn_run(HEstimateSHknnPtr esthknn,
                         uint8_t* G,
                         uint8_t* H,
                         float* A,
                         uint8_t* S,
                         int n,
                         int m,
                         float small_penalty,
                         int num_threads,
                         HParameterOptimizationPtr param,
                         ErrorHandler* eh);

  HEstimateSknnPtr estimatesknn_create(ErrorHandler* eh);

  void estimatesknn_destroy(HEstimateSknnPtr p,
                          ErrorHandler* eh);

  void estimatesknn_run(HEstimateSknnPtr graph,
                        uint8_t* H,
                        uint8_t* A,
                        uint32_t* S,
                        float* weights,
                        int n,
                        int m,
                        int num_threads,
                        HParameterOptimizationPtr param,
                        ErrorHandler* eh);

#ifdef __cplusplus
}
#endif

#endif
