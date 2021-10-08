# Loter

Loter is a Python (and soon R) package for local ancestry inference [1] and haplotype phasing [2].

Loter is available under the MIT license. Copyright 2017 - Inria, UGA, CNRS.

If you encounter any problem or if you have questions regarding Loter,
please open an issue on [Github](https://github.com/bcm-uga/Loter.git),
or you can contact us at <loter.dev@inria.fr>.

## Requirements

The package requires BLAS/LAPACK libraries, OpenMP (optional but recommended for parallel computing), a C++ compiler (tested with g++) and Python 3 (for the Python package). In addition, a version for R is under development.

## Installation

### Python package

#### From PyPI

Run:
```bash
pip install loter
```

> :warning: Precompiled package is only available for Linux 64bits system. On other systems (Linux 32bits, MacOS, Windows), the package will need to be compiled at installation. You must prepare your system by installing all requirements (c.f. [previous section](#requirements)) including OpenMP (mandatory for installation with `pip`).

#### From precompiled package (only on Linux 64bits)

Go to the release page on [Github](https://github.com/bcm-uga/Loter/releases) and download the `loter-*.whl` file corresponding to your Python version, then install Loter by running:
```bash
pip install loter-*.whl
```

> **Note:** replace `loter-*.whl` by the full name of the file you downloaded.

#### From sources

To get Loter sources:
```bash
git clone https://github.com/bcm-uga/Loter.git
```

To install the `loter` Python package:
```bash
# go to package source dir
cd Loter/python-package/
# install
pip install -e .
# or
python setup.py install
```

The following Python packages will be installed during the process as dependencies: `numpy`, `pandas`, `scikit-learn`, `scipy`. If not, you may have to install them before installing `loter`, for instance with the command `pip install numpy pandas scikit-learn scipy`.

To install `loter` locally and avoid messing with your system, you can do:
```bash
python setup.py install --user
```
or you can use a Python virtual environment (recommended) or a specific Python distribution like Anaconda.

If you do not have OpenMP on your system (especially for MacOS users), you can do:
```bash
python setup.py install --no_openmp
# or
python setup.py install --user --no_openmp
```

### R package

A version of Loter will be soon available for R.

> :warning: The development of the version for R is currently paused.


## Use Loter Python package

You can find details about how to run Loter for local ancestry inference (LAI) [1]
and haplotype phasing [2] in Python [here](./python-package/README.md).

In particular, regarding LAI, please check the tutorial in the `python-package` directory:
see [Local Ancestry Example](./python-package/Local_Ancestry_Example.ipynb) available as a Jupyter notebook.

To test it:
```bash
# install jupyter (if not available)
pip install jupyter
# go to package source dir
cd Loter/python-package/
# run jupyter
jupyter notebook
```

> **Note:** The tutorial requires the following additional Python packages: `matplotlib` and `scikit-allel` (you can run `pip install matplotlib scikit-allel` to get them).

In addition, here is a small example of local ancestry inference with Loter:
```python
import os
import numpy as np

# admixed haplotypes
H_adm = np.load(os.path.expanduser("FILE1")) # replace FILE1 by your data file name
# ref 1 haplotypes
H_ref1 = np.load(os.path.expanduser("FILE2")) # replace FILE2 by your data file name
# ref 2 haplotypes
H_ref2 = np.load(os.path.expanduser("FILE3")) # replace FILE3 by your data file name

# Loter local ancestry inference module
import loter.locanc.local_ancestry as lc

## Loter with bagging and phase correction module
res_loter = lc.loter_smooth(l_H=[H_ref1, H_ref2], h_adm=H_adm, num_threads=8) ## set the number of threads
## Loter with bagging only
res_loter = lc.loter_local_ancestry(l_H=[H_ref1, H_ref2], h_adm=H_adm, num_threads=8) ## set the number of threads
```

**Note:** More details are given in the [notebook](./python-package/Local_Ancestry_Example.ipynb),
especially how to load data from VCF files if your data are not available as Numpy arrays.


# Comand line tool

With the Python package installation comes a command line interface `loter_cli`
for **local ancestry inference** that allows you to directly call Loter
from the command line without writing your own Python script.

It requires that your haplotype input data are stored as saved Numpy arrays,
in csv text files (experimental) or in VCF files. In any case, your input
haplotype matrices should be organised as follows: with haplotypes (samples)
in rows and SNPs in columns. Ancestries of admixed haplotypes inferred by Loter
will be stored in the same way.

```bash
# help
loter_cli -h
# examples run in Loter project root directory
cd Loter
# Loter with bagging
loter_cli -r data/H_ceu.npy data/H_yri.npy -a data/H_mex.npy -f npy -o tmp.npy -n 8 -v
# Loter with bagging and phase correction
loter_cli -r data/H_ceu.npy data/H_yri.npy -a data/H_mex.npy -f npy -o tmp.npy -n 8 -pc -v
```

**Important:** When using text format (csv) for input data, missing values should be encoded as 255 or NA.


# References

[1] Dias-Alves, T., Mairal, J., Blum, M.G.B., 2018. Loter: A Software Package to Infer Local Ancestry for a Wide Range of Species. Mol Biol Evol 35, 2318–2326. https://doi.org/10.1093/molbev/msy126

[2] Dias Alves, T., 2017. Modélisation du déséquilibre de liaison en génomique des  populations par méthodes l’optimisation. PhD manuscript. Grenoble Alpes University. http://www.theses.fr/2017GREAS052
