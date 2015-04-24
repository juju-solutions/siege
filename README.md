# Benchmark-siege

Requires Juju 1.23 or later

# Deploy

```
juju bootstrap
juju deploy mysql
juju deploy mediawiki
juju deploy siege
juju add-relation mysql:db mediawiki:db
juju add-relation siege:website mediawiki:website
```

# List actions

```
$ juju action defined siege
siege: Standard siege benchmark.
```

# Run an action

Choose an action to run, like `siege`

```
$ juju action do siege/0 siege
Action queued with id: 097d714d-455e-47d6-8cc9-3eef5f9d5cad
```

# Run siege with custom parameters
```
$ juju action do siege/0 siege time=30s concurrency=30
```

# Check on actions

Make sure it's completed

```
$ juju action status 097d714d-455e-47d6-8cc9-3eef5f9d5cad
id: 097d714d-455e-47d6-8cc9-3eef5f9d5cad
status: completed
```

# Get results

```
$ juju action fetch 097d714d-455e-47d6-8cc9-3eef5f9d5cad
results:
    meta:
        start: 2015-01-27T16:52:05Z
        stop: 2015-01-27T16:52:20Z
    results:
        concurrent:
            units: ""
            value: "24.64"
        elapsed:
            units: secs
            value: "14.69"
        failed:
            units: ""
            value: "0"
        okay:
            units: ""
            value: "5216"
        response-time:
            units: secs
            value: "0.07"
        throughput:
            units: MB/sec
            value: "0.20"
        timestamp:
            units: ""
            value: 2015-01-2716:52:20
        transactions:
            units: hits
            value: "5216"
        transfer-rate:
            units: trans/sec
            value: "355.07"
        transfered:
            units: MB
            value: "3"
        status: completed
```
