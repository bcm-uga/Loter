# Loter

Loter is a Python package for haplotype phasing and local ancestry inference.

Loter is free for academic use only.

Copyright 2017 All rights reserved - Inria, UGA, CNRS

Contact: loter.dev@inria.fr

# Installation

The package require OpenMP (only mandatory for parallel computing), python and g++.

Get Loter sources:
```bash
git clone https://github.com/bcm-uga/Loter.git
```

Install the `loter` Python package:
```bash
cd Loter/python-package/
python setup.py install
```

To install `loter` locally and avoid messing with you system, you can do:
```bash
python setup.py install --user
```
or you can use python virtual environment or a specific Python distribution like Anaconda.

If you do not have OpenMP on your system (especially for MacOS users), you can do:
```bash
python setup.py install --no_openmp
# or
python setup.py install --user --no_openmp
```


# Run the method

## Local Ancestry Inference

For Local Ancestry, see the tutorial in the python-package directory: see [Local Ancestry Example](./python-package/Local_Ancestry_Example.ipynb) available as a Jupyter notebook.

To test it:
```bash
cd Loter/python-package/
jupyter notebook
```

**Reference:** Dias-Alves, T., Mairal, J., Blum, M.G.B., 2018. Loter: A Software Package to Infer Local Ancestry for a Wide Range of Species. Mol Biol Evol 35, 2318–2326. https://doi.org/10.1093/molbev/msy126

**Simulations of admixed individuals:** informations about data simulation are available  [here](https://github.com/BioShock38/aede).


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

**Reference:** Dias Alves, T., 2017. Modélisation du déséquilibre de liaison en génomique des  populations par méthodes l’optimisation. PhD manuscript. Grenoble Alpes University. http://www.theses.fr/2017GREAS052
