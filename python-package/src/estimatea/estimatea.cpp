#include "estimatea.hpp"

#include "../utils/matrixtype.hpp"
#include "../datastruct/parameter_opti.hpp"
#include "../utils/missingdata.hpp"
#include "../Eigen/Core"
#include <stdint.h>
#include <iostream>

void EstimateA::Run(Ref< Matrixu8Row> G, Ref< Matrixu8Row> H, Ref< MatrixfRow> A, Ref< Matrixu8Row> S,
                    ParameterOptimization& p)  const {

  int n = G.rows();
  int m = G.cols();
  int k = p.nbclust;
  float w = p.w_h;

  for(int j = 0; j < m; ++j) {
    Eigen::VectorXf n1 = Eigen::VectorXf::Zero(k);
    Eigen::VectorXf n0 = Eigen::VectorXf::Zero(k);

    for(int i = 0; i < 2*n; ++i) {
      if(G(i/2,j) == 1) {
        if(H(i,j) == 0){
          n0(S(i,j)) += 1;
        } else {
          n1(S(i,j)) += 1;
        }
      } else if(G(i/2,j) == 0 || G(i/2,j) == 2){
        if(H(i,j) == 0){
          n0(S(i,j)) += w;
        } else {
          n1(S(i,j)) += w;
        }
      }
    }

    for(int l = 0; l < k; ++l) {
      if((n1(l) + n0(l)) == 0) {
        A(l,j) = 0.5;
      } else {
        A(l,j) = float(n1(l)) / (n1(l) + n0(l));
      }
    }
  }
}

void EstimateAGrad::Run(Ref< Matrixu8Row> G, Ref< Matrixu8Row> H, Ref< MatrixfRow> A, Ref< Matrixu8Row> S,
                        ParameterOptimization& p)  const {

  int n = G.rows();
  int m = G.cols();
  int k = p.nbclust;
  float w = p.w_h;
  float eta = 0.1;

  for(int j = 0; j < m; ++j) {
    Eigen::VectorXf n1 = Eigen::VectorXf::Zero(k);
    Eigen::VectorXf n0 = Eigen::VectorXf::Zero(k);

    for(int i = 0; i < 2*n; ++i) {
      if(G(i/2,j) == 1) {
        if(H(i,j) == 0){
          n0(S(i,j)) += 1;
        } else {
          n1(S(i,j)) += 1;
        }
      } else if(G(i/2,j) == 0 || G(i/2,j) == 2){
        if(H(i,j) == 0){
          n0(S(i,j)) += w;
        } else {
          n1(S(i,j)) += w;
        }
      }
    }

    for(int l = 0; l < k; ++l) {
      if((n1(l) + n0(l)) != 0) {
        int card_ik = n1(l) + n0(l);
        A(l,j) = (1.0 - eta) * float(A(l,j)) + eta*(float(n1(l)) / card_ik);
      }
    }
  }
}
