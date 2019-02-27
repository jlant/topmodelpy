Installation
============

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
| usually specifies that the module/package has been packaged and distributed with the standard Python distribution package 
| called Distutils_.

4. Run `setup.py` with the `install` command::

    $ python setup.py install

topmodelpy will now be installed to the standard location for third-party Python modules on your computer platform.

For more information regarding installing third-party Python modules, please see `Installing Python Modules`_ 
For a description of how installation works including where the module will be installed on your computer platform, please see `How Installation Works`_.


.. _Python: https://www.python.org/
.. _Python's download page: https://www.python.org/downloads/
.. _git: https://git-scm.com/
.. _Distutils: https://docs.python.org/3/library/distutils.html
.. _Installing Python Modules: https://docs.python.org/3.5/install/
.. _How Installation Works: https://docs.python.org/3.5/install/#how-installation-works
