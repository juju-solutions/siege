#!/usr/bin/python

from charmhelpers.core.services.base import ServiceManager
from charmhelpers.core.services import helpers

import actions
from charmhelpers.core import hookenv

try:
    from charmbenchmark import Benchmark
except ImportError:
    import subprocess
    from charmhelpers.fetch import apt_install

    apt_install('python-pip', fatal=True)
    cmd = ['pip', 'install', '-U', 'charm-benchmark']
    subprocess.call(cmd)
    from charmbenchmark import Benchmark


class BenchmarkRelation(helpers.RelationContext):
    """
    Stub interface to connect the ServiceFramework to a Benchmark relation
    """
    interface = 'benchmark'
    name = 'benchmark'

    required_keys = [
        'hostname',
        'port',
        'graphite_port',
        'graphite_endpoint',
        'api_port'
    ]

    benchmarks = []

    def __init__(self, *args):
        if args:
            for arg in args:
                hookenv.log("benchmark: %s" % arg)
                self.benchmarks.append(arg)
            Benchmark(self.benchmarks)

        helpers.RelationContext.__init__(self, self.name)

    def is_ready(self):
        ready = super(BenchmarkRelation, self).is_ready()
        if ready and self.benchmarks:
            Benchmark(self.benchmarks)
        return ready


class HttpRelation(helpers.RelationContext):
    """
    Override HttpRelation to fix the required keys, and return the port
    provided by the relation, rather than the hard-coded port 80
    """
    name = 'website'
    interface = 'http'
    required_keys = ['hostname', 'port']

    def __init__(self, *args, **kwargs):
        helpers.RelationContext.__init__(self, *args, **kwargs)

    def provide_data(self):
        return {
            'host': hookenv.unit_get('hostname'),
            'port': hookenv.unit_get('port'),
        }


def manage():
    manager = ServiceManager([
        {
            'service': 'benchmark-siege',
            'ports': [],  # ports to after start
            'provided_data': [
                BenchmarkRelation('siege'),
            ],
            'required_data': [
                HttpRelation(),
                BenchmarkRelation(),
            ],
            'data_ready': [
                helpers.render_template(
                    source='siegerc',
                    target='%s/.siegerc' % hookenv.charm_dir()
                ),
                actions.log_start,
            ],
            'data_lost': [
            ],
        },
    ])
    manager.manage()
