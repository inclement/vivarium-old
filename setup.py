
from setuptools import setup, find_packages
from os import walk
from os.path import join, dirname, sep
import os
import glob

packages = find_packages()

package_data = {'pywlc': ['*.py',
                          '*_cdef.h',
                          'wlc.c'], }

data_files = []

setup(name='pywm',
      version='0.1',
      description='An experimental Wayland compositor using wlc.',
      author='Alexander Taylor',
      author_email='alexanderjohntaylor@gmail.com',
      url='https://github.com/inclement/pywm', 
      license='MIT', 
      # install_requires=['cffi>=1.0.0'],
      # cffi_modules=['pywm/make_callbacks.py:ffibuilder'],
      packages=packages,
      package_data=package_data,
      )
