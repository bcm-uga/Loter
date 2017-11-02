#include <stdint.h>
#include <vector>
#include <algorithm>

#include "../omp.h"
#include "graph.hpp"
#include "../utils/matrixtype.hpp"
#include "../datastruct/parameter_opti.hpp"
#include "../utils/missingdata.hpp"
#include <iostream>

#define NORM(X) ((X) * (X))

int EstimateS::s_cost_i(Ref< Matrixu8Row> G, Ref< Matrixu8Row> H, Ref< MatrixfRow> A,
                        VectorXf& graph_s_i_cost, VectorXf& graph_s_i_cost_new,
                        Matrixu8Row& graph_s_i_path,
                        int i, int k, int m,
                        float penalty) const {
  float mini = std::numeric_limits<float>::max();
  int mini_idx = 0;

  for(int l = 0; l < k; ++l) {
    float cost_l =  NORM(H(i,0) - A(l,0));
    graph_s_i_cost_new(l) = cost_l;
    if(cost_l < mini) {
      mini = cost_l;
      mini_idx = l;
    }
  }

  VectorXf* s_cost_new = &graph_s_i_cost_new;
  VectorXf* s_cost = &graph_s_i_cost;

  float new_mini;
  int new_mini_idx;

  for(int j = 1; j < m; ++j) {

    new_mini = std::numeric_limits<float>::max();
    new_mini_idx = 0;

    VectorXf* temp = s_cost_new;
    s_cost_new = s_cost;
    s_cost = temp;

    for(int l = 0; l < k; ++l) {
      if(G(i/2,j) == NaN) {
        (*s_cost_new)(l) = (*s_cost)(l);
        graph_s_i_path(l,j) = l;
      } else {
        float error = NORM(H(i,j) - A(l,j));
        if(l == mini_idx) {
          (*s_cost_new)(l) = (*s_cost)(l) + error;
          graph_s_i_path(l,j) = mini_idx;
        } else {
          float cost_jump = mini + penalty;
          float cost_not_jump = (*s_cost)(l);
          if(cost_jump < cost_not_jump) {
            (*s_cost_new)(l) = cost_jump + error;
            graph_s_i_path(l,j) = mini_idx;
          } else {
            (*s_cost_new)(l) = cost_not_jump + error;
            graph_s_i_path(l,j) = l;
          }
        }
      }
      if((*s_cost_new)(l) < new_mini) {
        new_mini = (*s_cost_new)(l);
        new_mini_idx = l;
      }
    }
    mini = new_mini;
    mini_idx = new_mini_idx;
  }
  return mini_idx;
}

void EstimateS::min_path_ind(int idx_min, Ref< Matrixu8Row> S,
                             VectorXf& graph_s_i_cost, Matrixu8Row& graph_s_i_path,
                             int i, int m, int k) const {
  int mini_idx = idx_min;

  for(int j = m-1; j >= 0; --j) {
    S(i,j) = mini_idx;
    mini_idx = graph_s_i_path(mini_idx,j);
  }
}

void EstimateS::Run(Ref< Matrixu8Row> G, Ref< Matrixu8Row> H, Ref< MatrixfRow> A, Ref< Matrixu8Row> S,
                    ParameterOptimization &p) const {
  int n = G.rows();
  int m = G.cols();

  int k = p.nbclust;
  float penalty = p.penalty;

  VectorXf graph_s_i_cost(k);
  VectorXf graph_s_i_cost_new(k);
  Matrixu8Row graph_s_i_path = Matrixu8Row::Zero(k,m);

  for(int i = 0; i < 2*n; ++i) {

    int idx_min = this->s_cost_i(G, H, A,
                                 graph_s_i_cost, graph_s_i_cost_new,
                                 graph_s_i_path,
                                 i, k, m,
                                 penalty);
    this->min_path_ind(idx_min, S,
                       graph_s_i_cost_new, graph_s_i_path,
                       i, m, k);
  }
}

void EstimateSknn::Run(Ref< Matrixu8Col> H, Ref< Matrixu8Col> A, Ref< Matrixu32Row> S,
                       ParameterOptimization &p, Ref< VectorXf> weights, int num_threads) const {
  int n = H.rows();

  float penalty = p.penalty;
  VectorXf differentiate(H.cols());

  omp_set_num_threads(num_threads);
  #pragma omp parallel for
  for(int i = 0; i < n; ++i) {

    this->s_cost_i(H, A, S,
                   i,
                   weights,
                   penalty);
  }
}

void EstimateSknn::s_cost_i(Ref< Matrixu8Col> H, Ref< Matrixu8Col> A,
                            Ref< Matrixu32Row> S,
                            int i,
                            Ref< VectorXf> weights,
                            float penalty) const {

  VectorXf cost_nojump;
  VectorXf cost_jump;
  Matrixu8Col::Index m = H.cols();
  MatrixXf::Index minIndex;
  float mini;
  MatrixXf graph_s_i_cost(A.rows(), A.cols());
  MatrixiCol graph_s_i_path(A.rows(), A.cols());

  if(H(i, 0) <= 1) {
    graph_s_i_cost.col(0) = (A.col(0).array() != H(i, 0)).cast<float>();
    mini = graph_s_i_cost.col(0).minCoeff(&minIndex);
  } else { // missing data
    graph_s_i_cost.col(0).setZero();
    mini = graph_s_i_cost.col(0).minCoeff(&minIndex);
  }

  for(int j = 1; j < m; ++j) {
    if (H(i, j) > 1) {
      graph_s_i_cost.col(j) = graph_s_i_cost.col(j-1).cwiseMin(mini + penalty).array();
      graph_s_i_path.col(j) = VectorXi::LinSpaced(graph_s_i_path.rows(), 0, graph_s_i_path.rows()-1);
      graph_s_i_path.col(j) = ((graph_s_i_cost.col(j-1).array() - (mini + penalty)) <= 0.0).select(graph_s_i_path.col(j), minIndex);
    } else {
      graph_s_i_cost.col(j) = weights(j)*(A.col(j).array() != H(i, j)).cast<float>().array() + graph_s_i_cost.col(j-1).cwiseMin(mini + penalty).array();
      graph_s_i_path.col(j) = VectorXi::LinSpaced(graph_s_i_path.rows(), 0, graph_s_i_path.rows()-1);
      graph_s_i_path.col(j) = ((graph_s_i_cost.col(j-1).array() - (mini + penalty)) <= 0.0).select(graph_s_i_path.col(j), minIndex);
      mini = graph_s_i_cost.col(j).minCoeff(&minIndex);
    }
  }

  for(int j = m-1; j >= 0; --j) {
    S(i,j) = minIndex;
    minIndex = graph_s_i_path(minIndex,j);
  }
}

inline int compact_k1k2(int k1, int k2, int k) {
  return k1 * (k) + k2;
}

inline int get_k1(int k1k2, int k) {
  return k1k2 / (k);
}

inline int get_k2(int k1k2, int k) {
  return k1k2 % (k);
}

inline int other_ind(int k) {
  if(k % 2 == 0) {
    return k + 1;
  } else {
    return k - 1;
  }
}

int EstimateSH::s_cost_i(Ref< Matrixu8Row> G, Ref< Matrixu8Row> H, Ref< MatrixfRow> A,
                         MatrixXf& graph_s_i_cost,
                         MatrixiCol& graph_s_i_path,
                         int i, int k, int m,
                         float penalty) const {

  VectorXf min_k_1 = VectorXf::Constant(k, std::numeric_limits<float>::max());
  VectorXi argmin_k_1 = VectorXi::Zero(k);

  VectorXf min_k_2 = VectorXf::Constant(k, std::numeric_limits<float>::max());
  VectorXi argmin_k_2 = VectorXi::Zero(k);

  float min_both_hap = std::numeric_limits<float>::max();
  int argmin_both_hap = 0;
  float cost_k1_k2 = 0;

  for(int k1 = 0; k1 < k; ++k1) {
    for(int k2 = 0; k2 < k; ++k2) {

      // Case of Homozygous Site
      int Hi1 = 0;
      int Hi2 = 0;
      if(G(i, 0) == 0 || G(i,0) == 2) {
        Hi1 = G(i, 0) / 2;
        Hi2 = G(i, 0) / 2;
      } else {
        if(A(k1, 0) >= A(k2, 0)) {
          Hi1 = 1;
          Hi2 = 0;
        } else {
          Hi1 = 0;
          Hi2 = 1;
        }
      }
      cost_k1_k2 =  NORM(Hi1 - A(k1, 0)) + NORM(Hi2 - A(k2, 0));

      graph_s_i_cost(compact_k1k2(k1, k2, k), 0) = cost_k1_k2;

      // jump on k1
      if(min_k_1(k2) >= cost_k1_k2) {
        min_k_1(k2) = cost_k1_k2;
        argmin_k_1(k2) = k1;
      }

      // jump on k2
      if(min_k_2(k1) >= cost_k1_k2) {
        min_k_2(k1) = cost_k1_k2;
        argmin_k_2(k1) = k2;
      }

      // 2 jumps
      if(min_both_hap >= cost_k1_k2) {
        min_both_hap = cost_k1_k2;
        argmin_both_hap = compact_k1k2(k1, k2, k);
      }
    }
  }

  for(int j = 1; j < m; ++j) {
    VectorXf new_min_k_1 = VectorXf::Constant(k, std::numeric_limits<float>::max());
    VectorXi new_argmin_k_1 = VectorXi::Zero(k);

    VectorXf new_min_k_2 = VectorXf::Constant(k, std::numeric_limits<float>::max());
    VectorXi new_argmin_k_2 = VectorXi::Zero(k);

    float new_min_both_hap = std::numeric_limits<float>::max();
    int new_argmin_both_hap = 0;

    for(int k1 = 0; k1 < k; ++k1) {
      for(int k2 = 0; k2 < k; ++k2) {

        int Hi1 = 0;
        int Hi2 = 0;
        if(G(i, j) == 0 || G(i, j) == 2) {
          Hi1 = G(i, j) / 2;
          Hi2 = Hi1;
        } else {
          if(A(k1, j) >= A(k2, j)) {
            Hi1 = 1;
            Hi2 = 0;
          } else {
            Hi1 = 0;
            Hi2 = 1;
          }
        }

        if(G(i, j) == NaN) {
          graph_s_i_cost(compact_k1k2(k1, k2, k), j) = graph_s_i_cost(compact_k1k2(k1, k2, k), j - 1);
          graph_s_i_path(compact_k1k2(k1, k2, k), j) = compact_k1k2(k1, k2, k);
        } else {
          float error = NORM(Hi1 - A(k1, j)) + NORM(Hi2 - A(k2, j));

          std::vector<float> possibles_jump_cost(4);
          std::vector<int> possibles_jump_k1(4);
          std::vector<int> possibles_jump_k2(4);
          // cost no jump
          float cost_no_jump = graph_s_i_cost(compact_k1k2(k1, k2, k), j - 1);
          possibles_jump_cost[0] = cost_no_jump;
          possibles_jump_k1[0] = k1;
          possibles_jump_k2[0] = k2;

          // cost jump on k1
          float min_k1 = min_k_1(k2);
          int argmin_k1 = argmin_k_1(k2);
          float cost_jump_k1 = penalty + min_k1;
          possibles_jump_cost[1] = cost_jump_k1;
          possibles_jump_k1[1] = argmin_k1;
          possibles_jump_k2[1] = k2;

          // cost jump on k2
          float min_k2 = min_k_2(k1);
          int argmin_k2 = argmin_k_2(k1);
          float cost_jump_k2 = penalty + min_k2;
          possibles_jump_cost[2] = cost_jump_k2;
          possibles_jump_k1[2] = k1;
          possibles_jump_k2[2] = argmin_k2;

          // cost 2 jumps
          float min_both = min_both_hap;
          int argmin_both = argmin_both_hap;
          float cost_jump_both = 2 * penalty + min_both;
          possibles_jump_cost[3] = cost_jump_both;
          possibles_jump_k1[3] = get_k1(argmin_both, k);
          possibles_jump_k2[3] = get_k2(argmin_both, k);

          int argmin = std::distance(possibles_jump_cost.begin(),
                                     std::min_element(possibles_jump_cost.begin(),
                                                      possibles_jump_cost.end()));

          cost_k1_k2 = possibles_jump_cost[argmin] + error;
          graph_s_i_cost(compact_k1k2(k1, k2, k), j) = cost_k1_k2;
          graph_s_i_path(compact_k1k2(k1, k2, k), j) = compact_k1k2(possibles_jump_k1[argmin],
                                                                    possibles_jump_k2[argmin],
                                                                    k);

        }

        // jump on k1
        if(new_min_k_1(k2) >= cost_k1_k2) {
          new_min_k_1(k2) = cost_k1_k2;
          new_argmin_k_1(k2) = k1;
        }

        // jump on k2
        if(new_min_k_2(k1) >= cost_k1_k2) {
          new_min_k_2(k1) = cost_k1_k2;
          new_argmin_k_2(k1) = k2;
        }

        // 2 jumps
        if(new_min_both_hap >= cost_k1_k2) {
          new_min_both_hap = cost_k1_k2;
          new_argmin_both_hap = compact_k1k2(k1, k2, k);
        }
      }
    }
    argmin_k_1 = new_argmin_k_1;
    min_k_1 = new_min_k_1;
    argmin_k_2 = new_argmin_k_2;
    min_k_2 = new_min_k_2;
    argmin_both_hap = new_argmin_both_hap;
    min_both_hap = new_min_both_hap;

  }
  return argmin_both_hap;
}

void EstimateSH::min_path_ind(int idx_min, Ref< Matrixu8Row> S,
                              MatrixiCol& graph_s_i_path,
                              int i, int m, int k) const {
  int mini_idx = idx_min;

  for(int j = m-1; j >= 0; --j) {
    int k1 = get_k1(mini_idx, k);
    int k2 = get_k2(mini_idx, k);
    S(2*i,j) = k1;
    S(2*i + 1,j) = k2;
    mini_idx = graph_s_i_path(mini_idx, j);
  }
}

void EstimateSH::Run(Ref< Matrixu8Row> G, Ref< Matrixu8Row> H, Ref< MatrixfRow> A, Ref< Matrixu8Row> S,
                    ParameterOptimization &p) const {
  int n = G.rows();
  int m = G.cols();

  int k = p.nbclust;
  float penalty = p.penalty;

  MatrixXf graph_s_i_cost = MatrixXf::Zero(k*k, m);
  MatrixiCol graph_s_i_path = MatrixiCol::Zero(k*k, m);

  for(int i = 0; i < n; ++i) {

      int idx_min = this->s_cost_i(G, H, A,
                                 graph_s_i_cost,
                                 graph_s_i_path,
                                 i, k, m,
                                 penalty);
    this->min_path_ind(idx_min, S,
                       graph_s_i_path,
                       i, m, k);
  }
}

int EstimateSHknn::s_cost_i(Ref< Matrixu8Row> G, Ref< Matrixu8Row> H, Ref< MatrixfRow> A,
                         MatrixXf& graph_s_i_cost,
                         MatrixiCol& graph_s_i_path,
                         int i, int k, int m,
                         float penalty, float small_penalty) const {

  VectorXf min_k_1 = VectorXf::Constant(k, std::numeric_limits<float>::max());
  VectorXi argmin_k_1 = VectorXi::Zero(k);

  VectorXf min_k_2 = VectorXf::Constant(k, std::numeric_limits<float>::max());
  VectorXi argmin_k_2 = VectorXi::Zero(k);

  float min_both_hap = std::numeric_limits<float>::max();
  int argmin_both_hap = 0;
  float cost_k1_k2 = 0;

  for(int k1 = 0; k1 < k; ++k1) {
    for(int k2 = 0; k2 < k; ++k2) {

      // Case of Homozygous Site
      int Hi1 = 0;
      int Hi2 = 0;
      if(G(i, 0) == 0 || G(i,0) == 2) {
        Hi1 = G(i, 0) / 2;
        Hi2 = G(i, 0) / 2;
      } else {
        if(A(k1, 0) >= A(k2, 0)) {
          Hi1 = 1;
          Hi2 = 0;
        } else {
          Hi1 = 0;
          Hi2 = 1;
        }
      }
      cost_k1_k2 =  NORM(Hi1 - A(k1, 0)) + NORM(Hi2 - A(k2, 0));

      graph_s_i_cost(compact_k1k2(k1, k2, k), 0) = cost_k1_k2;

      // jump on k1
      if(min_k_1(k2) >= cost_k1_k2) {
        min_k_1(k2) = cost_k1_k2;
        argmin_k_1(k2) = k1;
      }

      // jump on k2
      if(min_k_2(k1) >= cost_k1_k2) {
        min_k_2(k1) = cost_k1_k2;
        argmin_k_2(k1) = k2;
      }

      // 2 jumps
      if(min_both_hap >= cost_k1_k2) {
        min_both_hap = cost_k1_k2;
        argmin_both_hap = compact_k1k2(k1, k2, k);
      }
    }
  }

  for(int j = 1; j < m; ++j) {
    VectorXf new_min_k_1 = VectorXf::Constant(k, std::numeric_limits<float>::max());
    VectorXi new_argmin_k_1 = VectorXi::Zero(k);

    VectorXf new_min_k_2 = VectorXf::Constant(k, std::numeric_limits<float>::max());
    VectorXi new_argmin_k_2 = VectorXi::Zero(k);

    float new_min_both_hap = std::numeric_limits<float>::max();
    int new_argmin_both_hap = 0;

    for(int k1 = 0; k1 < k; ++k1) {
      for(int k2 = 0; k2 < k; ++k2) {

        int Hi1 = 0;
        int Hi2 = 0;
        if(G(i, j) == 0 || G(i, j) == 2) {
          Hi1 = G(i, j) / 2;
          Hi2 = Hi1;
        } else {
          if(A(k1, j) >= A(k2, j)) {
            Hi1 = 1;
            Hi2 = 0;
          } else {
            Hi1 = 0;
            Hi2 = 1;
          }
        }

        if(G(i, j) == NaN) {
          graph_s_i_cost(compact_k1k2(k1, k2, k), j) = graph_s_i_cost(compact_k1k2(k1, k2, k), j - 1);
          graph_s_i_path(compact_k1k2(k1, k2, k), j) = compact_k1k2(k1, k2, k);
        } else {
          float error = NORM(Hi1 - A(k1, j)) + NORM(Hi2 - A(k2, j));

          std::vector<float> possibles_jump_cost(7);
          std::vector<int> possibles_jump_k1(7);
          std::vector<int> possibles_jump_k2(7);
          // cost no jump
          float cost_no_jump = graph_s_i_cost(compact_k1k2(k1, k2, k), j - 1);
          possibles_jump_cost[0] = cost_no_jump;
          possibles_jump_k1[0] = k1;
          possibles_jump_k2[0] = k2;

          // cost jump on k1
          float min_k1 = min_k_1(k2);
          int argmin_k1 = argmin_k_1(k2);
          float cost_jump_k1 = penalty + min_k1;
          possibles_jump_cost[1] = cost_jump_k1;
          possibles_jump_k1[1] = argmin_k1;
          possibles_jump_k2[1] = k2;

          // cost jump on k2
          float min_k2 = min_k_2(k1);
          int argmin_k2 = argmin_k_2(k1);
          float cost_jump_k2 = penalty + min_k2;
          possibles_jump_cost[2] = cost_jump_k2;
          possibles_jump_k1[2] = k1;
          possibles_jump_k2[2] = argmin_k2;

          // cost 2 jumps
          float min_both = min_both_hap;
          int argmin_both = argmin_both_hap;
          float cost_jump_both = 2 * penalty + min_both;
          possibles_jump_cost[3] = cost_jump_both;
          possibles_jump_k1[3] = get_k1(argmin_both, k);
          possibles_jump_k2[3] = get_k2(argmin_both, k);

          float cost_small_jump = graph_s_i_cost(compact_k1k2(other_ind(k1), k2, k), j - 1) + small_penalty;
          possibles_jump_cost[4] = cost_small_jump;
          possibles_jump_k1[4] = other_ind(k1);
          possibles_jump_k2[4] = k2;

          cost_small_jump = graph_s_i_cost(compact_k1k2(k1, other_ind(k2), k), j - 1) + small_penalty;
          possibles_jump_cost[5] = cost_small_jump;
          possibles_jump_k1[5] = k1;
          possibles_jump_k2[5] = other_ind(k2);

          cost_small_jump = graph_s_i_cost(compact_k1k2(other_ind(k1), other_ind(k2), k), j - 1) + small_penalty;
          possibles_jump_cost[6] = cost_small_jump;
          possibles_jump_k1[6] = other_ind(k1);
          possibles_jump_k2[6] = other_ind(k2);


          int argmin = std::distance(possibles_jump_cost.begin(),
                                     std::min_element(possibles_jump_cost.begin(),
                                                      possibles_jump_cost.end()));

          cost_k1_k2 = possibles_jump_cost[argmin] + error;
          graph_s_i_cost(compact_k1k2(k1, k2, k), j) = cost_k1_k2;
          graph_s_i_path(compact_k1k2(k1, k2, k), j) = compact_k1k2(possibles_jump_k1[argmin],
                                                                    possibles_jump_k2[argmin],
                                                                    k);

        }

        // jump on k1
        if(new_min_k_1(k2) >= cost_k1_k2) {
          new_min_k_1(k2) = cost_k1_k2;
          new_argmin_k_1(k2) = k1;
        }

        // jump on k2
        if(new_min_k_2(k1) >= cost_k1_k2) {
          new_min_k_2(k1) = cost_k1_k2;
          new_argmin_k_2(k1) = k2;
        }

        // 2 jumps
        if(new_min_both_hap >= cost_k1_k2) {
          new_min_both_hap = cost_k1_k2;
          new_argmin_both_hap = compact_k1k2(k1, k2, k);
        }
      }
    }
    argmin_k_1 = new_argmin_k_1;
    min_k_1 = new_min_k_1;
    argmin_k_2 = new_argmin_k_2;
    min_k_2 = new_min_k_2;
    argmin_both_hap = new_argmin_both_hap;
    min_both_hap = new_min_both_hap;

  }
  return argmin_both_hap;
}
void EstimateSHknn::min_path_ind(int idx_min, Ref< Matrixu8Row> S,
                              MatrixiCol& graph_s_i_path,
                              int i, int m, int k) const {
  int mini_idx = idx_min;

  for(int j = m-1; j >= 0; --j) {
    int k1 = get_k1(mini_idx, k);
    int k2 = get_k2(mini_idx, k);
    S(2*i,j) = k1;
    S(2*i + 1,j) = k2;
    mini_idx = graph_s_i_path(mini_idx, j);
  }
}

void EstimateSHknn::Run(Ref< Matrixu8Row> G, Ref< Matrixu8Row> H, Ref< MatrixfRow> A, Ref< Matrixu8Row> S,
                        ParameterOptimization &p, float small_penalty, int num_threads) const {
  int n = G.rows();
  int m = G.cols();

  int k = p.nbclust;
  float penalty = p.penalty;

  omp_set_num_threads(num_threads);
  #pragma omp parallel for
  for(int i = 0; i < n; ++i) {

      MatrixXf graph_s_i_cost = MatrixXf::Zero(k*k, m);
      MatrixiCol graph_s_i_path = MatrixiCol::Zero(k*k, m);

      int idx_min = this->s_cost_i(G, H, A,
                                 graph_s_i_cost,
                                 graph_s_i_path,
                                 i, k, m,
                                 penalty, small_penalty);
      this->min_path_ind(idx_min, S,
                         graph_s_i_path,
                         i, m, k);
  }
}
