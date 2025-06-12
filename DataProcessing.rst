====================
Processing diffraction datasets
====================

.. note::

    This page summarizes the minimum workflow of processing the diffraction datasets collected the Jungfrau and the GUI.

**XDS**
"""""""""""""""""""""""

- The XDS.INP file automatically generated in the specified directory (default: under the same directory as that for the recorded HDF files) can be used for processing after the indexing.

**DIALS**
"""""""""""""""""""""""

``dxtbx.install_format -u FormatHDFJungfrau1MJFJVIE02_multipanel.py``
    Installation of the specific class file to read the HDF file with DIALS. This should be done if the format of HDF is updated.

    Then, run the process with each datasets:
.. code-block:: bash

    dials.import [prefix]_master.h5
    dials.find_spots imported.expt
    dials.index strong.refl imported.expt detector.fix=distance
    dials.refine indexed.expt indexed.refl scan_varying=true detector.fix=distance
    dials.integrate refined.expt refined.refl