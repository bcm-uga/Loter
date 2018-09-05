#if defined(_OPENMP)
#include <omp.h>
#else
#ifndef DISABLE_OPENMP
#pragma message("OpenMP is not available.")
#endif

inline int omp_get_thread_num() { return 0; }
inline int omp_get_num_threads() { return 1; }
inline int omp_get_max_threads() { return 1; }
inline int omp_get_num_procs() { return 1; }
inline void omp_set_num_threads(int nthread) {}
#endif
