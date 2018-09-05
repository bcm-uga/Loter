#ifndef ESTIMATEH_C_API_H
#define ESTIMATEH_C_API_H

#include "../errorhandler/errorhandler.h"
#include "../datastruct/parameter_c_api.h"

struct HEstimateH;
typedef struct HEstimateH* HEstimateHPtr;

typedef void* SelectSwitchPtr;
typedef void* TreatNaNPtr;

#ifdef __cplusplus
extern "C" {
#endif

  SelectSwitchPtr selectswitch_create(ErrorHandler* eh);
  void selectswitch_destroy(SelectSwitchPtr p, ErrorHandler* eh);
  SelectSwitchPtr selectswitchdeter_create(ErrorHandler* eh);
  void selectswitchdeter_destroy(SelectSwitchPtr p, ErrorHandler* eh);
  SelectSwitchPtr selectswitchprob_create(ErrorHandler* eh);
  void selectswitchprob_destroy(SelectSwitchPtr p, ErrorHandler* eh);
  TreatNaNPtr treatnan_create(ErrorHandler* eh);
  void treatnan_destroy(TreatNaNPtr p, ErrorHandler* eh);

  HEstimateHPtr estimateh_create(SelectSwitchPtr ssptr,
                                 TreatNaNPtr ttnanptr,
                                 ErrorHandler* eh);

  void estimateh_destroy(HEstimateHPtr p,
                         ErrorHandler* eh);

  void estimateh_run(HEstimateHPtr esth,
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
