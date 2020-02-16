# 1.0.0 (2020-02-11)

### Bug Fixes

- prevent generated changelog from style guide violation ([d3a472f](https://github.com/dry-python/dependencies/commit/d3a472f1779f443be0d9f3321c8451241ee723ff))

## 0.15 (2018-07-21)

- Support `in` checks in the `Injector` subclasses.
- Add `operation` decorator to build injectable functions.
- Add `Package` proxy to reduce import boilerplate in the `Injector`
  definition.
- Add Celery contrib to define tasks from `Injector` subclasses.
- Add Py.Test contrib to define fixtures from `Injector` subclasses.
- Add Django contrib to define views from `Injector` subclasses.
- Add Django REST Framework contrib to define API views and model view
  sets from `Injector` subclasses.
- A class named attributes should end with `_class`.
- Improved error messages for missing dependencies.
- Raise `DependencyError` instead of `AttributeError` for missed
  dependencies.
- Drop python 2.6 and 3.4 support.

## 0.14 (2018-04-13)

- Add `this` proxy object for aliases and cross injector links.
- Deprecate attribute assignment and `use` decorator.
- Release under BSD license.

## 0.13 (2016-10-09)

- Performance improvements.

## 0.12 (2016-09-29)

- Allow multiple inheritance for Injector subclasses.
- Evaluate dependencies once.
- Add `use` decorator.
- Allow nested injectors.

## 0.11 (2016-08-22)

- Twelve times speed up.
- Protect from incorrect operations with attribute assignment.
- Deny \*args and \*\*kwargs in the injectable classes.
- Classes can be used as default argument values only if argument name
  ends with `_cls`.
- Remove `six` library from install requires.

## 0.10 (2016-06-09)

- Turn into module.

## 0.9 (2016-06-08)

- Dependency assignment and cancellation for `Injector` subclasses.

## 0.8 (2016-06-05)

- Correct syntax error for Python 2.6

## 0.7 (2016-06-04)

- Raise `DependencyError` for mutual recursion in constructor
  arguments and specified dependencies.
- Show injected dependencies in the `dir` result.
- Deny to instantiate `Injector` and its subclasses.

## 0.6 (2016-03-09)

- Deprecate `c` alias. Use real classes.
- Allow to use `let` directly on `Injector`.
- Do not instantiate dependencies named with `cls` at the end.

## 0.5 (2016-03-03)

- Avoid attribute search recursion. This occurs with inheritance chain
  length started at 3 and missing dependency on first level.
- Add `c` alias for `Injector` subclass access.
- Add `let` factory to temporarily overwrite specified dependencies.

## 0.4 (2016-03-03)

- Detect `object.__init__` and skip it in the argument injection.

## 0.3 (2016-03-02)

- Deprecate injectable mechanism. Injector may inject any arguments to
  any classes. Injector now support multiple DI targets. All possible
  targets now specified in the Injector attributes. Only single base
  inheritance allowed for Injector subclasses.

## 0.2 (2016-02-13)

- Allows to override dependencies specified with Injector by
  inheritance from this Injector subclass.

## 0.1 (2016-01-31)

- Initial release.
