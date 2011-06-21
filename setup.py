# Licensed to Rackspace, Inc ('Rackspace') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# Rackspace licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import sys

from os.path import basename, splitext, join as pjoin
from glob import glob
from distutils.core import setup
from distutils.core import Command
from unittest import TextTestRunner, TestLoader

TEST_PATHS = ['tests']


def read_version_string():
    version = None
    sys.path.insert(0, pjoin(os.getcwd()))
    from pystats import __version__
    version = __version__
    sys.path.pop(0)
    return version


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        THIS_DIR = os.path.abspath(os.path.split(__file__)[0])
        sys.path.insert(0, THIS_DIR)
        for test_path in TEST_PATHS:
          sys.path.insert(0, pjoin(THIS_DIR, test_path))
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        status = self._run_tests()
        sys.exit(status)

    def _run_tests(self):
        testfiles = []
        for test_path in TEST_PATHS:
            for t in glob(pjoin(self._dir, test_path, 'test_*.py')):
                testfiles.append('.'.join(
                    [test_path.replace('/', '.'), splitext(basename(t))[0]]))

        tests = TestLoader().loadTestsFromNames(testfiles)

        t = TextTestRunner(verbosity=2)
        res = t.run(tests)
        return not res.wasSuccessful()


setup(
    name='pystats',
    version=read_version_string(),
    description='A simple library for recording application-specific metrics',
    author='Rackspace',
    requires=(),
    packages=[
        'pystats',
    ],
    package_dir={
        'pystats': 'pystats',
    },
    cmdclass={
        'test': TestCommand,
    },
    license='Apache License (2.0)',
    url='https://github.com/racker/python-stats',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
