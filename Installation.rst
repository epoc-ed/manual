Installation
------------

Below is a brief "How-To" guide that summarizes the steps for building the JF_GUI as a conda package from a local recipe.


**A. Create environment for the GUI**
"""""""""""""""""""""""""""""""""""""

**1. Clone the repository**

Clone the git repository on your local machine:

.. code-block:: console

    $ git clone https://github.com/epoc-ed/GUI.git

**2. Create a New Conda Environment**

If you don't have conda installed, install Miniforge (recommended lightweight distribution):

.. code-block:: console

   $ wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
   $ bash Miniforge3-Linux-x86_64.sh
   # Follow the prompts, then restart your terminal or run: source ~/.bashrc

Open your terminal (or Anaconda Prompt on Windows) and run:

.. code-block:: console

    $ conda config --show channels

    # remove `default` only if not usable (for e.g. blocked at PSI)
    $ conda config --remove channels defaults

    # Add required channels
    $ conda config --add channels conda-forge
    $ conda config --add channels epoc-project

    $ conda create --name jf_gui python=3.10 pyyaml epoc simple_tem

This creates the environment and installs Python 3.10 along with the required 
dependencies (``pyyaml``, ``epoc``, and ``simple_tem``) in a single step.

**3. Activate the Environment**

Now activate your new environment:

.. code-block:: console

    $ conda activate jf_gui

**4.Install Packages Using pip**

With your environment active, install all packages from your ``requirements.txt`` by running:

.. code-block:: console

    $ cd GUI/jungfrau_gui
    $ pip install -r requirements.txt # pip installed

The environment is now ready with all necessary dependencies for building and 
running the GUI package.

**B. Install the software as a conda package**
""""""""""""""""""""""""""""""""""""""""""""""

At this point, you need to have completed steps in the previous section.

**1. Make sure your project is well structured**

The root directory should include the following files:

- A ``setup.py`` file at the root directory.

- A ``MANIFEST.in`` if needed (to include additional files).

- A ``conda-recepie/`` folder containing the ``meta.yaml`` file.

For example::

    my_project/
    ├─ jungfrau_gui
    ├─ ............
    ├─ setup.py
    ├─ MANIFEST.in
    └─ conda-recepie/
        └─ meta.yaml

**2. Build the Package with ``conda-build``**

From the project's root directory (/path/to/GUI):

.. code-block:: console

    $ conda install conda-build  # if not already installed
    $ conda build conda-recepie

This will produce a ``.conda`` (or ``.tar.bz2``) file in your ``conda-bld/<platform>`` directory (often ``conda-bld/noarch`` for noarch packages).

**Locating the built package:**

The build output will show the package location near the end, typically:

.. code-block:: bash

   anaconda upload \
       ~/.conda/envs/jf_gui/conda-bld/noarch/jungfrau_gui-<version>-py_0.conda

**3. Installing the Newly Built Package**

Normally, you can install the package from the local build by:

.. code-block:: console

    $ conda install --use-local jungfrau_gui

Sometimes, you may encounter a situation where the newly built package is not found even though you know it’s in ``conda-bld/``.
In that case, you can install the package directly from the ``.conda`` (or ``.tar.bz2``) file:

.. code-block:: console

    $ conda install <path/to/built/package>

    # for example:
    $ conda install /opt/miniforge/miniforge3/envs/jf_gui/conda-bld/noarch/jungfrau_gui-2025.04.14-py_0.conda

.. important::
   **Before launching the GUI**, you must initialize the Redis database with the 
   required configuration parameters. The GUI will fail to start if these fields 
   are not properly set. Follow the Redis configuration steps below to complete 
   the installation.

**C. Initial Redis Configuration**
"""""""""""""""""""""""""""""""""""

This section describes how to set up the Redis database server that stores 
configuration parameters for the EPOC system. **The GUI requires this database 
to be initialized before it can launch.**

Prerequisites
~~~~~~~~~~~~~

- Redis server installed on the server machine
- ``epoc`` and ``pyyaml`` Python packages installed in your conda environment on both server and client
- Network connectivity between server and client machines


.. note::
   The ``epoc`` package provides the ``ConfigurationClient`` class used to interact 
   with the Redis database. For more details on the EPOC utilities, see the 
   `epoc-utils repository <https://github.com/epoc-ed/epoc-utils>`_.
   
Installation and Setup
~~~~~~~~~~~~~~~~~~~~~~

**1. Install Redis on Server**

On the server machine (RHEL/CentOS):

.. code-block:: console

   $ sudo yum install epel-release
   $ sudo yum install redis
   $ redis-server --version

**2. Configure Environment Variables**

**On the server machine:**

Add to ``~/.bashrc``:

.. code-block:: bash

   export EPOC_REDIS_HOST=localhost
   export EPOC_REDIS_TOKEN=<your_password>
   export EPOC_REDIS_PORT=<port_number>

Example:

.. code-block:: bash

   export EPOC_REDIS_HOST=localhost
   export EPOC_REDIS_TOKEN=mySecurePassword123
   export EPOC_REDIS_PORT=5454

**On the client machine:**

Add to ``~/.bashrc``:

.. code-block:: bash

   export EPOC_REDIS_HOST=<server_hostname>
   export EPOC_REDIS_TOKEN=<your_password>
   export EPOC_REDIS_PORT=<port_number>

Example:

.. code-block:: bash

   export EPOC_REDIS_HOST=jungfrau-server
   export EPOC_REDIS_TOKEN=mySecurePassword123
   export EPOC_REDIS_PORT=5454

Apply the changes:

.. code-block:: console

   $ source ~/.bashrc

.. note::
   **Setting up hostname resolution:** If the server hostname (or other machine 
   hostnames like the TEM control computer) are not automatically resolved on your 
   network, add them to ``/etc/hosts`` on the client machine:
   
   .. code-block:: console
   
      $ sudo nano /etc/hosts
   
   Add lines mapping each machine's IP address to its hostname:
   
   .. code-block:: text
   
      192.168.1.100    jungfrau-server
      192.168.1.150    temserver
   
   Replace the IP addresses with the actual IPs of each machine (find them by 
   running ``hostname -I`` on the respective machines). While you primarily need 
   the Redis server hostname defined now, you may also add other machine hostnames 
   (like the TEM control computer) at the same time for future use.

**3. Configure and Start Redis Server**

**Edit Redis configuration:**

.. code-block:: console

   $ sudo nano /etc/redis/redis.conf # sometimes located at /etc/redis.conf

Set the following parameters:

.. code-block:: text

   # Port configuration
   port <port_number>
   
   # Allow external connections
   bind 0.0.0.0
   
   # Set password for authentication
   requirepass <your_password>
   
   # Run as daemon
   daemonize yes
   
   # Disable protected mode (we have password authentication)
   protected-mode no

Example:

.. code-block:: text

   # port 6379 (default)
   port 5454
   
   # bind 127.0.0.1 (default)
   bind 0.0.0.0

   requirepass mySecurePassword123
   daemonize yes
   protected-mode yes

**Open firewall port:**

.. code-block:: console

   $ sudo firewall-cmd --permanent --add-port=<port_number>/tcp
   $ sudo firewall-cmd --reload

Example:

.. code-block:: console

   $ sudo firewall-cmd --permanent --add-port=5454/tcp
   $ sudo firewall-cmd --reload

**Enable and start Redis service:**

.. code-block:: console

   $ sudo systemctl enable redis
   $ sudo systemctl start redis
   $ sudo systemctl status redis

The ``enable`` command ensures Redis starts automatically on system boot.

**Verify Redis is running:**

.. code-block:: console

   $ sudo netstat -tlnp | grep redis

You should see output like:

.. code-block:: text

   tcp  0  0  0.0.0.0:5454  0.0.0.0:*  LISTEN  12345/redis-server

This confirms Redis is listening on all interfaces (``0.0.0.0``) on the configured port.

**4. Initialize Redis Database**

Create a YAML configuration file with all required parameters:

**epoc-config.yaml:**

.. code-block:: yaml

   # EPOC Redis Configuration
   
   # Experiment metadata
   affiliation: "YourInstitution"
   PI_name: "DefaultPI"
   project_id: "ProjectID"
   experiment_class: "External"
   measurement_tag: "sample1"
   
   # Data directories
   base_data_dir: "/data/jungfrau"
   XDS_template: "/path/to/XDS.INP"
   cal_dir: "/path/to/calibration"
   
   # Detector settings (e.g. of 1 Megapixel JUNGFRAU)
   nrows: 1064
   ncols: 1030
   threshold: 5
   
   # Viewer settings
   viewer_interval: 20.0
   viewer_cmin: 0.0
   viewer_cmax: 12000.0
   
   # Network endpoints
   jfjoch_host: "http://jungfrau-server:5232"      # Replace by the HTTP address of the Jungfraujoch web GUI 
   receiver_endpoint: "tcp://jungfrau-server:5000" # look at the ZMQ stream endpoint in the Jungfraujoch Web GUI
   temserver: "temserver"                          # IP address of the TEM control machine (define in /etc/hosts) 
   
   # Acquisition settings
   rotation_speed_idx: 0
   file_id: 0
   
   # Display overlays (optional)
   overlays:
    - {'type': 'circle', 'xy': [526, 253], 'radius': 188, 'ec': 'r', 'fill': False, 'lw': 2}
    - {'type': 'circle', 'xy': [526, 253], 'radius': 5, 'ec': 'g', 'fill': False, 'lw': 2}
    - {'type': 'rectangle', 'xy': [574, 52], 'width': 60, 'height': 31, 'angle': 27.5, 'ec': 'y', 'fill': False}
    - {'type': 'rectangle', 'xy': [0, 0], 'width': 1000, 'height': 1, 'angle': 19.8, 'ec': 'r', 'fill': False}
   
   # Used affiliations list
   usedAffiliations: ["YourInstitution", "External"]

**Initialize the database (can be run from client or server):**

.. code-block:: python

   from pathlib import Path
   from epoc import ConfigurationClient, auth_token, redis_host
   
   # Connect to Redis
   cfg = ConfigurationClient(redis_host(), token=auth_token())
   
   # Load configuration from YAML (flush_db=True clears any existing data)
   cfg.from_yaml(Path('path/to/epoc-config.yaml'), flush_db=True)
   
   print("Redis database initialized successfully!")
   print(cfg)

.. note::
   This initialization can be performed from either the server or client machine. 
   The Redis server stores the configuration data, and any machine with proper 
   authentication can modify it.

**5. Verify Configuration**

**On the server machine, using redis-cli:**

.. code-block:: console

   $ redis-cli -h localhost -p <PORT> -a <PASSWORD>

Example:

.. code-block:: console

   $ redis-cli -h localhost -p 5454 -a mySecurePassword123

**Check database contents:**

.. code-block:: text

   127.0.0.1:5454> DBSIZE
   (integer) 21
   
   127.0.0.1:5454> KEYS *
   1) "affiliation"
   2) "PI_name"
   3) "project_id"
   4) "base_data_dir"
   ... (more keys)
   
   127.0.0.1:5454> GET PI_name
   "DefaultPI"
   
   127.0.0.1:5454> GET base_data_dir
   "/data/jungfrau"
   
   127.0.0.1:5454> GET nrows
   "1064"
   
   127.0.0.1:5454> EXIT

**Alternatively, using Python:**

.. code-block:: python

   from pathlib import Path
   from epoc import ConfigurationClient, auth_token, redis_host
   
   cfg = ConfigurationClient(redis_host(), token=auth_token())
   
   # Print configuration summary
   print(cfg)
   
   # Check specific values
   print(f"PI_name: {cfg.PI_name}")
   print(f"project_id: {cfg.project_id}")
   print(f"base_data_dir: {cfg.base_data_dir}")
   
   # Export current configuration to YAML for inspection
   cfg.to_yaml(Path('current_config.yaml'))

Then inspect the exported file:

.. code-block:: console

   $ cat current_config.yaml

Architecture Notes
~~~~~~~~~~~~~~~~~~

**Redis as a centralized configuration store:**

The Redis server runs on a single machine (the server) and stores all configuration 
parameters in memory. Client machines connect to this server over the network to 
read and write configuration values. This ensures all components of the EPOC system 
share the same configuration state.

**Network communication:**

- Client applications use the Redis protocol over TCP/IP to communicate with the server
- The ``bind 0.0.0.0`` setting allows Redis to accept connections from any network interface
- Authentication via password (``requirepass``) prevents unauthorized access
- Firewall rules control which machines can reach the Redis port

**Data persistence:**

Redis periodically saves its in-memory data to disk (``/var/lib/redis/dump.rdb``). 
After a system reboot, Redis automatically reloads this data, preserving your 
configuration. The ``systemctl enable redis`` command ensures Redis starts 
automatically on boot.

Maintenance Commands
~~~~~~~~~~~~~~~~~~~~

**Restart Redis service:**

.. code-block:: console

   $ sudo systemctl restart redis

**Stop Redis service:**

.. code-block:: console

   $ sudo systemctl stop redis

**Prevents auto-start on boot:**

.. code-block:: console

   $ sudo systemctl disable redis

**View Redis logs:**

.. code-block:: console

   $ sudo journalctl -u redis -f

**Backup configuration:**

.. code-block:: python

   from pathlib import Path
   from epoc import ConfigurationClient, auth_token, redis_host
   
   cfg = ConfigurationClient(redis_host(), token=auth_token())
   cfg.to_yaml(Path('backup_config.yaml'))

**Restore configuration:**

.. code-block:: python

   cfg.from_yaml(Path('backup_config.yaml'), flush_db=True)

**Reset database (clear all data):**

.. code-block:: console

   $ redis-cli -h localhost -p <PORT> -a <PASSWORD> FLUSHDB

Or in Python:

.. code-block:: python

   cfg.client.flushdb()