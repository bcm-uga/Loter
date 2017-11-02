#include <iostream>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include <limits>
#include "Eigen/Core"

#include "omp.h"
#include "utils/matrixtype.hpp"
#include "graph/graph.hpp"
#include "datastruct/parameter_opti.hpp"
#include "datastruct/parameter_c_api.h"
#include "errorhandler/errorhandler.h"
#include "estimateh/estimateh.hpp"
#include "estimatea/estimatea.hpp"
#include "haplophase.hpp"
#include "init.hpp"

#define NORM(X) ((X) * (X))

using namespace Eigen;

void haplophase_cpp(uint8_t* G_in, uint8_t* H_in_out, float* A_in_out, uint8_t* S_in_out,
                    int n, int m, int k, int nb_iter,
                    float w, float penalty) {

  MapMatrixu8Row G(G_in, n, m);
  MapMatrixu8Row H(H_in_out, 2*n, m);
  MapMatrixfRow A(A_in_out, k, m);
  MapMatrixu8Row S(S_in_out, 2*n, m);

  EstimateH esth;
  EstimateS ests;
  EstimateA esta;
  ParameterOptimization p(penalty, k, w, nb_iter);

  srand(time(NULL));

  init_H(G,H);
  init_A_float(A);

  for(int iter = 0; iter < nb_iter; ++iter) {
    ests.Run(G, H, A, S, p);
    esta.Run(G, H, A, S, p);
    esth.Run(G, H, A, S, p);
  }
  return;
}

void update_count(MatrixXi& count, Ref< Matrixu8Row> H, int n, int m) {
  for(int i = 0; i < n; ++i) {

    int last = -1;
    for(int j = 0; j < m; ++j) {
      if((H(2*i,j) + H(2*i+1,j))== 1) {
        if(last >= 0) {
          if(H(2*i,last)+H(2*i,j) == 1) {
            count(i,j) += 1;
          } else {
            count(i,j) -= 1;
          }
        }
        last = j;
      }
    }
  }
}

void update_count_g(MatrixXi& count_0, MatrixXi& count_1, MatrixXi& count_2,
                    Ref< Matrixu8Row> H, int n, int m) {
  for(int i = 0; i < n; ++i) {
    for(int j = 0; j < m; ++j) {
      int val = H(2*i,j) + H(2*i+1,j);
      switch(val) {
      case 0:
        count_0(i,j)++;
        break;
      case 1:
        count_1(i,j)++;
        break;
      case 2:
        count_2(i,j)++;
        break;
      }
    }
  }
}

void applied_count(MatrixXi& count, Ref< Matrixu8Row> H, int n, int m) {
  for(int i = 0; i < n; ++i) {

    bool was_01 = true;
    for(int j = 0; j < m; ++j) {
      if((H(2*i,j) + H(2*i+1,j))== 1) {
        if(count(i,j) > 0) {
          if(was_01) {
            H(2*i,j) = 1;
            H(2*i+1,j) = 0;
            was_01 = false;
          } else {
            H(2*i,j) = 0;
            H(2*i+1,j) = 1;
            was_01 = true;
          }
        } else {
          if(was_01) {
            H(2*i,j) = 0;
            H(2*i+1,j) = 1;
          } else {
            H(2*i,j) = 1;
            H(2*i+1,j) = 0;
          }
        }
      }
    }
  }
}

void applied_count_g(MatrixXi& count_0, MatrixXi& count_1, MatrixXi& count_2,
                     Ref< Matrixu8Row> G, int n, int m) {
  for(int i = 0; i < n; ++i) {
    for(int j = 0; j < m; ++j) {
      int c_0 = count_0(i,j); 
      int c_1 = count_1(i,j); 
      int c_2 = count_2(i,j); 
      int argmax = 0;
      int max = c_0;
      if(c_0 < c_1) {
        argmax = 1;
        max = c_1;
      }
      if(max < c_2) {
        argmax = 2;
      }
      G(i,j) = argmax;
    }
  }
}

void haplophase_all(uint8_t* G_in, uint8_t* H_out,
                    int n, int m, int k, int nb_iter, int nb_run,
                    float w, float penalty) {

  MapMatrixu8Row G(G_in, n, m);
  MapMatrixu8Row H(H_out, 2*n, m);
  MatrixfRow A(k, m);
  Matrixu8Row S(2*n, m);
  MatrixXi count_h = MatrixXi::Zero(n,m);
  MatrixXi count_0 = MatrixXi::Zero(n,m);
  MatrixXi count_1 = MatrixXi::Zero(n,m);
  MatrixXi count_2 = MatrixXi::Zero(n,m);

  EstimateH esth;
  EstimateS ests;
  EstimateA esta;
  ParameterOptimization p(penalty, k, w, nb_iter);

  srand(time(NULL));

  for(int run = 0; run < nb_run; ++run) {

    std::cout << "Run " << run << std::endl;
    init_H(G,H);
    init_A_float(A);

    for(int iter = 0; iter < nb_iter; ++iter) {
      ests.Run(G, H, A, S, p);
      esta.Run(G, H, A, S, p);
      esth.Run(G, H, A, S, p);
    }
    update_count_g(count_0, count_1, count_2, H, n, m);
    update_count(count_h, H, n, m);
  }
  applied_count_g(count_0,  count_1, count_2, G, n, m);
  init_H(G,H);
  applied_count(count_h, H, n, m);
}

void haplophase_parallel(uint8_t* G_in, uint8_t* H_out,
                         int n, int m, int k, int nb_iter, int nb_run,
                         float w, float penalty, int num_threads) {

  MapMatrixu8Row G (G_in, n, m);
  MapMatrixu8Row H (H_out, 2*n, m);
  MatrixXi count_h = MatrixXi::Zero(n,m);
  MatrixXi count_0 = MatrixXi::Zero(n,m);
  MatrixXi count_1 = MatrixXi::Zero(n,m);
  MatrixXi count_2 = MatrixXi::Zero(n,m);

  EstimateH esth;
  EstimateS ests;
  EstimateA esta;
  ParameterOptimization p(penalty, k, w, nb_iter);

  srand(time(NULL));

  omp_set_num_threads(num_threads);
  #pragma omp parallel for
  for(int run = 0; run < nb_run; ++run) {

    Matrixu8Row Hrun(2*n,m);
    MatrixfRow A(k, m);
    Matrixu8Row S(2*n, m);

    #pragma omp critical
    std::cout << "Run " << run << std::endl;

    init_H(G,Hrun);
    init_A_float(A);

    for(int iter = 0; iter < nb_iter; ++iter) {
      ests.Run(G, Hrun, A, S, p);
      esta.Run(G, Hrun, A, S, p);
      esth.Run(G, Hrun, A, S, p);
    }
    update_count_g(count_0, count_1, count_2, Hrun, n, m);
    update_count(count_h, Hrun, n, m);
  }
  applied_count_g(count_0,  count_1, count_2, G, n, m);
  init_H(G,H);
  applied_count(count_h, H, n, m);
}

void haplophase_lambdvar(uint8_t* G_in, uint8_t* H_out, uint8_t* lambdavar_in, int nb_lambdavar,
                         int n, int m, int k, int nb_iter, int nb_run,
                         float w, float penalty, int num_threads) {

  MapMatrixu8Row G (G_in, n, m);
  MapMatrixu8Row H (H_out, 2*n, m);
  MapMatrixu8Row lambdavar (lambdavar_in, 1, nb_lambdavar);
  MatrixXi count_h = MatrixXi::Zero(n,m);
  MatrixXi count_0 = MatrixXi::Zero(n,m);
  MatrixXi count_1 = MatrixXi::Zero(n,m);
  MatrixXi count_2 = MatrixXi::Zero(n,m);

  EstimateH esth;
  EstimateS ests;
  EstimateAGrad esta;
  ParameterOptimization p(penalty, k, w, nb_iter);

  srand(time(NULL));

  omp_set_num_threads(num_threads);
  #pragma omp parallel for
  for(int run = 0; run < nb_run; ++run) {

    Matrixu8Row Hrun(2*n,m);
    MatrixfRow A(k, m);
    Matrixu8Row S(2*n, m);

    #pragma omp critical
    std::cout << "Run " << run << std::endl;

    init_H(G,Hrun);
    init_A_float(A);

    for(int i_lambd = 0; i_lambd < nb_lambdavar; ++i_lambd) {
      p.penalty = lambdavar(i_lambd);
      for(int iter = 0; iter < nb_iter; ++iter) {
        ests.Run(G, Hrun, A, S, p);
        esta.Run(G, Hrun, A, S, p);
        esth.Run(G, Hrun, A, S, p);
      }
    }
    update_count_g(count_0, count_1, count_2, Hrun, n, m);
    update_count(count_h, Hrun, n, m);
  }
  applied_count_g(count_0,  count_1, count_2, G, n, m);
  init_H(G,H);
  applied_count(count_h, H, n, m);
}
