# Useful links for cythonize|requirements|
# https://stackoverflow.com/questions/38441424/how-to-use-distutils-or-setuptools-in-setup-py-to-make-a-cython-extention-import
# python setup.py build_ext --inplace
from distutils.core import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from distutils.extension import Extension
import numpy as np


setup(
    name='numpy-exts',
    version='0.0.1',
    ext_modules=cythonize([Extension('*', sources=['*/*.pyx'], include_dirs=[np.get_include()])]),
    cmdclass={'build_ext': build_ext},
)
