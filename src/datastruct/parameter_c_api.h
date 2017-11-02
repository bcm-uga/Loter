#ifndef PARAMETER_C_API_H
#define PARAMETER_C_API_H

#include "../errorhandler/errorhandler.h"

struct HParameterOptimization;
typedef struct HParameterOptimization* HParameterOptimizationPtr;

#ifdef __cplusplus
extern "C" {
#endif
  HParameterOptimizationPtr parameterOptimization_create(float lambda,
                                                         int nbclust,
                                                         float weight_homozygous,
                                                         int nb_iter,
                                                         ErrorHandler* eh);

  void parameterOptimization_destroy(HParameterOptimizationPtr p,
                                     ErrorHandler* eh);

  void parameterOptimization_set(HParameterOptimizationPtr p,
                                 const char* name,
                                 const char* value,
                                 ErrorHandler* eh);

  const char* parameterOptimization_get(HParameterOptimizationPtr p,
                                        const char* name,
                                        ErrorHandler* eh);
#ifdef __cplusplus
}
#endif

#endif
