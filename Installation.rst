Installation
------------

Below is a brief "How-To" guide that summarizes the steps for building a conda package from a local recipe.

Install the GUI as a conda package
""""""""""""""""""""""""""""""""""

**1. Clone the repository**

.. code-block:: bash

    git clone git@github.com:epoc-ed/GUI.git

**2. Make sure your project is well structured**

The root directory should include the following files:

- A ``setup.py`` file at the root directory.

- A ``MANIFEST.in`` if needed (to include additional files).

- A ``conda-recepie/`` folder containing the ``meta.yaml`` file.

For example::

    my_project/
    ├─ setup.py
    ├─ MANIFEST.in
    └─ conda-recepie/
        └─ meta.yaml

**3. Build the Package with ``conda-build``**

From the project's root directory:

.. code-block:: bash

    conda install conda-build  # if not already installed
    conda build conda-recepie

This will produce a ``.conda`` (or ``.tar.bz2``) file in your ``conda-bld/<platform>`` directory (often ``conda-bld/noarch`` for noarch packages).

**4. Installing the Newly Built Package**

Normally, you can install the package from the local build by:

.. code-block:: bash

    conda install --use-local jungfrau_gui

Sometimes, you may encounter a situation where the newly built package is not found even though you know it’s in ``conda-bld/``.
In that case, you can install the package directly from the ``.conda`` (or ``.tar.bz2``) file:

.. code-block:: bash

    conda install <path/to/built/package>
    # for example:
    conda install /opt/miniforge/miniforge3/envs/stable/conda-bld/noarch/jungfrau_gui-2025.04.14-py_0.conda
