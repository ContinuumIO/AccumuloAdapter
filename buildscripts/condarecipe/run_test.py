import subprocess
import accumuloadapter
import os
import time
import inspect
import atexit
import sys
import shlex
from accumuloadapter.tests import setup_accumulo_data



def dl_docker_compose(git_rev='a87da6c329a52f4dd8b3e1b8f52f6536b4b1265b'):
    """Download docker-compose script and a docker-compose.yml file from the
    appropriate repo.
    """
    subprocess.check_call('curl -L https://github.com/docker/compose/releases/download/1.8.0/docker-compose-`uname -s`-`uname -m` -o docker-compose', shell=True)
    subprocess.check_call('chmod +x docker-compose', shell=True)
    subprocess.check_call('curl -sLO https://raw.githubusercontent.com/geodocker/geodocker-accumulo/{}/docker-compose.yml'.format(git_rev), shell=True)


def start_accumulo(waitsecs=10):
    print('Starting Accumulo test env...')
    subprocess.check_call('./docker-compose up -d', shell=True)
    time.sleep(waitsecs)

    cmd = shlex.split('''./docker-compose run --rm --publish 42424:42424 accumulo-master \
        bash -c "set -e && \
            source /sbin/accumulo-lib.sh && \
            wait_until_accumulo_is_available accumulo zookeeper && \
            sed -i 's/localhost/zookeeper/;s/instance=test/instance=accumulo/' ./proxy/proxy.properties && \
            accumulo proxy -p ./proxy/proxy.properties"''')
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True)
    while True:
        output_line = proc.stdout.readline()
        print(output_line.rstrip())
        if proc.poll() is not None: # If the process exited
            raise Exception('Proxy server failed to start up properly.')
        if 'Proxy server started on' in output_line:
            break


def stop_accumulo(let_fail=False):
    try:
        print('Stopping Accumulo test env...')
        subprocess.check_call('docker ps -aq --filter="ancestor=quay.io/geodocker/accumulo" --filter="ancestor=quay.io/geodocker/zookeeper" --filter="ancestor=quay.io/geodocker/hdfs:0.1" | xargs docker rm -fv || true', shell=True)
        subprocess.check_call('./docker-compose down', shell=True)
    except subprocess.CalledProcessError:
        if not let_fail:
            raise


### Download docker-compose
dl_docker_compose()

### Restart Accumulo
stop_accumulo(let_fail=True)
start_accumulo(waitsecs=10)

### Run Accumulo tests
atexit.register(stop_accumulo) # Stop Accumulo when this script exits
print('Setting up the Accumulo test database...')
setup_accumulo_data.main()
print('Running tests...')
assert accumuloadapter.test()

# Print the version
print('accumuloadapter.__version__: %s' % accumuloadapter.__version__)

sys.exit(0)
