===================
 ``Package`` proxy
===================

``Package`` object is a way to define injector scope with dependencies
defined in other places (like modules and packages).  You can point
package object to the module, a variable defined in the module, a
function defined in the module, a class defined in the module, any
attribute of the class which was defined in this module.

.. code:: python

    from dependencies import Injector, Package

Reasons
=======

If you have complex project structure, you will see a lot of code like
this in your injectors.

.. code:: python

    from application.users.utils import create_user
    # A lot of import statements here...

    class Container(Injector):

        persist_user = create_user
        # A lot of assignment statements here...

To save some typing I tend to write this code like this

.. code:: python

    class Container(Injector):

        from application.users.utils import create_user as persist_user
        # A lot of import statements here...

``Package`` can help to deal with this inconsistency

.. code:: python

    application = Package("application")

    class Container(Injector):

        persist_user = application.users.utils.create_user
        # A lot of assignment statements here...

If a lot of dependencies defined in the utils module, you can set
``Package`` source to the utils module itself.

.. code:: python

    utils = Package("application.users.utils")

    class Container(Injector):

        persist_user = utils.create_user
        # A lot of assignment statements here...
