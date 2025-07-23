.. _jungfraujoch:

Jungfraujoch
------------

Jungfraujoch is a FPGA based data backed developed by Filip Leonarski. It started as a project focused on MX at synchrotrons
but has evolved to general data backend.

- Source code: https://gitlab.psi.ch/jungfraujoch/nextgendcu
- Documentation: https://jungfraujoch.readthedocs.io/en/latest/

.. attention::

    Jungfraujoch will move to https://gitea.psi.ch in the future, since the PSI gitlab is being phased out.

Installation
""""""""""""

The Jungfraujoch FPGA card is mounted in noehter and the detector is directly connected using optical fibers.

.. TODO! expand on physical setup

The code is compiled locally on noehter ``/home/psi/nextgendcu`` and the binaries are stored in ``/opt/jfjoch``.


**Installation location:**

.. code-block:: bash


    #installation location
    /opt/jfjoch

    #Detector configuration
    /opt/etc/broker_jf1M.json

    #Web frontend 
    /opt/jfjoch_frontend

    #Detector calibration
    /opt/cal



Updating Jungfraujoch
=======================

.. attention::

    Always check the latest deployment documentation before updating JFJ. 
    https://jungfraujoch.readthedocs.io/en/latest/DEPLOYMENT.html


**Update the FPGA firmware**

#. Download the latest firmware from the Jungfraujoch repository.
#. Make sure the card is not un use by unloading the kernel module [TBC]:

   .. code-block:: bash

        sudo rmmod jfjoch

#. Flash the firmware to the FPGA card using xbflash.qspi
#. Server needs a hard reboot ``sudo ipmitool chassis power cycle``

**Update the code**

.. code-block:: bash

    # Update the Jungfraujoch code
    cd /home/psi/nextgendcu
    git pull

    # Compile the code
    make -j20

    # Install JFJ (will need sudo/root access to update the kernel module)
    make install 

**Copy the new frontend**

#. Download the frontend from the Jungfraujoch repository.
#. Copy the new frontend to the web server directory:

   .. code-block:: bash

        tar -xvf jfjoch_frontend.tar.gz -C /opt/jfjoch_frontend


JFJ hdf5 file content
=======================

.. code-block:: bash
    
    HDF5 "dark_long2_master.h5" {
    FILE_CONTENTS {
    group      /
    group      /entry
    group      /entry/data
    ext link   /entry/data/data_000001 -> dark_long2_data_000001.h5 /entry/data/data
    ext link   /entry/data/data_000002 -> dark_long2_data_000002.h5 /entry/data/data
    ext link   /entry/data/data_000003 -> dark_long2_data_000003.h5 /entry/data/data
    ext link   /entry/data/data_000004 -> dark_long2_data_000004.h5 /entry/data/data
    ext link   /entry/data/data_000005 -> dark_long2_data_000005.h5 /entry/data/data
    ext link   /entry/data/data_000006 -> dark_long2_data_000006.h5 /entry/data/data
    ext link   /entry/data/data_000007 -> dark_long2_data_000007.h5 /entry/data/data
    ext link   /entry/data/data_000008 -> dark_long2_data_000008.h5 /entry/data/data
    ext link   /entry/data/data_000009 -> dark_long2_data_000009.h5 /entry/data/data
    ext link   /entry/data/data_000010 -> dark_long2_data_000010.h5 /entry/data/data
    dataset    /entry/definition
    dataset    /entry/end_time
    dataset    /entry/end_time_estimated
    group      /entry/instrument
    group      /entry/instrument/beam
    dataset    /entry/instrument/beam/incident_wavelength
    group      /entry/instrument/detector
    dataset    /entry/instrument/detector/acquisition_type
    dataset    /entry/instrument/detector/beam_center_x
    dataset    /entry/instrument/detector/beam_center_y
    dataset    /entry/instrument/detector/bit_depth_image
    dataset    /entry/instrument/detector/bit_depth_readout
    group      /entry/instrument/detector/calibration
    dataset    /entry/instrument/detector/calibration/pedestal_g0
    dataset    /entry/instrument/detector/calibration/pedestal_g1
    dataset    /entry/instrument/detector/calibration/pedestal_g2
    dataset    /entry/instrument/detector/calibration/pedestal_rms_g0
    dataset    /entry/instrument/detector/calibration/pedestal_rms_g1
    dataset    /entry/instrument/detector/calibration/pedestal_rms_g2
    dataset    /entry/instrument/detector/count_time
    dataset    /entry/instrument/detector/countrate_correction_applied
    dataset    /entry/instrument/detector/description
    group      /entry/instrument/detector/detectorSpecific
    dataset    /entry/instrument/detector/detectorSpecific/data_collection_efficiency
    dataset    /entry/instrument/detector/detectorSpecific/data_reduction_factor_serialmx
    dataset    /entry/instrument/detector/detectorSpecific/gain_file_names
    dataset    /entry/instrument/detector/detectorSpecific/jfjoch_release
    dataset    /entry/instrument/detector/detectorSpecific/max_receiver_delay
    dataset    /entry/instrument/detector/detectorSpecific/nimages
    dataset    /entry/instrument/detector/detectorSpecific/nimages_collected
    dataset    /entry/instrument/detector/detectorSpecific/nimages_written
    dataset    /entry/instrument/detector/detectorSpecific/ntrigger
    dataset    /entry/instrument/detector/detectorSpecific/pixel_mask
    dataset    /entry/instrument/detector/detectorSpecific/software_git_commit
    dataset    /entry/instrument/detector/detectorSpecific/software_git_date
    dataset    /entry/instrument/detector/detectorSpecific/storage_cell_number
    dataset    /entry/instrument/detector/detectorSpecific/x_pixels_in_detector
    dataset    /entry/instrument/detector/detectorSpecific/y_pixels_in_detector
    dataset    /entry/instrument/detector/detector_distance
    dataset    /entry/instrument/detector/distance
    dataset    /entry/instrument/detector/error_value
    dataset    /entry/instrument/detector/flatfield_applied
    dataset    /entry/instrument/detector/frame_time
    group      /entry/instrument/detector/module
    dataset    /entry/instrument/detector/module/data_origin
    dataset    /entry/instrument/detector/module/data_size
    dataset    /entry/instrument/detector/module/fast_pixel_direction
    dataset    /entry/instrument/detector/module/module_offset
    dataset    /entry/instrument/detector/module/slow_pixel_direction
    dataset    /entry/instrument/detector/number_of_cycles
    dataset    /entry/instrument/detector/pixel_mask -> /entry/instrument/detector/detectorSpecific/pixel_mask
    dataset    /entry/instrument/detector/pixel_mask_applied
    dataset    /entry/instrument/detector/saturation_value
    dataset    /entry/instrument/detector/sensor_material
    dataset    /entry/instrument/detector/sensor_thickness
    group      /entry/instrument/detector/transformations
    dataset    /entry/instrument/detector/transformations/translation
    dataset    /entry/instrument/detector/x_pixel_size
    dataset    /entry/instrument/detector/y_pixel_size
    dataset    /entry/instrument/name
    group      /entry/result
    group      /entry/result/adu_histogram
    dataset    /entry/result/adu_histogram/bin_width
    dataset    /entry/result/adu_histogram/module0
    group      /entry/result/azimIntegration
    dataset    /entry/result/azimIntegration/bin_to_q
    dataset    /entry/result/azimIntegration/dataset
    group      /entry/sample
    dataset    /entry/sample/depends_on
    group      /entry/source
    dataset    /entry/source/name
    dataset    /entry/source/type
    dataset    /entry/start_time
    }
    }
