# loter

Loter is a package for haplotype phasing and local ancestry inference.

# Installation

Inside the top directory `loter`, compile the C++ library.
The package require openmp , python and g++.

```bash
# inside the top directory run :
make

# or if you do not have OPENMP
make no_omp=1
```

Then we can install the python package.

```bash
# inside the top directory run :
cd python-package/
python setup.py install --user

# or
cd python-package/
python setup.py install
```

# Run the method

## Phasing

Two methods to run the package for phasing

```python
# Directly run the C++ function

import haplophase.wrapper_cpp as hap

G = np.load(os.path.expanduser("FILE"))
G_res = np.copy(G)
H = hap.wrapper_all(G=G_res, k=k, nb_iter=20, nb_run=10, w=100, penalty=2.0)

# You get the imputed genotype matrix in G_res and H the haplotypes.
```

```python
# You can create your own pipeline or select one already existing

import haplophase.pipeline as pipeline
G = np.load(os.path.expanduser("FILE"))

l_res = pipeline.pipelines["classic_pipeline"].run(np.copy(G), nbrun=10, nb_iter=20, nb_run=10, w=100, penalty=2.0)
# You get a list of results that you can combine.

G_res = combine.combiner_G["G vote"](l_res)
H_res = combine.combiner_H["H_mean"](l_res)
```

For Local Ancestry, see the tutorial in the python-package directory.
