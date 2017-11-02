#include "estimateh.hpp"

#include "../utils/matrixtype.hpp"
#include "../datastruct/parameter_opti.hpp"
#include "../utils/missingdata.hpp"
#include "../Eigen/Core"
#include <stdint.h>

SelectSwitch defaultSelectSwitch;

TreatNaN defaultTreatNaN;

void SelectSwitch::calc(float a1, float a2, uint8_t& h1ij, uint8_t& h2ij) {
  float norm_prob = a1 + a2;
  float prob_a = (norm_prob <= 0.001) ? 0.5 : (a1 / norm_prob);

  if( (static_cast<float>(rand()) / static_cast<float>(RAND_MAX))
      <= prob_a ) {
    h1ij = 1;
    h2ij = 0;
  } else {
    h1ij = 0;
    h2ij = 1;
  }
}

void SelectSwitchProb::calc(float a1, float a2, uint8_t& h1ij, uint8_t& h2ij) {
  float norm_prob = a1*(1-a1) + a2*(1-a2);
  float prob_a = (norm_prob <= 0.001) ? 0.5 : (a1*(1-a2) / norm_prob);

  if( (static_cast<float>(rand()) / static_cast<float>(RAND_MAX))
      <= prob_a ) {
    h1ij = 1;
    h2ij = 0;
  } else {
    h1ij = 0;
    h2ij = 1;
  }
}

void SelectSwitchDeter::calc(float a1, float a2, uint8_t& h1ij, uint8_t& h2ij) {
  if(a1 >= a2) {
    h1ij = 1;
    h2ij = 0;
  } else {
    h1ij = 0;
    h2ij = 1;
  }
}

void TreatNaN::calc(float a1, float a2, uint8_t& h1ij, uint8_t& h2ij) {
  h1ij = static_cast<uint8_t> (a1 + 0.5);
  h2ij = static_cast<uint8_t> (a2 + 0.5);
}

void EstimateH::Run(Eigen::Ref< Matrixu8Row> G, Eigen::Ref< Matrixu8Row> H,
                    Eigen::Ref< MatrixfRow> A, Eigen::Ref< Matrixu8Row> S,
                    ParameterOptimization& p) const {

  int n = G.rows();
  int m = G.cols();

  for(int i = 0; i < n; ++i) {
    for(int j = 0; j < m; ++j) {
      float AS1 = A(S(2*i, j),j);
      float AS2 = A(S(2*i+1, j),j);

      if(G(i,j) == 1) {
        selectSwitch->calc(AS1, AS2, H(2*i,j), H(2*i+1,j));
      } else if(G(i,j) == NaN) {
        treatNaN->calc(AS1, AS2, H(2*i,j), H(2*i+1,j));
      }
    }
  }
}
