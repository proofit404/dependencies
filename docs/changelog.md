# 7.2.0 (2022-05-29)

### Features

- restrict sticky scopes
  [#447](https://github.com/proofit404/dependencies/issues/447) 67fbae3

## 7.1.7 (2022-02-04)

### Bug Fixes

- this should not trigger error
  [#531](https://github.com/proofit404/dependencies/issues/531) 99cc55d

## 7.1.6 (2021-12-22)

### Bug Fixes

- deny relative imports in Package declaration
  [#71](https://github.com/proofit404/dependencies/issues/71) 9636e32

## 7.1.5 (2021-12-12)

### Bug Fixes

- correct possible recursion error caused by package import
  [#87](https://github.com/proofit404/dependencies/issues/87) 2304537

## 7.1.4 (2021-12-11)

### Bug Fixes

- correct stack representation in circle error message
  [#525](https://github.com/proofit404/dependencies/issues/525) 8776947

## 7.1.3 (2021-12-10)

### Bug Fixes

- show correct error message for circle error
  [#470](https://github.com/proofit404/dependencies/issues/470) e547c54

## 7.1.2 (2021-12-10)

### Bug Fixes

- show proper hint on nested injector missed dependency
  [#522](https://github.com/proofit404/dependencies/issues/522) 865877d

## 7.1.1 (2021-12-07)

### Bug Fixes

- show resolver stack in missing dependency hint
  [#32](https://github.com/proofit404/dependencies/issues/32) edf4436

# 7.1.0 (2021-07-29)

### Features

- implement sticky scopes
  [#311](https://github.com/proofit404/dependencies/issues/311)

# 7.0.0 (2021-07-21)

### Bug Fixes

- hide scope objects own attributes
  [#514](https://github.com/proofit404/dependencies/issues/514)
- initialize dependency graph lazily
  [#241](https://github.com/proofit404/dependencies/issues/241)
- store nested injector spec as scalar data type
  [#510](https://github.com/proofit404/dependencies/issues/510)

### Features

- deny classes to depend on nested injectors
  [#479](https://github.com/proofit404/dependencies/issues/479)
- deny resolve nested injector directly
  [#474](https://github.com/proofit404/dependencies/issues/474)
- deny resolve this objects directly
  [#472](https://github.com/proofit404/dependencies/issues/472)
- deny to resolve value object directly
  [#473](https://github.com/proofit404/dependencies/issues/473)
- respect resolution ruses in package objects
  [#471](https://github.com/proofit404/dependencies/issues/471)
- scalar dependencies can't be resolved directly
  [#480](https://github.com/proofit404/dependencies/issues/480)

### BREAKING CHANGES

- Injector won't pass nested injectors to the constructor of the class. Use
  `this` objects to access inner attributes of nested injector and pass them to
  the constructor arguments.
- The only allowed purpose of nested injectors is to be targets for this
  objects.
- Package objects will conform its resolution rules with imported objects. If
  package dependency points to the class, it's allowed to resolve such
  dependency directly. If package object points to the scalar type for example,
  it'll raise exception if you tries to resolve such dependency directly.
- The only allowed purpose of this objects is to specify dependencies of classes
  and value objects as links to attributes with different names or stored in
  nested Injector classes.
- value objects could only be used to evaluate arguments of classes. Attribute
  access of Injector subclass which result in value object would raise an error.
- Scalar dependencies are basically data types. They are allowed to be used as
  dependencies for other more complicated data types, like classes. If you need
  to take scalar dependency from Injector subclass, use constant value instead.
  You don't need Injector for this.

## 6.0.1 (2021-02-20)

### Bug Fixes

- custom error message for enumerations
  [#121](https://github.com/proofit404/dependencies/issues/121)

# 6.0.0 (2021-02-12)

### Features

- deprecate [@operation](https://github.com/operation) object
  [#457](https://github.com/proofit404/dependencies/issues/457)

### BREAKING CHANGES

- @operation object was removed. You could replace it with @value object
  returning inner function. This inner function would use it's closure to
  resolve injected dependencies.

# 5.2.0 (2020-11-21)

### Features

- support descriptor protocol
  [#25](https://github.com/proofit404/dependencies/issues/25)

# 5.1.0 (2020-11-20)

### Features

- support pypy interpreter
  [#42](https://github.com/proofit404/dependencies/issues/42)

# 5.0.0 (2020-11-12)

### Build System

- add python 3.9 support
  [#410](https://github.com/proofit404/dependencies/issues/410)

### BREAKING CHANGES

- drop python 3.6 support.

# 4.1.0 (2020-10-23)

### Features

- deny to use empty extension scope
  [#398](https://github.com/proofit404/dependencies/issues/398)

## 4.0.1 (2020-10-02)

### Bug Fixes

- handle shadowed default arguments
  [#240](https://github.com/proofit404/dependencies/issues/240)

# 4.0.0 (2020-10-01)

### Bug Fixes

- correct default argument error message
  [#239](https://github.com/proofit404/dependencies/issues/239)

### Features

- replace let attribute with call
  [#315](https://github.com/proofit404/dependencies/issues/315)

### BREAKING CHANGES

- `let` attribute was removed. Use `Injector()` instead of obsolete
  `Injector.let()`.

# 3.0.0 (2020-08-30)

### Code Refactoring

- drop Python 2.7 and 3.4 support
  [#348](https://github.com/proofit404/dependencies/issues/348)

### BREAKING CHANGES

- Due to the our new policy of enterprise user support we will drop abandoned
  version of python and libraries we are integrated with as soon as they reach
  official end of life.

## 2.0.1 (2020-07-16)

### Bug Fixes

- compatibility with typing module on Python 3.6

# [2.0.0](https://github.com/proofit404/dependencies/compare/1.0.1...2.0.0) (2020-05-17)

### Features

- remove contrib package closes
  [#192](https://github.com/proofit404/dependencies/issues/192)

### BREAKING CHANGES

- Every time a new user asks me how to use their favorite framework together
  with stories and dependencies I understand that there is a missing module in
  the contrib package.

## 1.0.1 (2020-03-31)

### Bug Fixes

- add **wrapped** attribute

# 1.0.0 (2020-02-11)

### Bug Fixes

- prevent generated changelog from style guide violation

## 0.15 (2018-07-21)

- Support `in` checks in the `Injector` subclasses.
- Add `operation` decorator to build injectable functions.
- Add `Package` object to reduce import boilerplate in the `Injector`
  definition.
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

- Add `this` object for aliases and cross injector links.
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

<p align="center">&mdash; ⭐ &mdash;</p>
