==========
DI example
==========

Example application for Dependency Injection demonstration.  It send
email notifications to address you specify in the web form.

Installation
------------

Prepare virtual environment and install package in editable mode

.. code:: bash

    virtualenv di
    . di/bin/activate
    pip install -e .

Run development server and open browser at specified url

.. code:: bash

    python notification.py
