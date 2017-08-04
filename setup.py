# coding: utf-8
import os
from setuptools import setup, find_packages
from pip.req import parse_requirements


setup(
  name="farmy",
  version="1.0.0",
  packages=find_packages("farmy"),
  package_dir={"": "farmy"},
  include_package_data=True,
  install_requires=[
      str(i.req) for i in parse_requirements(
            os.path.join(os.path.dirname(__file__), 'requirements.txt'), session=False)
  ],
  entry_points={
      'console_scripts': [
          'farmy=farmy:main'
      ]
  },
)
