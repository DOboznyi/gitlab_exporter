import time
import sys
import random
import gitlab
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

class Collector(object):
    def collect(self):
        c = GaugeMetricFamily('gitlab_merge_requests', 'Help text', labels=['project_id','project_name','id','state'])
        gl = gitlab.Gitlab('', private_token='')
        gl.auth()
        print("connection completed")
        projects = gl.projects.list()
        for project in projects:
            #print(project.path_with_namespace)
            mrs = project.mergerequests.list()
            for mr in mrs:
                #print(mr.id)
                c.add_metric([str(project.id), str(project.path_with_namespace), str(mr.id), str(mr.state)], 1)
        yield c

if name == '__main__':
    start_http_server(8000)
    coll = Collector()
    REGISTRY.register(coll)

    try:
        while True:
            coll.collect()
            time.sleep(10)

    except KeyboardInterrupt:
        print('\nProgram interrupt!\n')
        sys.exit()