# Note for developpers

## To create a new release

> See the dedicated build [script](./build_pkg.sh).

Create a dedicated python environment:
```bash
python -m venv .pydevenv && source ./.pydevenv/bin/activate
```

Install and run `cibuildwheel` (only for Linux, requirement: `docker`):
```bash
pip install -U cibuildwheel
export CIBW_BEFORE_ALL_LINUX="yum install -y openblas-devel lapack-devel"
python -m cibuildwheel --output-dir wheelhouse --platform linux --arch auto64
```

Build source:
```bash
pip install -U setuptools
python setup.py build sdist
```

## Upload to PyPI

Install and run `twine`:
```bash
pip install twine
cp wheelhouse/* dist/
twine upload dist/*
```
