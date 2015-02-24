from charmhelpers.core import hookenv
from charmhelpers.core.services import helpers


def write_benchmark_config(service_name):
    if hookenv.in_relation_hook():
        hookenv.log('write_benchmark_config')

        hookenv.relation_set(actions='asdf')
        hostname = hookenv.relation_get('hostname')
        graphite_endpoint = hookenv.relation_get('graphite_endpoint')
        if hostname:
            print "[%s] %s" % (hostname, graphite_endpoint)
            # helpers.render_template(
            #     source='benchmark.conf',
            #     target='/etc/benchmark.conf'
            # )

        # hookenv.log('Service name: %s' % service_name)
        # if BenchmarkRelation[0].is_ready():
        #     host = BenchmarkRelation()[0]['hostname']
        #     port = BenchmarkRelation()[0]['port']
        #     hookenv.log('write_config(%s): %s:%d' % (service_name, host, port))


def log_start(service_name):
    hookenv.log('benchmark-siege starting')
