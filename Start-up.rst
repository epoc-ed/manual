====================
Start up 
====================

.. note::
    This procedure documents the full start-up process. Often it's enough to:

    - Start the relay server on the TEM-PC.
    - Open the GUI on the CameraPC.

TEM-PC - relay server
"""""""""""""""""""""""

The relay server on the Windows PC that controls the TEM (TEM-PC) server listens
for commands on a zmq socket and runs them in PyJEM before returning the result.
Enables control of the microscope from other computers.

This should be done before starting the GUI.

#. Check if ``server_tem.py`` is running in the Miniconda PowerShell Prompt on TEMPC. 

    .. note::
        
        If the script is running, you can jump to the section **CameraPC (hodgkin)**.

        Otherwise, please follow the instructions in steps (2) and (3) below.

#. Navigate to: **C:\\Users\\JEM User\\Documents\\DataExchange\\bat**

#. Double-click on the **run_tem_server.bat** file

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
    
    As of 2025-01-24, the manual start-up of Jungfraujoch's broker and writer is no longer necessary as they are started
    automatically at boot time of noether.

    Keep an eye on this section since the procedure will change as we improve the Jungfraujoch integration.
    Processes will be automated using systemctl services.

    For now leave the terminals open. 

1. Check that broker and writer are running on noether:

.. code-block:: bash
    
    $ ssh noether
    $ ps -elf | grep writer
    jem2100+    2024       1  1 Jan22 ?        00:47:58 /opt/jfjoch/bin/jfjoch_writer -R /data/epoc/storage/jem2100plus tcp://localhost:5500
    $ ps -elf | grep broker 
    4 S root        3569       1  7  80   0 - 3155992 -    Jan22 ?        03:02:46 /opt/jfjoch/bin/jfjoch_broker /opt/config/broker_jf1M.json

2. Check that the metadata updater script is also running on noether.

.. code-block:: bash
        
    $ ssh noether # only if opened a new terminal on hodgkin
    $ ps -elf | grep metadata_update_server
    jem2100+    4975       1  1 Feb18 ?        10:09:18 /data/epoc/storage/jem2100plus/metadata_update_server.py

⚠️ If the metadata updater script is not active, run the following commands:

.. code-block:: bash

    $ python -i /data/epoc/storage/jem2100plus/metadata_update_server.py

.. note::

    If the metadata-updater script seems to be stuck in an error-loop, please recover it as follows;
    Stop the process with ```ctrl + z```, kill it with ```kill %1```, restore the status to foreground with ```fg```, then restart the script.

3. Open a web browser and navigate to the Jungfraujoch GUI at `http://noether:5232/`.

4. Initialize the detector and backend by pressing the **INITIALIZE** button in the web interface.

5. Launch the GUI using **one of** the following options:

   **5.a. Stable version for users (stable environment on hodgkin)**

   Run the following commands:

   .. code-block:: bash

       cd ~
       mamba activate stable
       jungfrau_gui

   **5.b. Developer version for users/developers (available also under stable python environment on hodgkin)**

   Run the following commands:

   .. code-block:: bash

       mamba activate stable
       cd ~/developer/epoc-utils
       git switch developer
       cd ~/developer/GUI
       git switch developer
       python launch_gui.py [-s tcp://noether:5501] [-f] [-e]
       :
       :
       cd ~/developer/epoc-utils
       git switch main

⚠️ Please reactivate the main branch of epoc-utils at the end of the session:

.. code-block:: bash

    cd ~/developer/epoc-utils
    git switch main
       