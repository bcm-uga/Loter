#ifndef HAP_R_H
#define HAP_R_H

#include <Rinternals.h>
#include <R.h>

extern "C" {
 void hap_parallel_(SEXP G, SEXP H, SEXP n, SEXP m, SEXP k,
                   SEXP nb_iter, SEXP nb_run, SEXP w,
                   SEXP penalty, SEXP num_threads);
}
void hap_parallel_(SEXP G, SEXP H, SEXP n, SEXP m, SEXP k,
                   SEXP nb_iter, SEXP nb_run, SEXP w,
                   SEXP penalty, SEXP num_threads);

#endif
