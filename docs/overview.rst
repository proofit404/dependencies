==========
 Overview
==========

``dependencies`` library provides a nice DSL for specifying relations
of your classes and make instantiation as simple as attribute access.

.. code:: python

    class Container(Injector):
        logger = Logger
        controller = Controller # Constructor of this class needs `logger` argument.
        robot = Robot # Constructor of this class needs `controller` argument.

    Container.robot.run()
    #          `---> This attribute access creates three instances in
    #                the proper order and call each constructor with
    #                proper arguments.
