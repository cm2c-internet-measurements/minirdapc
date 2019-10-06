# setup.py
# Setup for minirdapc
# 20190720 v1

from setuptools import setup, find_namespace_packages

setup(name='minirdapc',
      version='0.3.0',
      description='cm2c Mini RDAP Client',
      url='https://github.com/cm2c-internet-measurements/minirdapc',
      author='Carlos M. Martinez',
      author_email='carlos@lacnic.net',
      license='BSD',
      packages=find_namespace_packages(where='.'),
      install_requires=['ipaddr', 'pyjq', 'click', 'requests'],
      zip_safe=False)