# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

INSTALL_REQUIRES = []
with open(os.path.join(here, 'requirements.txt')) as req:
    INSTALL_REQUIRES = [req.read().split('\n')]

TESTS_REQUIRE = ['nose']
TESTING_REQUIRE = TESTS_REQUIRE + []

setup(name='tr313logger',
      version='0.1',
      description='TR-313j Logger locator',
      url='https://aoisakura.jp',
      author='wataru',
      author_email='wataru@aoisakura.jp',
      license='GPL3',
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES,
      zip_safe=False,
      entry_points={
          'console_scripts': ['convert_log_db=tr313logger.tools.convert_log_db:main',
                              'logger_client=tr313logger.tools.logger_client.main'],
      },
      extras_require={
          'develop': ['pep8'],
          'testing': TESTING_REQUIRE,
      },
      tests_require=TESTS_REQUIRE,
      test_suite='nose.collector',
      long_description='TR-313j Logger locator',
      platforms=['POSIX'],
      classifiers=[
            'Environment :: Web Server',
            'Programming Language :: Python :: 3',
            'Operating System :: POSIX'])
