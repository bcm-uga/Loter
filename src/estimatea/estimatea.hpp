#ifndef ESTIMATEA_HPP
#define ESTIMATEA_HPP

#include "../utils/matrixtype.hpp"
#include "../utils/missingdata.hpp"
#include "../datastruct/parameter_opti.hpp"
#include "../Eigen/Core"

#include <stdint.h>

class EstimateA {
public:
  EstimateA() {}
  virtual void Run(Eigen::Ref< Matrixu8Row> G, Eigen::Ref< Matrixu8Row> H,
                   Eigen::Ref< MatrixfRow> A, Eigen::Ref< Matrixu8Row> S,
                   ParameterOptimization& p) const;

  virtual ~EstimateA() {}
};

class EstimateAGrad: public EstimateA {
public:
  EstimateAGrad() {}
  virtual void Run(Eigen::Ref< Matrixu8Row> G, Eigen::Ref< Matrixu8Row> H,
                   Eigen::Ref< MatrixfRow> A, Eigen::Ref< Matrixu8Row> S,
                   ParameterOptimization& p) const;

  virtual ~EstimateAGrad() {}
};

#endif
