from setuptools import find_packages
from distutils.core import setup, Extension
import distutils.util
import os
import sys
from glob import glob

## path
curr_path = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))
src_path = os.path.join(curr_path, 'src')

## src files
src = []
pattern = '*.cpp'
for subdir,_,_ in os.walk(src_path):
    src.extend(glob(os.path.join(subdir, pattern)))

## dependencies
dep = []
patterns = ['*.h', '*.hpp']
for subdir,_,_ in os.walk(src_path):
    for pattern in patterns:
        dep.extend(glob(os.path.join(subdir, pattern)))


## include and linking
incs = []
libdirs = []
libs = []
link_flags = []

## compile flags
cxx_flags = ['-Wall', '-fPIC', '-O3', '-msse2']

if "--no_openmp" in sys.argv:
    cxx_flags.append('-DDISABLE_OPENMP')
    sys.argv.remove("--no_openmp")
    libs = ['stdc++', 'blas', 'lapack']
else:
    cxx_flags.append('-fopenmp')
    link_flags.append('-fopenmp')
    libs += ['stdc++', 'blas', 'lapack', 'gomp']

## C++ extension
loter_wrap = Extension(
    'loter._loter_wrap',
    sources = src,
    include_dirs = incs,
    extra_compile_args = cxx_flags,
    library_dirs = libdirs,
    libraries = libs,
    extra_link_args = link_flags,
    language = 'c++',
    depends = dep,
)


setup(
    name='loter',
    version='1.0',
    description="Optimization Package to phase haplotypes",
    author="Thomas Dias-Alves",
    url = 'https://github.com/bcm-uga/Loter',
    license = "MIT",
    license_files = ('LICENSE.txt',),
    setup_requires=['numpy'],
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "scipy"
    ],
    ext_modules=[loter_wrap,],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['loter_cli=loter.cli:main'],
    },
    data_files=[],
    zip_safe=False
)
