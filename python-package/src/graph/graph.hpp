#ifndef GRAPH_H
#define GRAPH_H

#include "../Eigen/Core"
#include "../utils/matrixtype.hpp"
#include "../datastruct/parameter_opti.hpp"

using namespace Eigen;

class EstimateS {
public:
  EstimateS() {}

  virtual void Run(Ref< Matrixu8Row> G, Ref< Matrixu8Row> H, Ref< MatrixfRow> A, Ref< Matrixu8Row> S,
                   ParameterOptimization &p) const;

  virtual ~EstimateS() {}

protected:
  virtual int s_cost_i(Ref< Matrixu8Row> G, Ref< Matrixu8Row> H, Ref< MatrixfRow> A,
                       VectorXf& graph_s_i_cost, VectorXf& graph_s_i_cost_new,
                       Matrixu8Row& graph_s_i_path,
                       int i, int k, int m,
                       float penalty) const;

  void min_path_ind(int idx_min, Ref< Matrixu8Row> S,
                    VectorXf& graph_s_i_cost, Matrixu8Row& graph_s_i_path,
                    int i, int m, int k) const;
};

class EstimateSknn {
public:
  EstimateSknn() {}

  virtual void Run(Ref< Matrixu8Col> H, Ref< Matrixu8Col> A, Ref< Matrixu32Row> S,
                   ParameterOptimization &p, Ref< VectorXf> weights, int num_threads) const;

  virtual ~EstimateSknn() {}

protected:
  virtual void s_cost_i(Ref< Matrixu8Col> H, Ref< Matrixu8Col> A,
                        Ref< Matrixu32Row> S,
                        int i, Ref< VectorXf> weights,
                        float penalty) const;
};

class EstimateSH {
public:
  EstimateSH() {}

  virtual void Run(Ref< Matrixu8Row> G, Ref< Matrixu8Row> H, Ref< MatrixfRow> A, Ref< Matrixu8Row> S,
                   ParameterOptimization &p) const;

  virtual ~EstimateSH() {}

protected:
  virtual int s_cost_i(Ref< Matrixu8Row> G, Ref< Matrixu8Row> H, Ref< MatrixfRow> A,
                       MatrixXf& graph_s_i_cost,
                       MatrixiCol& graph_s_i_path,
                       int i, int k, int m,
                       float penalty) const;

  void min_path_ind(int idx_min, Ref< Matrixu8Row> S,
                    MatrixiCol& graph_s_i_path,
                    int i, int m, int k) const;
};

class EstimateSHknn {
public:
  EstimateSHknn() {}

  virtual void Run(Ref< Matrixu8Row> G, Ref< Matrixu8Row> H, Ref< MatrixfRow> A, Ref< Matrixu8Row> S,
                   ParameterOptimization &p, float small_penalty, int num_threads) const;

  virtual ~EstimateSHknn() {}

protected:
  virtual int s_cost_i(Ref< Matrixu8Row> G, Ref< Matrixu8Row> H, Ref< MatrixfRow> A,
                       MatrixXf& graph_s_i_cost,
                       MatrixiCol& graph_s_i_path,
                       int i, int k, int m,
                       float penalty, float small_penalty) const;

  void min_path_ind(int idx_min, Ref< Matrixu8Row> S,
                    MatrixiCol& graph_s_i_path,
                    int i, int m, int k) const;
};
#endif
