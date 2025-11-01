# setup.py
from setuptools import setup
from Cython.Build import cythonize
import os

# Set the source file
cython_module = "shop/recommender_cy.pyx"

setup(
    ext_modules = cythonize(cython_module)
)