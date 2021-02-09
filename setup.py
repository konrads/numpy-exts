# # Useful links for cythonize|requirements|
# # https://stackoverflow.com/questions/38441424/how-to-use-distutils-or-setuptools-in-setup-py-to-make-a-cython-extention-import
# # python setup.py build_ext --inplace
# from distutils.core import setup
# from Cython.Build import cythonize
# from Cython.Distutils import build_ext
# from distutils.extension import Extension
# import numpy as np
#
#
# setup(
#     name='numpy-exts',
#     version='0.0.1',
#     ext_modules=cythonize([Extension('*', sources=['*/*.pyx'], include_dirs=[np.get_include()])]),
#     cmdclass={'build_ext': build_ext},
# )


# for Rust: https://pypi.org/project/setuptools-rust/
from setuptools import setup, Extension
from setuptools_rust import Binding, RustExtension
import numpy as np

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

try:
  from Cython.Build import cythonize
except ImportError:
  # create closure for deferred import
  def cythonize (*args, ** kwargs ):
    from Cython.Build import cythonize
    return cythonize(*args, ** kwargs)

setup(
  name='numpy-exts',
  version='0.1.0',
  install_requires=requirements,
  tests_require=['pytest'],
  ext_modules=cythonize([Extension('*', sources=['*/*.pyx'], include_dirs=[np.get_include()])]),
  rust_extensions=[RustExtension('npexts.rust_trade_fsm', binding=Binding.PyO3)],
  packages=['npexts'],
  # rust extensions are not zip safe, just like C-extensions.
  zip_safe=False,
)
