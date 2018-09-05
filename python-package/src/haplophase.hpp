#ifndef HAPLOPHASE_H
#define HAPLOPHASE_H

#include "Eigen/Core"
#include "utils/matrixtype.hpp"

using namespace Eigen;

extern "C" {
  void haplophase_cpp(uint8_t* G_in, uint8_t* H_in_out, float* A_in_out, uint8_t* S_in_out,
                      int n, int m, int k, int nb_iter,
                      float w, float penalty);

  void haplophase_all(uint8_t* G_in, uint8_t* H_out,
                      int n, int m, int k, int nb_iter, int nb_run,
                      float w, float penalty);

  void haplophase_parallel(uint8_t* G_in, uint8_t* H_out,
                           int n, int m, int k, int nb_iter, int nb_run,
                           float w, float penalty, int num_threads);

  void haplophase_lambdvar(uint8_t* G_in, uint8_t* H_out, uint8_t* lambdavar_in, int nb_lambdavar,
                           int n, int m, int k, int nb_iter, int nb_run,
                           float w, float penalty, int num_threads);
}

void estimate_h(Ref< Matrixu8Row> G, Ref< Matrixu8Row> H, Ref< MatrixfRow> A, Ref< Matrixu8Row> S,
                int m, int n, int k);

void estimate_a(Ref< Matrixu8Row> G, Ref< Matrixu8Row> H, Ref< MatrixfRow> A, Ref< Matrixu8Row> S,
                int m, int n, int k, float w);

void update_count(MatrixXi& count, Ref< Matrixu8Row> H, int n, int m);

void applied_count(MatrixXi& count, Ref< Matrixu8Row> H, int n, int m);

void haplophase_cpp(uint8_t* G_in, uint8_t* H_in_out, float* A_in_out, uint8_t* S_in_out,
                    int n, int m, int k, int nb_iter,
                    float w, float penalty);

void haplophase_all(uint8_t* G_in, uint8_t* H_out,
                    int n, int m, int k, int nb_iter, int nb_run,
                    float w, float penalty);

void haplophase_parallel(uint8_t* G_in, uint8_t* H_out,
                         int n, int m, int k, int nb_iter, int nb_run,
                         float w, float penalty, int num_threads);

void haplophase_lambdvar(uint8_t* G_in, uint8_t* H_out, uint8_t* lambdavar_in, int nb_lambdavar,
                         int n, int m, int k, int nb_iter, int nb_run,
                         float w, float penalty, int num_threads);
#endif
