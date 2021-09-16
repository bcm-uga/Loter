#!/usr/bin/env python

"""Comand line tool for Local Ancestry Inference (LAI) with Loter
"""

from __future__ import print_function

import os
import sys
import numpy as np
import argparse
import textwrap

import loter.locanc.local_ancestry as lc


def vcf2npy(vcfpath):
    """Convert a haplotype matrix stored in a VCF file to a Numpy array

    Args:
        vcfpath (string): complete VCF file name.

    Return: the haplotype matrix as a Numpy array.
    """
    import allel
    callset = allel.read_vcf(vcfpath)
    haplotypes_1 = callset['calldata/GT'][:,:,0]
    haplotypes_2 = callset['calldata/GT'][:,:,1]

    m, n = haplotypes_1.shape
    mat_haplo = np.empty((2*n, m))
    mat_haplo[::2] = haplotypes_1.T
    mat_haplo[1::2] = haplotypes_2.T

    return mat_haplo.astype(np.uint8)


def load_data(file_name, format="npy", verbose=True):
    """load haplotype array (from saved Numpy array or VCF files)

    Args:
        file_name (string): file storing the haplotype data.
        format (string): data format 'npy' for saved Numpy array, 'vcf' for
            VCF data file. Default is 'npy'.
        verbose (bool): set verbosity. Default is True.

    Return: the haplotype matrix as a Numpy array.
    """
    if verbose:
        print("loading file {}".format(file_name))
    data_array = None
    if format == "npy":
        data_array = np.load(os.path.expanduser(file_name), allow_pickle = True)
    elif format == "txt":
        data_array = np.genfromtxt(os.path.expanduser(file_name), dtype=np.uint8)
    elif format == "vcf":
        try:
            data_array = vcf2npy(file_name)
        except (ModuleNotFoundError):
            print("Using VCF files requires the `scikit-allel` package "
                  + "(available with `pip install scikit-allel`)")
    else:
        raise ValueError("Wrong data file format")
    return data_array.astype(np.uint8)


def main():
    """Command line interface for Loter
    """
    ## args
    parser = argparse.ArgumentParser(
        prog="loter_cli",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description = __doc__,
        epilog=textwrap.dedent('''\
            **Note:**
                Haplotype input matrices should be organised
                as follows: with haplotypes (samples) in rows and SNPs
                in columns. Ancestries of admixed haplotypes inferred by Loter
                will be stored in the same way.
            
            **Important:** When using text format (csv) for input data, 
            missing values should be encoded as 255 or NA.

            Example (run from Loter project root directory):
            loter_cli -r data/H_ceu.npy data/H_yri.npy -a data/H_mex.npy -f npy -o tmp.npy -n 8 -v'''))
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument(
                        "-r", "--ref", nargs='+',
                        help="files storing input reference haplotypes.",
                        required=True)
    requiredNamed.add_argument(
                        "-a", "--adm", nargs=None,
                        help="file storing input admixed haplotypes.",
                        required=True)
    parser.add_argument("-f", "--format", default="npy", nargs=None,
                        help="file format: `npy` (default) for saved numpy arrays, "
                             + "`txt` for csv text files (experimental) "
                             + "or `vcf` for VCF files (which require "
                             + "the `scikit-allel` package). "
                             + "**Note:** all input files (references and admixed) "
                             + "should have the same format.")
    requiredNamed.add_argument(
                        "-o", "--output", nargs=None,
                        help="file to store the infered ancestries of admixed haplotypes, "
                             + "saved as a numpy array by default, or as a text CSV file "
                             + " if the file extension is '.txt'.", required=True)
    parser.add_argument("-n", "--ncore", default=1, type=int, nargs=None,
                        help="Number of CPU cores to use. Default is 1.")
    parser.add_argument("-pc", "--phase_correction",
                        help="Run the phase correction module after the "
                             + "inference algorithm (only available for "
                             + "data from diploid organisms).",
                        action="store_true")
    parser.add_argument("-v", "--verbose", help="Set verbosity on.",
                        action="store_true")
    args = parser.parse_args()

    # set verbosity
    VERBOSE = args.verbose
    def pprint(string):
        """custom print function
        """
        if VERBOSE:
            print(string)

    ## data
    pprint("## Loading reference haplotypes")
    pprint("Using {} reference populations".format(len(args.ref)))
    H_ref = []
    for index, file in enumerate(args.ref):
        H_ref.append(load_data(file, args.format, args.verbose))
        pprint("Dimension of reference haplotype matrix {} = {}"
                    .format(index, H_ref[-1].shape))

    pprint("## Loading admixed haplotypes")
    H_adm = load_data(args.adm, args.format)
    pprint("Dimension of admixed haplotype matrix = {}"
                .format(H_adm.shape))

    pprint("## Run loter")
    res_loter = None
    if args.phase_correction:
        pprint("Using Loter with bagging and phase correction")
        res_loter = lc.loter_smooth(
                        l_H=H_ref, h_adm=H_adm, range_lambda=np.arange(1.5, 5.5, 0.5),
                        threshold=0.90, rate_vote=0.5, nb_bagging=20,
                        num_threads=args.ncore)
    else:
        pprint("Using Loter with bagging")
        res_loter = lc.loter_local_ancestry(
                        l_H=H_ref, h_adm=H_adm, range_lambda=np.arange(1.5, 5.5, 0.5),
                        rate_vote=0.5, nb_bagging=20, num_threads=args.ncore)
        res_loter = res_loter[0]

    pprint("## saving result to file {}".format(args.output))
    if args.output.lower().endswith('.txt'):
        np.savetxt(os.path.expanduser(args.output), res_loter, fmt="%i")
    else:
        np.save(os.path.expanduser(args.output), res_loter)


if __name__ == "__main__":
    main()
