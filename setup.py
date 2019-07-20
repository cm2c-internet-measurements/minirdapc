# setup.py
# Setup for minirdapc
# 20190720 v1

from setuptools import setup

setup(name='minirdapc',
      version='0.2.0',
      description='cm2c Mini RDAP Client',
      url='https://github.com/cm2c-internet-measurements/minirdapc',
      author='Carlos M. Martinez',
      author_email='carlos@lacnic.net',
      license='BSD',
      packages=['minirdapc'],
      install_requires=['ipaddr'],
      zip_safe=False)