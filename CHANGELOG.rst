
.. :changelog:

Changelog
---------

0.10 (2016-06-09)
+++++++++++++++++

- Turn into module.

0.9 (2016-06-08)
++++++++++++++++

- Dependency assignment and cancellation for ``Injector`` subclasses.

0.8 (2016-06-05)
++++++++++++++++

- Correct syntax error for Python 2.6

0.7 (2016-06-04)
++++++++++++++++

- Raise ``DependencyError`` for mutual recursion in constructor
  arguments and specified dependencies.
- Show injected dependencies in the ``dir`` result.
- Deny to instantiate ``Injector`` and its subclasses.

0.6 (2016-03-09)
++++++++++++++++

- Deprecate ``c`` alias.  Use real classes.
- Allow to use ``let`` directly on ``Injector``.
- Do not instantiate dependencies named with ``cls`` at the end.

0.5 (2016-03-03)
++++++++++++++++

- Avoid attribute search recursion.  This occurs with inheritance
  chain length started at 3 and missing dependency on first level.
- Add ``c`` alias for ``Injector`` subclass access.
- Add ``let`` factory to temporarily overwrite specified
  dependencies.

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
