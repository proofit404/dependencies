
.. :changelog:

Changelog
---------

0.4 (2016-03-03)
++++++++++++++++

- Detect ``object.__init__`` and skip it in the argument injection.

0.3 (2016-03-02)
++++++++++++++++

- Deprecate injectable mechanism.  Injector may inject any arguments
  to any classes.  Injector now support multiple DI targets.  All
  possible targets now specified in the Injector attributes.  Only
  single base inheritance allowed for Injector subclasses.

0.2 (2016-02-13)
++++++++++++++++

- Allows to override dependencies specified with Injector by
  inheritance from this Injector subclass.

0.1 (2016-01-31)
++++++++++++++++

- Initial release.
