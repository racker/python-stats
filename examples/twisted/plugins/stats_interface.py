# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from twisted.application.service import IServiceMaker
from twisted.plugin import IPlugin
from twisted.application import service
from twisted.python import usage

from zope.interface import implements

from pystats.twisted.httpd import add_stats_interface

class Options(usage.Options):
    optParameters = [['port', 'p', None, 'port on which to listen']]

class ServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = 'stats_interface'
    description = 'Twisted service with stats interface'
    options = Options

    def makeService(self, options):
        s = service.MultiService()

        s1 = add_stats_interface(options['port'])
        # s2 = your service...
        s1.setServiceParent(s)
        return s

serviceMaker = ServiceMaker()
