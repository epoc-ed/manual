.. _hdf5-metadata:

HDF5 metadata layout
====================

Overview
--------

Diffraction data are written on the server by **Jungfraujoch** (``jfjoch_writer``), producing NeXus/NXmx-style
HDF5 files. After acquisition, the Jungfrau GUI (JFGui) optionally *post-processes* the written HDF5 and
**adds/updates electron-diffraction/TEM-specific metadata** (beam fit, TEM state, stage motion, apertures, etc.).

This page documents:

1) The **baseline file structure** produced by Jungfraujoch (master + data files).
2) The **extra/overwritten fields** written by the JFGui (this project).
3) Conventions (units, datatypes, and where values come from).

References
~~~~~~~~~~

* Jungfraujoch writer: see ``JFJOCH_WRITER`` documentation (upstream).
* NeXus NXmx application definition (schema reference).


Files produced by Jungfraujoch
------------------------------

Jungfraujoch writes a **master file** (high-level metadata + links) and one or more **data files**
(image stacks and per-image values). Two master-file styles exist upstream (legacy vs VDS),
but from the GUI perspective the important point is that *data live in data files* while the master
file holds *links and experiment description*.

Data-file datasets and master-file mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Upstream convention:

* The data file contains per-image datasets under ``/entry/detector``.
* These datasets are mapped/linked into the master file under
  ``/entry/instrument/detector/detectorSpecific``.

A (non-exhaustive) view of data-file content is shown here for orientation (see ``JFJOCH_WRITER`` docs for the full list):

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Data-file path
     - Meaning (summary)
   * - ``/entry/data/data``
     - Raw image data (stack)
   * - ``/entry/detector/timestamp``
     - Per-image timestamps
   * - ``/entry/detector/exptime``
     - Per-image exposure time
   * - ``/entry/detector/number``
     - Per-image index (may differ if rejection is used)
   * - ``/entry/detector/storage_cell_image``
     - Storage cell number (optional)
   * - ``/entry/detector/packets_expected``
     - Expected UDP packet count (optional)
   * - ``/entry/detector/packets_received``
     - Received UDP packet count (optional)
   * - ``/entry/detector/data_collection_efficiency_image``
     - Received/expected ratio (optional)
   * - ``/entry/MX/*``
     - Spot finding / indexing auxiliaries (optional)
   * - ``/entry/roi/{roi_name}/*``
     - ROI statistics (optional)
   * - ``/entry/xfel/*``
     - XFEL-specific tags (optional)

.. note::
   The master file may additionally contain user-provided metadata under ``/entry/user`` depending on the
   acquisition configuration (see ``JFJOCH_WRITER`` docs).


JFGui metadata injection
--------------------------

The JFGui post-processes the master HDF5 file (or a chosen target HDF5 file) and
**creates or overwrites** datasets using the helper:

*If the dataset exists, it is deleted and recreated.*

This guarantees the GUI’s values win, but it also means:
existing attributes, chunking/compression, and original dtypes are not preserved.

The injected metadata are grouped below by subsystem.


1) Detector group
~~~~~~~~~~~~~~~~~

Paths under ``/entry/instrument/detector``:

.. list-table::
   :header-rows: 1
   :widths: 52 14 14 20

   * - Path
     - Type
     - Unit
     - Source / meaning
   * - ``/entry/instrument/detector/detector_name``
     - string
     - -
     - Human-readable detector identifier (site-specific)
   * - ``/entry/instrument/detector/beam_center_x``
     - int
     - pixel
     - Beam center X from beam fitting (JFGui)
   * - ``/entry/instrument/detector/beam_center_y``
     - int
     - pixel
     - Beam center Y from beam fitting (JFGui)
   * - ``/entry/instrument/detector/detector_distance``
     - uint64
     - mm 
     - Calibrated sample-to-detector distance from LUT (see note).
   * - ``/entry/instrument/detector/framerate``
     - uint64
     - Hz
     - Detector frame rate (fixed for JUNGFRAU here)
   * - ``/entry/instrument/detector/count_threshold_in_keV``
     - uint64
     - keV
     - JUNGFRAU threshold used during acquisition

Paths under ``/entry/instrument/detector/detectorSpecific``:

.. list-table::
   :header-rows: 1
   :widths: 52 14 14 20

   * - Path
     - Type
     - Unit
     - Source / meaning
   * - ``/entry/instrument/detector/detectorSpecific/element``
     - string
     - -
     - Sensor material label (e.g. ``Si``)
   * - ``/entry/instrument/detector/detectorSpecific/software_version_gui``
     - string
     - -
     - JFGui version tag (``JF_GUI/<tag>``)
   * - ``/entry/instrument/detector/detectorSpecific/gui_commit_hash``
     - string
     - -
     - Git commit hash of the GUI build


2) Source group
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 52 14 14 20

   * - Path
     - Type
     - Unit
     - Source / meaning
   * - ``/entry/source/probe``
     - string
     - -
     - Set to ``electron`` (ED)

.. note::
   NeXus/NXmx is historically rooted in X-ray crystallography, but electron-diffraction pipelines
   commonly set ``probe=electron`` when writing NXmx-like files.


3) Optics (TEM state + beam characterization)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These are written under ``/entry/instrument/optics``:

.. list-table::
   :header-rows: 1
   :widths: 52 14 14 20

   * - Path
     - Type
     - Unit
     - Source / meaning
   * - ``.../info_acquisition_date_time``
     - string
     - -
     - Timestamp of GUI metadata update
   * - ``.../microscope_name``
     - string
     - -
     - TEM model string
   * - ``.../accelerationVoltage``
     - float
     - kV
     - HT value (fallback to 200 kV on read error)
   * - ``.../accelerationVoltage_readout``
     - uint16
     - -
     - HT readout status (1=valid, 0=invalid)
   * - ``.../wavelength``
     - float
     - Å
     - Computed from acceleration voltage (relativistic electron wavelength)
   * - ``.../magnification``
     - uint16
     - -
     - TEM Magnification value readback (Imaging mode)
   * - ``.../distance_nominal``
     - uint16
     - -
     - TEM Magnification value readback (Diffraction mode)
   * - ``.../end_tilt_angle``
     - float
     - deg
     - Final TX tilt angle (stage readback)
   * - ``.../spot_size``
     - uint16
     - -
     - Spot size index (+1 stored). Range is 1-8
   * - ``.../alpha_angle``
     - uint16
     - -
     - Alpha index (+1 stored). Range is 1-9

Apertures:

.. list-table::
   :header-rows: 1
   :widths: 52 14 14 20

   * - Path
     - Type
     - Unit
     - Source / meaning
   * - ``.../CL_ID``
     - uint16
     - (index)
     - Condenser aperture hole number (0=open, 1–4=hole index).
   * - ``.../CL_size``
     - string
     - µm
     - Condenser aperture diameter from LUT mapping (CL_ID → size in µm).
   * - ``.../CL_position_x``
     - uint16
     - (device counts)
     - Condenser aperture centering X 
   * - ``.../CL_position_y``
     - uint16
     - (device counts)
     - Condenser aperture centering Y 
   * - ``.../SA_ID``
     - uint16
     - (index)
     - Selected-area aperture hole number (0=open, 1–4=hole index).
   * - ``.../SA_size``
     - string
     - µm
     - Selected-area (SA) aperture size label
   * - ``.../SA_position_x``
     - uint16
     - (device counts)
     - Selected-area (SA) aperture centering X
   * - ``.../SA_position_y``
     - uint16
     - (device counts)
     - Selected-area (SA) aperture centering Y
    
.. note::
    Aperture positions are reported in microscope controller coordinates (“device counts”).
    In JEOL TEMExt-style interfaces these are typically 12-bit values (0–4095).


Lens/deflector state (raw readbacks):

.. list-table::
   :header-rows: 1
   :widths: 52 14 14 20

   * - Path
     - Type
     - Unit
     - Source / meaning
   * - ``.../brightness``
     - uint32
     - (device counts)
     - Raw value of CL3 lens setting (0–65535)
   * - ``.../diff_focus``
     - uint32
     - (device counts)
     - Raw value of IL1 lens setting (0–65535)
   * - ``.../il_stigm_x``
     - uint32
     - (device counts)
     - Raw value of X component of Intermediate Stigmator (IL Stig) deflector (0–65535)
   * - ``.../il_stigm_y``
     - uint32
     - (device counts)
     - Raw value of Y component of IL Stig (0–65535)
   * - ``.../pl_align_x``
     - uint32
     - (device counts)
     - Raw value of X component of the Projector Shift (PLA) deflector (0–65535)
   * - ``.../pl_align_y``
     - uint32
     - (device counts)
     - Raw value of Y component of the PLA (0–65535)

Beam fit / illumination (GUI-derived):

.. list-table::
   :header-rows: 1
   :widths: 52 14 14 20

   * - Path
     - Type
     - Unit
     - Source / meaning
   * - ``.../optical_axis_center_x``
     - float
     - pixel
     - Optical axis center X on detector (from LUT/config).
   * - ``.../optical_axis_center_y``
     - float
     - pixel
     - Optical axis center Y on detector (from LUT/config).
   * - ``.../beam_width_sigmax``
     - float
     - pixel
     - Beam width sigma X from beam fit
   * - ``.../beam_width_sigmay``
     - float
     - pixel
     - Beam width sigma Y from beam fit
   * - ``.../beam_ellipse_angle``
     - float
     - deg
     - Beam ellipse angle from fit
   * - ``.../beam_illumination_pa_per_cm2_detector``
     - float
     - pA/cm²
     - Estimated illumination at detector plane
   * - ``.../beam_illumination_e_per_A2_sample``
     - float
     - e⁻/Å²
     - Dose estimate at sample plane


4) Stage (position + rotation during collection)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Written under ``/entry/instrument/stage``.

.. list-table::
   :header-rows: 1
   :widths: 52 14 14 20

   * - Path
     - Type
     - Unit
     - Source / meaning
   * - ``.../stage_x``
     - float
     - µm
     - Stage X (converted from TEM readback)
   * - ``.../stage_y``
     - float
     - µm
     - Stage Y (converted from TEM readback)
   * - ``.../stage_z``
     - float
     - µm
     - Stage Z (converted from TEM readback)
   * - ``.../stage_xyz_unit``
     - string
     - -
     - ``µm``
   * - ``.../stage_tx_speed_ID``
     - float
     - (index)
     - Speed selector index from TEM
   * - ``.../velocity_data_collection``
     - float
     - deg/s
     - Nominal rotation speed from lookup table
   * - ``.../stage_tx_axis``
     - float[3]
     - (vector)
     - Rotation axis unit vector (XDS convention) from LUT (ht_voltage and magnification regime).

If rotation angle samples were recorded (``rotations_angles`` not ``None``),
additional datasets are stored:

.. list-table::
   :header-rows: 1
   :widths: 52 14 14 20

   * - Path
     - Type
     - Unit
     - Source / meaning
   * - ``.../stage_tx_start``
     - float
     - deg
     - Start angle from recorded samples
   * - ``.../stage_tx_end``
     - float
     - deg
     - End angle from recorded samples
   * - ``.../stage_tx_speed_measured``
     - float
     - deg/s
     - Mean measured angular velocity from samples
   * - ``.../stage_tx_speed_measured_std``
     - float
     - deg/s
     - Std dev of measured angular velocity
   * - ``.../stage_tx_speed_unit``
     - string
     - -
     - ``deg/s``
   * - ``.../stage_tx_record``
     - array
     - (time,deg)
     - Raw record (as stored by GUI)


5) CIF convenience block (downstream crystallography tooling)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Written under ``/entry/cif`` as simple text fields to help downstream export.

.. list-table::
   :header-rows: 1
   :widths: 52 14 14 20

   * - Path
     - Type
     - Unit
     - Source / meaning
   * - ``/entry/cif/_diffrn_ambient_temperature``
     - string
     - K
     - Fixed-format CIF temperature formatted as text
   * - ``/entry/cif/_diffrn_radiation_wavelength``
     - string
     - Å
     - Wavelength formatted as text
   * - ``/entry/cif/_diffrn_radiation_probe``
     - string
     - -
     - ``electron``
   * - ``/entry/cif/_diffrn_radiation_type``
     - string
     - -
     - CIF label (monochromatic beam)
   * - ``/entry/cif/_diffrn_source``
     - string
     - -
     - TEM source
   * - ``/entry/cif/_diffrn_source_type``
     - string
     - -
     - TEM model (JEOL JEM2100Plus)
   * - ``/entry/cif/_diffrn_source_voltage``
     - string
     - kV
     - HT formatted as text
   * - ``/entry/cif/_diffrn_measurement_device_type``
     - string
     - -
     - Holder / goniometer (e.g. single axis tomography holder)
   * - ``/entry/cif/_diffrn_detector``
     - string
     - -
     - Detector class (e.g. hybrid pixel area detector)
   * - ``/entry/cif/_diffrn_detector_type``
     - string
     - -
     - Detector model (e.g. JUNGFRAU)
   * - ``/entry/cif/_diffrn_detector_area_resol_mean``
     - string
     - 1/mm
     - Convenience value, computed as ``1/pixel_size_mm``


Notes
---------------------

LUT-derived calibration values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some metadata are not direct TEM readbacks; they are **calibrated** using lookup tables stored in
``jfgui2_config.json`` (e.g. detector distance, aperture sizes, rotation axis, optical-axis center).

* ``detector_distance`` is interpolated from LUT points as a function of DIFF nominal and HT.
* ``CL_size`` / ``SA_size`` map aperture IDs to diameters in µm.
* ``stage_tx_axis`` provides an XDS-style rotation-axis unit vector keyed by HT (and magnification regime).
* ``optical_axis_center_{x,y}`` are detector pixel coordinates defined for the current setup.


Overwrite semantics
~~~~~~~~~~~~~~~~~~~

The JFGui uses "delete then recreate" for each dataset. This is simple and deterministic,
but it also discards:

* existing dataset attributes,
* chunking/compression,
* original dtype choices.


External schema references
--------------------------

The upstream file layout targets **NeXus NXmx** conventions (master/data and linking).
See:

* NeXus NXmx application definition (schema reference)
* Jungfraujoch writer docs (implementation reference)

.. rubric:: Links

* `JFJOCH_WRITER`_
* `NXmx`_
* `NXmx_xml`_

.. _JFJOCH_WRITER: https://jungfraujoch.readthedocs.io/en/latest/JFJOCH_WRITER.html
.. _NXmx: https://manual.nexusformat.org/classes/applications/NXmx.html
.. _NXmx_xml: https://github.com/nexusformat/definitions/blob/main/applications/NXmx.nxdl.xml
