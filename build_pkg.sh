# build wheel and source package

## Current working directory (should be root project directory)
WD=$(pwd)

## cleanup on exit
function cleanup() {
    cd $WD
}
trap cleanup EXIT

## create (if necessary) and activate dedicated python environment
PYENV=".pydevenv"
if [[ ! -d ${PYENV} ]]; then
    python -m venv $PYENV
else

source ${PYENV}/bin/activate
pip install -U setuptools cibuildwheel


## go to python package directory
cd python-package

## build wheel (only for Linux 64bits)
export CIBW_BEFORE_ALL_LINUX="yum install -y openblas-devel lapack-devel"
python -m cibuildwheel --output-dir wheelhouse --platform linux --arch auto64

## build source
python setup.py build sdist
