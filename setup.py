from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='webscraper',
      version=version,
      description="Web scraping tools",
      long_description="""\
Tools to make web scraping a more simple, less repetitive process.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='web scraping urllib2',
      author='Tom Hogans',
      author_email='tomhsx@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
