#ifndef ESTIMATEH_HPP
#define ESTIMATEH_HPP

#include "../utils/matrixtype.hpp"
#include "../utils/missingdata.hpp"
#include "../datastruct/parameter_opti.hpp"
#include "../Eigen/Core"

#include <stdint.h>

class SelectSwitch {
public:
  SelectSwitch() {}

  virtual void calc(float a1, float a2, uint8_t& h1ij, uint8_t& h2ij);

  virtual ~SelectSwitch() {}
};

extern SelectSwitch defaultSelectSwitch;

class SelectSwitchDeter: public SelectSwitch {
public:
  SelectSwitchDeter() {}

  virtual void calc(float a1, float a2, uint8_t& h1ij, uint8_t& h2ij);

  virtual ~SelectSwitchDeter() {}
};

class SelectSwitchProb: public SelectSwitch {
public:
  SelectSwitchProb() {}

  virtual void calc(float a1, float a2, uint8_t& h1ij, uint8_t& h2ij);

  virtual ~SelectSwitchProb() {}
};

class TreatNaN {
public:
  TreatNaN() {}

  virtual void calc(float a1, float a2, uint8_t& h1ij, uint8_t& h2ij);

  virtual ~TreatNaN() {}
};

extern TreatNaN defaultTreatNaN;

class EstimateH {
public:

  EstimateH(SelectSwitch* ss = &defaultSelectSwitch,
            TreatNaN* tn = &defaultTreatNaN) : selectSwitch(ss), treatNaN(tn) {}
  virtual void Run(Eigen::Ref< Matrixu8Row> G, Eigen::Ref< Matrixu8Row> H,
                   Eigen::Ref< MatrixfRow> A, Eigen::Ref< Matrixu8Row> S,
                   ParameterOptimization& p) const;
  virtual ~EstimateH() {}

private:
  SelectSwitch* selectSwitch;
  TreatNaN* treatNaN;
};

#endif
