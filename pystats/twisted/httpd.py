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

import random

try:
    import json
except:
    import simplejson as json

from twisted.python import log
from twisted.web import server, static
from twisted.web.resource import Resource
from twisted.application import service
from twisted.application import internet

from pystats.counter import Counter


def add_stats_interface(port=None, counter=None):
    port = port or random.randint(40000, 60000)
    counter = counter or Counter()

    stats_service = StatsService(counter=counter)
    factory = get_stats_http_server(service=stats_service)
    internet.TCPServer(port, factory).setServiceParent(stats_service)

    log.msg('Stats service HTTP interface listening on port %d' % (port))
    return stats_service


class StatsResource(Resource):

    def __init__(self, service):
        Resource.__init__(self)
        self.service = service
        self.counter = service.get_counter()

    def render_GET(self, req):
        req.setHeader('content-type', 'application/json')
        if req.prepath and req.prepath[0] == 'stats':
            req.setResponseCode(200)
            return json.dumps(self.counter.to_stats(), indent=2)


class StatsService(service.MultiService):

    def __init__(self, counter):
        service.MultiService.__init__(self)
        self.counter = counter

    def get_counter(self):
        return self.counter


def get_stats_http_server(service):
    root = static.File('/dev/null')
    root.putChild('stats', StatsResource(service=service))
    return server.Site(root)
