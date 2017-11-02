create_geno_test <- function() {
  return (matrix(c(0, 0, 1, 0, 2, 1), nrow = 2, byrow = TRUE))
}

create_hap_test <- function() {
  return (matrix(c(0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0), nrow = 4, byrow = TRUE))
}

test <- function() {
  G <- create_geno_test()
  H <- create_hap_test()
  res <- hap_parallel(G, H, 2, 3, 2, 10, 2, 100, 2, 1)
  return (res$H)
}

#' @useDynLib loter hap_parallel_
hap_parallel <- function(G, H, n, m, k, nb_iter,
                         nb_run, w, penalty, num_threads) {
  Gin <- matrix(as.raw(G), n, m)
  Hin <- matrix(as.raw(H), 2 * n, m)
  .Call(hap_parallel_, Gin, Hin, n, m, k, nb_iter,
        nb_run, w, penalty, num_threads)
  return (list(G = G, H = H))
}

run_loter <- function(G) {
  n = dim(G)[1]
  m = dim(G)[2]
  G_loter = matrix(as.raw(G))
  H = matrix(as.raw(0), nrow = 2 * n, ncol = m)
  res = hap_parallel(G_loter, H, n, m, 10, 20, 20, 100, 2.0, 1)
  return(list(G = G_loter, H = H))
}
