from setuptools import setup, find_packages, Extension
import os

curr_path = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))
lib_path = os.path.join(curr_path, '../lib/', 'libloter.so')

setup(
    name='loter',
    version='0.1',
    description="Optimization Package to phase haplotypes",
    author="Thomas Dias-Alves",
    setup_requires=['numpy'],
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "scipy"
    ],
    packages=find_packages(),
    data_files=[lib_path]
)
