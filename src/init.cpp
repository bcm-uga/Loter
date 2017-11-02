#include "Eigen/Core"
#include "init.hpp"

void init_H(const Ref<const Matrixu8Row> G, Ref< Matrixu8Row> H) {
  size_t nRows = G.rows();
  size_t nCols = G.cols();

  for(size_t i = 0; i < nRows; ++i) {
    for(size_t j = 0; j < nCols; ++j) {
      switch(G(i,j)) {
      case 1:
        if( rand() % 2 == 0 ) {
          H(2*i,j) = 0;
          H(2*i+1,j) = 1;
        } else {
          H(2*i,j) = 1;
          H(2*i+1,j) = 0;
        }
        break;
      case 0:
        H(2*i,j) = 0;
        H(2*i+1,j) = 0;
        break;
      case 2:
        H(2*i,j) = 1;
        H(2*i+1,j) = 1;
      }
    }
  }

  return;
}


void init_A(Ref< MatrixfRow> A) {

  size_t nRows = A.rows();
  size_t nCols = A.cols();

  for(size_t i = 0; i < nRows; ++i) {
    for(size_t j = 0; j < nCols; ++j) {
      A(i,j) = rand() % 2;
    }
  }

  return;
}

void init_A_float(Ref< MatrixfRow> A) {

  size_t nRows = A.rows();
  size_t nCols = A.cols();

  for(size_t i = 0; i < nRows; ++i) {
    for(size_t j = 0; j < nCols; ++j) {
      A(i,j) = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
    }
  }

  return;
}

void init_S(Matrixu8Row& S) {
  return;
}
