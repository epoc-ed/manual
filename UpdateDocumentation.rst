:hide-toc:


Update this documentation
---------------------------

- This site is built automatically using github actions on every push. 
- The deployed version reflects the main branch
- It is also possible to build locally using: make html


Workflow
""""""""""""

**1. Clone the repository**

.. code-block:: bash

    git clone git@github.com:epoc-ed/manual.git


**2. Make a new branch**

.. code-block:: bash

    git branch some_feature
    git checkout some_feature

**3. Make your changes**

**4. Push the new branch to github**

.. code-block:: bash

    git push --set-upstream origin some_feature


**5. Inspect your changes**

- Under the Actions tab you can see the build status of your branch
- If the build is successful, you can download the html files from the artifacts tab

**6. Make PR to merge your changes to the main branch**


Local build
""""""""""""""""

.. note::

    You only need to create the environment once. After that you can activate it and build the documentation.

.. code-block:: bash

    #install the dependencies listed in etc/environment.yml
    conda env create -f etc/environment.yml

    #activate the environment
    conda activate docs

    #build the documentation
    make html
