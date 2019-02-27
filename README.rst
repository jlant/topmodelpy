.. image:: https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/USGS_logo_green.svg/320px-USGS_logo_green.svg.png
        :target: http://www.usgs.gov/
        :alt: U.S. Geological Survey logo

topmodelpy
===============================

topmodelpy is a command line interface for a rainfall-runoff model, 
called Topmodel, that predicts the amount of water flow in rivers.


Features
--------

Add a list of features.


Example
-------

Add a short example

::

    show some example code here


Documentation
-------------

Add a link to the project and code documenation site.


Tests
-----

A suite of tests were built using `pytest <http://pytest.org/latest/>`_.

To run the test suite, from the command line in the project's root directory::

    $ py.test tests/



Requirements
------------

Add requirements and code dependencies.


Installation
------------

To install topmodelpy from source:

1. Check that you have Python_ installed::

    $ python --version

If you do not have Python_ installed, please download the latest version from `Python's download page`_

2. Download topmodelpy from the repository and extract to a directory of your choice.

   Or, if you have git_ installed you can clone the project::

    $ git clone <remote url to topmodelpy>

3. Navigate to the project's root directory where the setup script called `setup.py` is located::

    $ cd topmodelpy/

| The `setup.py` is a Python file that contains information regarding the installation of a Python module/package, and
| usually specifies that the module/package has been packaged and distributed with the standard Python distribution
| package called Distutils_.

4. Run `setup.py` with the `install` command::

    $ python setup.py install

topmodelpy will now be installed to the standard location for third-party Python modules on your
computer platform.

For more information regarding installing third-party Python modules, please see `Installing Python Modules`_
For a description of how installation works including where the module will be installed on your computer platform,
please see `How Installation Works`_.


License
-------

This software is licensed under `CC0 1.0`_ and is in the `public domain`_ because it contains materials that originally
came from the `U.S. Geological Survey (USGS)`_, an agency of the `United States Department of Interior`_. For more
information, see the `official USGS copyright policy`_.

.. image:: http://i.creativecommons.org/p/zero/1.0/88x31.png
        :target: http://creativecommons.org/publicdomain/zero/1.0/
        :alt: Creative Commons logo


Disclaimer
----------

This software is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely
best science. The software has not received final approval by the U.S. Geological Survey (USGS). No warranty, expressed
or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor
shall the fact of release constitute any such warranty. The software is provided on the condition that neither the USGS
nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the
software.

The USGS provides no warranty, expressed or implied, as to the correctness of the furnished software or the suitability
for any purpose. The software has been tested, but as with any complex software, there could be undetected errors. Users
who find errors are requested to report them to the USGS.

References to non-USGS products, trade names, and (or) services are provided for information purposes only and do not
constitute endorsement or warranty, express or implied, by the USGS, U.S. Department of Interior, or U.S. Government, as
to their suitability, content, usefulness, functioning, completeness, or accuracy.

Although this program has been used by the USGS, no warranty, expressed or implied, is made by the USGS or the United
States Government as to the accuracy and functioning of the program and related program material nor shall the fact of
distribution constitute any such warranty, and no responsibility is assumed by the USGS in connection therewith.

This software is provided "AS IS."


Author
------

Jeremiah Lant <jlant@usgs.gov>


.. _Python: https://www.python.org/
.. _pytest: http://pytest.org/latest/
.. _Sphinx: http://sphinx-doc.org/
.. _public domain: https://en.wikipedia.org/wiki/Public_domain
.. _CC0 1.0: http://creativecommons.org/publicdomain/zero/1.0/
.. _U.S. Geological Survey: https://www.usgs.gov/
.. _USGS: https://www.usgs.gov/
.. _U.S. Geological Survey (USGS): https://www.usgs.gov/
.. _United States Department of Interior: https://www.doi.gov/
.. _official USGS copyright policy: http://www.usgs.gov/visual-id/credit_usgs.html#copyright/
.. _U.S. Geological Survey (USGS) Software User Rights Notice: http://water.usgs.gov/software/help/notice/
.. _Python's download page: https://www.python.org/downloads/
.. _git: https://git-scm.com/
.. _Distutils: https://docs.python.org/3/library/distutils.html
.. _Installing Python Modules: https://docs.python.org/3.5/install/
.. _How Installation Works: https://docs.python.org/3.5/install/#how-installation-works
