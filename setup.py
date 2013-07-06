"""
Django Laboratory setup.
"""

from setuptools import setup, find_packages

setup( name='django-laboratory',
       version='0.1',
       description='Django app for A/B testing.',
       author='Matt Easterday',
       author_email='easterday@northwestern.edu',
       packages = find_packages(),
       include_package_data = True,
       zip_safe = False,
       install_requires = ['django-ttag']
      )