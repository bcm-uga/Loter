#ifndef ESTIMATEA_C_API_H
#define ESTIMATEA_C_API_H

#include "../errorhandler/errorhandler.h"
#include "../datastruct/parameter_c_api.h"

struct HEstimateA;
typedef struct HEstimateA* HEstimateAPtr;

struct HEstimateAGrad;
typedef struct HEstimateAGrad* HEstimateAGradPtr;

#ifdef __cplusplus
extern "C" {
#endif
  HEstimateAPtr estimatea_create(ErrorHandler* eh);

  void estimatea_destroy(HEstimateAPtr p,
                         ErrorHandler* eh);

  void estimatea_run(HEstimateAPtr esta,
                     uint8_t* G,
                     uint8_t* H,
                     float* A,
                     uint8_t* S,
                     int n,
                     int m,
                     HParameterOptimizationPtr param,
                     ErrorHandler* eh);

  HEstimateAGradPtr estimateagrad_create(ErrorHandler* eh);

  void estimateagrad_destroy(HEstimateAGradPtr p,
                             ErrorHandler* eh);

  void estimateagrad_run(HEstimateAGradPtr esta,
                         uint8_t* G,
                         uint8_t* H,
                         float* A,
                         uint8_t* S,
                         int n,
                         int m,
                         HParameterOptimizationPtr param,
                         ErrorHandler* eh);

#ifdef __cplusplus
}
#endif

#endif
