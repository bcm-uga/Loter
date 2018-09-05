#ifndef INIT_H
#define INIT_H

#include "Eigen/Core"
#include "utils/matrixtype.hpp"

void init_H(const Ref<const Matrixu8Row> G, Ref< Matrixu8Row> H);
void init_A(Ref< MatrixfRow> A);
void init_A_float(Ref< MatrixfRow> A);
void init_S(Ref< Matrixu8Row> S);

#endif
