Installation
------------

Below is a brief "How-To" guide that summarizes the steps for building the JF_GUI as a conda package from a local recipe.


**A. Create environment for the GUI**
"""""""""""""""""""""""""""""""""""""

**1. Clone the repository**

Clone the git repository on your local machine:

.. code-block:: bash

    git clone git@github.com:epoc-ed/GUI.git


**2. Create a New Conda Environment**

Open your terminal (or Anaconda Prompt on Windows) and run:

.. code-block:: bash

    conda create --name jf_gui python=3.10

**3. Activate the Environment**

Now activate your new environment:

.. code-block:: bash

    conda activate jf_gui

**4.Install Packages Using pip**

With your environment active, install all packages from your ``requirements.txt`` by running:

.. code-block:: bash

    cd jungfrau_gui
    pip install -r requirements.txt


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

From the project's root directory:

.. code-block:: bash

    conda install conda-build  # if not already installed
    conda build conda-recepie

This will produce a ``.conda`` (or ``.tar.bz2``) file in your ``conda-bld/<platform>`` directory (often ``conda-bld/noarch`` for noarch packages).

**3. Installing the Newly Built Package**

Normally, you can install the package from the local build by:

.. code-block:: bash

    conda install --use-local jungfrau_gui

Sometimes, you may encounter a situation where the newly built package is not found even though you know it’s in ``conda-bld/``.
In that case, you can install the package directly from the ``.conda`` (or ``.tar.bz2``) file:

.. code-block:: bash

    conda install <path/to/built/package>
    # for example:
    conda install /opt/miniforge/miniforge3/envs/jf_gui/conda-bld/noarch/jungfrau_gui-2025.04.14-py_0.conda
