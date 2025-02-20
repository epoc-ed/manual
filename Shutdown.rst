====================
Shutdown 
====================

.. note::

    This procedure describes how to switch off the detector in case of service or a longer dark period. 
    After data taking if the detector will be used the same week it's enough to close the GUI. 

CameraPC (hodgkin)
"""""""""""""""""""""""

From the GUI Window, hit the ``Exit`` button at the bottom to close and clean all running threads before closing the application.

TEM-PC
""""""

1. Open another PowerShell console and kill the corresponding python process:
   
.. code-block:: bash

   $ Get-Process python
   $ kill [process-id]