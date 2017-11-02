#!/bin/bash

oldpath=`pwd`
cd ../../

make clean
if make; then
    echo "Successfully build multi-thread loter"
else
    echo "Failed to build multi-thread loter"
    make clean
    make no_omp=1
    echo "Successfully build single-thread xgboost"
fi
cd $oldpath
