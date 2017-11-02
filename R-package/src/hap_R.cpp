#include <Rinternals.h>
#include <R.h>
#include <stdio.h>

#include "hap_R.h"
#include "src_libloter/haplophase.hpp"

void hap_parallel_(SEXP G, SEXP H, SEXP n, SEXP m, SEXP k,
                   SEXP nb_iter, SEXP nb_run, SEXP w,
                   SEXP penalty, SEXP num_threads) {

  unsigned char* gin = RAW(G);
  unsigned char* hin = RAW(H);

  int nin = asInteger(n);
  int min = asInteger(m);
  int kin = asInteger(k);
  int nbiterin = asInteger(nb_iter);
  int nbrunin = asInteger(nb_run);
  float win = asReal(w);
  float penaltyin = asReal(penalty);
  int numthreadsin = asInteger(nb_run);

  haplophase_parallel(gin, hin, nin, min, kin,
                      nbiterin, nbrunin, win, penaltyin,
                      numthreadsin);
}
