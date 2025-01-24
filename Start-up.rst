====================
Start up 
====================

.. note::
    This procedure documents the full start-up process. Often it's enough to:

    - Start the relay server on the TEM-PC.
    - Open the GUI on the CameraPC.

TEM-PC - relay server
"""""""""""""""""""""""

Start the relay server (tem-server.py). This server listens for commands on a zmq socket and runs them in PyJEM before returning the result.
Enables control of the microscope from other computers.

This should be done before starting the GUI.

#. Navigate to: **C:\\ProgramData\\EPOC**

#. Double-click on the .bat file

.. warning::
    
    In case of any issues with the .bat file, please follow the steps below for the manual start-up:

    1. Open a Miniconda PowerShell Prompt (Anaconda submenu) from the Windows Start Menu.

    .. note::

        The Quick Edit mode of the PowerShell prompt can interupt the script, disable it by:

        - Right-click on the title bar 
        - Select `Properties` from the dropdown menu.
        - In the `Options` tab, uncheck the box for `Quick Edit Mode`
        - Click `OK`.

    2. Navigate to: **C:\\ProgramData\\EPOC**

    .. code-block:: bash

        cd C:\\ProgramData\\EPOC

    3. Activate the environment by

    .. code-block:: bash

        conda activate vjem38

    4. Start the TEM server:

    .. code-block:: bash

        python server_tem.py

CameraPC (hodgkin)
"""""""""""""""""""""""

.. warning::
    
    Keep an eye on this section since the procedure will change as we improve the Jungfraujoch integration.
    Processes will be automated using systemctl services.

    For now leave the terminals open. 

1. Check that you are logged in as `jem2100user`.

2. Start the Jungfraujoch broker on noether:

.. code-block:: bash

    #The broker needs to run with root privileges to access the FPGA card.
    ssh psi@noether
    su - 
    ...


3. Start the Jungfraujoch writer on noether:
 
.. code-block:: bash

    #run as jem2100user?

4. Open a web browser and navigate to the Jungfraujoch GUI at `http://noether:5232/`.

5. Initialize the detector and backend by pressing the init button in the web interface.

6. Launch the GUI (stable)

.. code-block:: bash

    mamba activate stable
    jungfrau_gui [-t] [-s tcp://noether:5501] [-f]

7. Launch the GUI (dev)

.. code-block:: bash

    mamba activate dev
    cd ~/GUI/
    git branch --contains
    git switch no-reuss-client # Soon to be renamed "testing"
    python launch_gui.py [-t] [-s tcp://noether:5501] [-f]


