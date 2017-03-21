AccumuloAdapter
===============

AccumuloAdapter is a Python module containing optimized data adapters for importing
data from an Accumulo database into NumPy arrays and Pandas DataFrame.

Build Requirements
------------------

Building AccumuloAdapter requires a number of dependencies. In addition to a C/C++ dev
environment, the following modules are needed, which can be installed via conda:

* NumPy
* Pandas
* Thrift 0.10.0 (C++ interface)
* pyaccumulo
* geodocker-accumulo (builds/configures Docker images for testing)

Building Conda Package
----------------------

Note: If building under Windows, make sure the following commands are issued
within the Visual Studio command prompt for version of Visual Studio that
matches the version of Python you're building for.  Python 2.6 and 2.7 needs
Visual Studio 2008, Python 3.3 and 3.4 needs Visual Studio 2010, and Python
3.5 needs Visual Studio 2015.

1. Build the pyaccumulo dependency using the following command (replace Python version number with desired version):
   ```
   conda build buildscripts/dependency-recipies/pyaccumulo --python 3.5
   ```

1. Build the geodocker-accumulo dependency using the following command (ensure that `docker-compose` is down beforehand):
   ```
   conda build buildscripts/dependency-recipies/geodocker-accumulo --python 3.5
   ```

   The geodocker-accumulo package simply serves as a way to pin the dependency
   version and download the proper docker images.

1. Build AccumuloAdapter using the following command:
   ```
   conda build buildscripts/condarecipe --python 3.5
   ```

1. AccumuloAdapter can now be installed from the built conda package:
   ```
   conda install accumuloadapter --use-local
   ```

Building By Hand
----------------

Note: If building under Windows, make sure the following commands are issued
within the Visual Studio command prompt for version of Visual Studio that
matches the version of Python you're building for.  Python 2.6 and 2.7 needs
Visual Studio 2008, Python 3.3 and 3.4 needs Visual Studio 2010, and Python
3.5 needs Visual Studio 2015.

For building AccumuloAdapter for local development/testing:

1. Install most of the above dependencies into environment called 'accumuloadapter':
   ```
   conda env create -f environment.yml
   ```

   Be sure to activate new accumuloadapter environment before proceeding.

1. Build the pyaccumulo and geodocker-accumulo packages as described
   above. Install into accumuloadapter environment using commands:
   ```
   conda install pyaccumulo --use-local
   conda install geodocker-accumulo --use-local
   ```

1. Build AccumuloAdapter using Cython/distutils:
   ```
   python setup.py build_ext --inplace
   ```

Testing
-------

Below are instructions for setting up an Accumulo test environment (with
database and proxy) on a Unix-based OS:

1. Download `docker-compose` v1.8.0, along with the `docker-compose.yml` config
   from [geodocker-accumulo](https://github.com/geodocker/geodocker-accumulo):

    ```
    curl -L https://github.com/docker/compose/releases/download/1.8.0/docker-compose-`uname -s`-`uname -m` -o docker-compose
    chmod +x docker-compose
    curl -sLO https://raw.githubusercontent.com/geodocker/geodocker-accumulo/a87da6c329a52f4dd8b3e1b8f52f6536b4b1265b/docker-compose.yml
    ```

1. `docker-compose up` starts the necessary components (along with Accumulo),
   and an additional `docker-compose run` brings up the proxy server listening
   on port 42424:

    ```
    ./docker-compose up -d
    ./docker-compose run --rm --publish 42424:42424 accumulo-master bash -c "set -e && \
        source /sbin/accumulo-lib.sh && \
        wait_until_accumulo_is_available accumulo zookeeper && \
        sed -i 's/localhost/zookeeper/;s/instance=test/instance=accumulo/' ./proxy/proxy.properties && \
        accumulo proxy -p ./proxy/proxy.properties"
    ```

    `./docker-compose down` can be used later on to stop/remove the containers.

1. Once the proxy server is running (last line should say something like "Proxy
   server running..."), the database should be prepped for test data and loaded:

    ```
    ./accumuloadapter/tests/setup_accumulo_data.py
    ```

1. Tests can be run by calling the accumuloadapter module's test function:

    ```python
    python -Wignore -c 'import accumuloadapter; accumuloadapter.test()'
    ```

Related projects
----------------

- TextAdapter (CSV, JSON, etc): https://github.com/ContinuumIO/TextAdapter
- DBAdapter (SQL derivatives): https://github.com/ContinuumIO/DBAdapter
- PostgresAdapter (PostgreSQL): https://github.com/ContinuumIO/PostgresAdapter
- AccumuloAdapter (Apache Accumulo): https://github.com/ContinuumIO/AccumuloAdapter
- MongoAdapter (MongoDB): https://github.com/ContinuumIO/MongoAdapter
