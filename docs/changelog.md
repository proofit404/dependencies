## [4.0.1](https://github.com/proofit404/dependencies/compare/4.0.0...4.0.1) (2020-10-02)


### Bug Fixes

* handle shadowed default arguments [#240](https://github.com/proofit404/dependencies/issues/240) ([04f795f](https://github.com/proofit404/dependencies/commit/04f795f1cbb3d4820d2ce0ea58f2aed93610e0e3))

# [4.0.0](https://github.com/proofit404/dependencies/compare/3.0.0...4.0.0) (2020-10-01)

### Bug Fixes

- correct default argument error message
  [#239](https://github.com/proofit404/dependencies/issues/239)
  ([1d7c436](https://github.com/proofit404/dependencies/commit/1d7c4364749609fb87399f6e5ddee099e8885824))

### Features

- replace let attribute with call
  [#315](https://github.com/proofit404/dependencies/issues/315)
  ([1c84ea9](https://github.com/proofit404/dependencies/commit/1c84ea96ed3bef1b7f57b219a743b98a3837e9ca))

### BREAKING CHANGES

- `let` attribute was removed. Use `Injector()` instead of obsolete
  `Injector.let()`.

# [3.0.0](https://github.com/proofit404/dependencies/compare/2.0.1...3.0.0) (2020-08-30)

### Code Refactoring

- drop Python 2.7 and 3.4 support
  [#348](https://github.com/proofit404/dependencies/issues/348)
  ([360ad90](https://github.com/proofit404/dependencies/commit/360ad90b51063e5c14b4df9b643caee25aba4848))

### BREAKING CHANGES

- Due to the our new policy of enterprise user support we will drop abandoned
  version of python and libraries we are integrated with as soon as they reach
  official end of life.

## [2.0.1](https://github.com/proofit404/dependencies/compare/2.0.0...2.0.1) (2020-07-16)

### Bug Fixes

- compatibility with typing module on Python 3.6
  ([137741f](https://github.com/proofit404/dependencies/commit/137741fb29d69f6ffe22d949e05f9db06c706a38))

# [2.0.0](https://github.com/proofit404/dependencies/compare/1.0.1...2.0.0) (2020-05-17)

### Features

- remove contrib package
  ([5bfe041](https://github.com/proofit404/dependencies/commit/5bfe041f72bc82a4a24ea47599cf2bfbb8d13900)),
  closes [#192](https://github.com/proofit404/dependencies/issues/192)

### BREAKING CHANGES

- Every time a new user asks me how to use their favorite framework together
  with stories and dependencies I understand that there is a missing module in
  the contrib package.

## [1.0.1](https://github.com/proofit404/dependencies/compare/1.0.0...1.0.1) (2020-03-31)

### Bug Fixes

- add **wrapped** attribute
  ([e3c7aa9](https://github.com/proofit404/dependencies/commit/e3c7aa98cec4b33146c98855ae851fa57c990367))

# 1.0.0 (2020-02-11)

### Bug Fixes

- prevent generated changelog from style guide violation
  ([d3a472f](https://github.com/proofit404/dependencies/commit/d3a472f1779f443be0d9f3321c8451241ee723ff))

## 0.15 (2018-07-21)

- Support `in` checks in the `Injector` subclasses.
- Add `operation` decorator to build injectable functions.
- Add `Package` proxy to reduce import boilerplate in the `Injector` definition.
- Add Celery contrib to define tasks from `Injector` subclasses.
- Add Py.Test contrib to define fixtures from `Injector` subclasses.
- Add Django contrib to define views from `Injector` subclasses.
- Add Django REST Framework contrib to define API views and model view sets from
  `Injector` subclasses.
- A class named attributes should end with `_class`.
- Improved error messages for missing dependencies.
- Raise `DependencyError` instead of `AttributeError` for missed dependencies.
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
- Classes can be used as default argument values only if argument name ends with
  `_cls`.
- Remove `six` library from install requires.

## 0.10 (2016-06-09)

- Turn into module.

## 0.9 (2016-06-08)

- Dependency assignment and cancellation for `Injector` subclasses.

## 0.8 (2016-06-05)

- Correct syntax error for Python 2.6

## 0.7 (2016-06-04)

- Raise `DependencyError` for mutual recursion in constructor arguments and
  specified dependencies.
- Show injected dependencies in the `dir` result.
- Deny to instantiate `Injector` and its subclasses.

## 0.6 (2016-03-09)

- Deprecate `c` alias. Use real classes.
- Allow to use `let` directly on `Injector`.
- Do not instantiate dependencies named with `cls` at the end.

## 0.5 (2016-03-03)

- Avoid attribute search recursion. This occurs with inheritance chain length
  started at 3 and missing dependency on first level.
- Add `c` alias for `Injector` subclass access.
- Add `let` factory to temporarily overwrite specified dependencies.

## 0.4 (2016-03-03)

- Detect `object.__init__` and skip it in the argument injection.

## 0.3 (2016-03-02)

- Deprecate injectable mechanism. Injector may inject any arguments to any
  classes. Injector now support multiple DI targets. All possible targets now
  specified in the Injector attributes. Only single base inheritance allowed for
  Injector subclasses.

## 0.2 (2016-02-13)

- Allows to override dependencies specified with Injector by inheritance from
  this Injector subclass.

## 0.1 (2016-01-31)

- Initial release.

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The dependencies library is part of the SOLID python family.</i></p>
