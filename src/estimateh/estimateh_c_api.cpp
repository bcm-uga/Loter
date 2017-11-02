#include <exception>
#include <string>
#include <vector>
#include <utility>
#include <iostream>

#include "estimateh.hpp"
#include "../datastruct/parameter_opti.hpp"

#include "estimateh_c_api.h"
#include "../datastruct/parameter_c_api.h"
#include "../utils/matrixtype.hpp"
#include "../utils/tostring.hpp"
#include "../errorhandler/errorhandler.h"

SelectSwitchPtr selectswitch_create(ErrorHandler* eh) {
  try {
    return reinterpret_cast<void*>(new SelectSwitch());
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

void selectswitch_destroy(SelectSwitchPtr p, ErrorHandler* eh) {
  try {
    delete reinterpret_cast<SelectSwitch*>(p);
  } catch (std::exception const& e) {
    if(!eh) {
      basic_eh(e.what(), NULL);
    } else {
      eh->eh(e.what(), eh->user_data);
    }
  }
}

SelectSwitchPtr selectswitchdeter_create(ErrorHandler* eh) {
  try {
    return reinterpret_cast<void*>(new SelectSwitchDeter());
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

void selectswitchdeter_destroy(SelectSwitchPtr p, ErrorHandler* eh) {
  try {
    delete reinterpret_cast<SelectSwitchDeter*>(p);
  } catch (std::exception const& e) {
    if(!eh) {
      basic_eh(e.what(), NULL);
    } else {
      eh->eh(e.what(), eh->user_data);
    }
  }
}

SelectSwitchPtr selectswitchprob_create(ErrorHandler* eh) {
  try {
    return reinterpret_cast<void*>(new SelectSwitchProb());
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

void selectswitchprob_destroy(SelectSwitchPtr p, ErrorHandler* eh) {
  try {
    delete reinterpret_cast<SelectSwitchProb*>(p);
  } catch (std::exception const& e) {
    if(!eh) {
      basic_eh(e.what(), NULL);
    } else {
      eh->eh(e.what(), eh->user_data);
    }
  }
}

TreatNaNPtr treatnan_create(ErrorHandler* eh) {
  try {
    return reinterpret_cast<void*>(new TreatNaN());
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

void treatnan_destroy(TreatNaNPtr p, ErrorHandler* eh) {
  try {
    delete reinterpret_cast<TreatNaN*>(p);
  } catch (std::exception const& e) {
    if(!eh) {
      basic_eh(e.what(), NULL);
    } else {
      eh->eh(e.what(), eh->user_data);
    }
  }
}

HEstimateHPtr estimateh_create(SelectSwitchPtr ssptr,
                               TreatNaNPtr ttnanptr,
                               ErrorHandler* eh) {
  try {
    EstimateH* esth;
    if(ssptr == NULL) {
      esth = new EstimateH();
    } else if (ttnanptr == NULL) {
      SelectSwitch* sswitch = reinterpret_cast<SelectSwitch*>(ssptr);
      esth = new EstimateH(sswitch);
    } else {
      SelectSwitch* sswitch = reinterpret_cast<SelectSwitch*>(ssptr);
      TreatNaN* ttnan= reinterpret_cast<TreatNaN*>(ttnanptr);
      esth = new EstimateH(sswitch, ttnan);
    }
    return reinterpret_cast<HEstimateHPtr>(esth);

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

void estimateh_destroy(HEstimateHPtr p,
                       ErrorHandler* eh) {
  try {
    delete reinterpret_cast<EstimateH*>(p);
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

void estimateh_run(HEstimateHPtr esth,
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

    EstimateH* estimateh_ptr = reinterpret_cast<EstimateH*>(esth);
    estimateh_ptr->Run(G_mat, H_mat, A_mat, S_mat, *param_opti);
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
