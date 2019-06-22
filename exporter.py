#!/usr/bin/env python
# encoding: utf-8
import logging
import os
import time
import sys
import gitlab
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

try:
    loglevel = getattr(logging, os.environ.get('LOGLEVEL', 'WARN').upper())
except AttributeError:
    pass

INTERVAL = int(os.environ.get('INTERVAL', 300))

PORT = int(os.environ.get('PORT', 3001))

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(level=loglevel)

class Proj(object):
    def __init__(self, pr, mrs):
        self.pr = pr
        self.mrs = mrs

gl = gitlab.Gitlab.from_config()

class Collector(object):
    def update(self):
        log.info('updating info')
        projects = gl.projects.list()
        new_mrs = []
        for project in projects:
            for mr in project.mergerequests.list():
                mr.PROJ = project
                new_mrs.append(mr)
        self.mrs = new_mrs

    def collect(self):
        c = GaugeMetricFamily('gitlab_merge_requests', 'Help text', labels=['project_id','project_name','id','state'])
        for mr in self.mrs:
            c.add_metric([str(mr.PROJ.id), str(mr.PROJ.path_with_namespace), str(mr.id), str(mr.state)], 1)
        yield c

if __name__ == '__main__':
    start_http_server(PORT)
    log.info('listening on port {0}'.format(PORT))
    coll = Collector()
    coll.update()
    REGISTRY.register(coll)

    try:
        while True:
            coll.update()
            log.info('sleeping for {0} seconds'.format(INTERVAL))
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print('\nProgram interrupt!\n')
        sys.exit()