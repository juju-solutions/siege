#!/usr/bin/python

from charmhelpers.core.services.base import ServiceManager
from charmhelpers.core.services import helpers

import actions
from charmhelpers.core import hookenv


class Benchmark():
    """
    Helper class for the `benchmark` interface.

    :param list actions: Define the actions that are also benchmarks

    From inside the benchmark-relation-changed hook, you would
    Benchmark(['memory', 'cpu', 'disk', 'smoke', 'custom'])

    """

    required_keys = [
        'hostname',
        'port',
        'graphite_port',
        'graphite_endpoint',
        'api_port'
    ]

    def __init__(self, benchmarks=None):
        if benchmarks is not None:
            for rid in sorted(hookenv.relation_ids('benchmark')):
                hookenv.relation_set(relation_id=rid, relation_settings={
                    'benchmarks': ",".join(benchmarks)
                })

        # Check the relation data
        config = {}
        for key in self.required_keys:
            val = hookenv.relation_get(key)
            if val is not None:
                config[key] = val
            else:
                # We don't have all of the required keys
                config = {}
                break

        if len(config):
            f = open('/etc/benchmark.conf', 'w')
            for key, val in config.iteritems():
                f.write("%s=%s\n" % (key, val))
            f.close()


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

    def __init__(self, benchmarks=None):
        self.benchmarks = benchmarks
        super(BenchmarkRelation, self).__init__(self.name, None)

    def is_ready(self):
        ready = super(BenchmarkRelation, self).is_ready()
        if ready and self.benchmarks:
            Benchmark(self.benchmarks)

        return ready


class HttpRelation(helpers.HttpRelation):
    """
    Override HttpRelation to fix the required keys, and return the port
    provided by the relation, rather than the hard-coded port 80
    """
    required_keys = ['hostname', 'port']

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
                # context managers for provided relations
                # e.g.: helpers.HttpRelation()
                # BenchmarkRelation(['list', 'of', 'actions1']),
            ],
            'required_data': [
                # data (contexts) required to start the service
                # e.g.: helpers.RequiredConfig('domain', 'auth_key'),
                #       helpers.MysqlRelation(),
                # helpers.RequiredConfig('hostname', 'port'),
                HttpRelation(),
                BenchmarkRelation(['siege']),
            ],
            'data_ready': [
                helpers.render_template(
                    source='siegerc',
                    target='%s/.siegerc' % hookenv.charm_dir()),
                actions.log_start,
            ],
            'data_lost': [
            ],
        },
    ])
    manager.manage()
