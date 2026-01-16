# cy_setup.py
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
    ["cy_integrate.pyx", "cy_nogil.pyx"],
    compiler_directives={"language_level": "3"},
    )
)
