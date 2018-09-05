#ifndef MATRIXTYPE_H
#define MATRIXTYPE_H

#include "../Eigen/Core"
#include <stdint.h>

using namespace Eigen;

typedef Map<Matrix<uint8_t, Dynamic, Dynamic, RowMajor> > MapMatrixu8Row;
typedef Matrix<uint8_t, Dynamic, Dynamic, RowMajor> Matrixu8Row;
typedef Map<Matrix<uint8_t, Dynamic, Dynamic, ColMajor> > MapMatrixu8Col;
typedef Matrix<uint8_t, Dynamic, Dynamic, ColMajor> Matrixu8Col;
typedef Map<Matrix<uint8_t, Dynamic, Dynamic, ColMajor> > MapMatrixu8Col;
typedef Matrix<int, Dynamic, Dynamic, ColMajor> MatrixiCol;
typedef Map<Matrix<int, Dynamic, Dynamic, ColMajor> > MapMatrixiCol;
typedef Matrix<uint32_t, Dynamic, Dynamic, ColMajor> Matrixu32Col;
typedef Map<Matrix<uint32_t, Dynamic, Dynamic, ColMajor> > MapMatrixu32Col;
typedef Matrix<uint32_t, Dynamic, Dynamic, RowMajor> Matrixu32Row;
typedef Map<Matrix<uint32_t, Dynamic, Dynamic, RowMajor> > MapMatrixu32Row;
typedef Map<Matrix<float, Dynamic, Dynamic, RowMajor> > MapMatrixfRow;
typedef Matrix<float, Dynamic, Dynamic, RowMajor> MatrixfRow;

#endif
