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

from distutils.core import setup
from os.path import join as pjoin

def read_version_string():
    version = None
    sys.path.insert(0, pjoin(os.getcwd()))
    from pystats import __version__
    version = __version__
    sys.path.pop(0)
    return version

setup(
    name='pymetrics',
    version=read_version_string(),
    description='A unified interface into many cloud server providers',
    author='Rackspace',
    author_email='dev@libcloud.apache.org',
    requires=(),
    packages=[
        'pystats',
    ],
    package_dir={
        'pystats': 'pystats',
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
