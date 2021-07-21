# [7.0.0-rc.8](https://github.com/proofit404/dependencies/compare/7.0.0-rc.7...7.0.0-rc.8) (2021-07-21)

### Features

- deny classes to depend on nested injectors
  [#479](https://github.com/proofit404/dependencies/issues/479)
  ([3406946](https://github.com/proofit404/dependencies/commit/340694669c0abff951a1e5c197ea0b10657299ce))

### BREAKING CHANGES

- Injector won't pass nested injectors to the constructor of the class. Use
  `this` objects to access inner attributes of nested injector and pass them to
  the constructor arguments.

# [7.0.0-rc.7](https://github.com/proofit404/dependencies/compare/7.0.0-rc.6...7.0.0-rc.7) (2021-07-21)

### Bug Fixes

- hide scope objects own attributes
  [#514](https://github.com/proofit404/dependencies/issues/514)
  ([6440c97](https://github.com/proofit404/dependencies/commit/6440c9765cdc75a305e5cd7bad9ea8641c5799b3))

# [7.0.0-rc.6](https://github.com/proofit404/dependencies/compare/7.0.0-rc.5...7.0.0-rc.6) (2021-07-17)

### Features

- deny resolve nested injector directly
  [#474](https://github.com/proofit404/dependencies/issues/474)
  ([779d3ac](https://github.com/proofit404/dependencies/commit/779d3ac95ea9838a5f624c529dd830923b2d71bf))

### BREAKING CHANGES

- The only allowed purpose of nested injectors is to be targets for this
  objects.

# [7.0.0-rc.5](https://github.com/proofit404/dependencies/compare/7.0.0-rc.4...7.0.0-rc.5) (2021-07-11)

### Bug Fixes

- store nested injector spec as scalar data type
  [#510](https://github.com/proofit404/dependencies/issues/510)
  ([ac89edb](https://github.com/proofit404/dependencies/commit/ac89edbf9a0d759ffaac34f2fcaf30e1ebbecf2e))

### Features

- respect resolution ruses in package objects
  [#471](https://github.com/proofit404/dependencies/issues/471)
  ([ac27877](https://github.com/proofit404/dependencies/commit/ac278772c364db32dd3550074bf6b15f903a017e))

### BREAKING CHANGES

- Package objects will conform its resolution rules with imported objects. If
  package dependency points to the class, it's allowed to resolve such
  dependency directly. If package object points to the scalar type for example,
  it'll raise exception if you tries to resolve such dependency directly.

# [7.0.0-rc.4](https://github.com/proofit404/dependencies/compare/7.0.0-rc.3...7.0.0-rc.4) (2021-07-09)

### Features

- deny resolve this objects directly
  [#472](https://github.com/proofit404/dependencies/issues/472)
  ([d368589](https://github.com/proofit404/dependencies/commit/d368589ed2d6d2f8800caab9d36cb83ef1ea8fba))

### BREAKING CHANGES

- The only allowed purpose of this objects is to specify dependencies of classes
  and value objects as links to attributes with different names or stored in
  nested Injector classes.

# [7.0.0-rc.3](https://github.com/proofit404/dependencies/compare/7.0.0-rc.2...7.0.0-rc.3) (2021-07-08)

### Features

- deny to resolve value object directly
  [#473](https://github.com/proofit404/dependencies/issues/473)
  ([b3746c3](https://github.com/proofit404/dependencies/commit/b3746c382c282b1a394b71c1067d090ac3364807))

### BREAKING CHANGES

- value objects could only be used to evaluate arguments of classes. Attribute
  access of Injector subclass which result in value object would raise an error.

# [7.0.0-rc.2](https://github.com/proofit404/dependencies/compare/7.0.0-rc.1...7.0.0-rc.2) (2021-07-06)

### Bug Fixes

- initialize dependency graph lazily
  [#241](https://github.com/proofit404/dependencies/issues/241)
  ([4d0d3c9](https://github.com/proofit404/dependencies/commit/4d0d3c90f4c81de7db1e51f5451ec120e8209df9))

# [7.0.0-rc.1](https://github.com/proofit404/dependencies/compare/6.0.1...7.0.0-rc.1) (2021-07-04)

### Features

- scalar dependencies can't be resolved directly
  [#480](https://github.com/proofit404/dependencies/issues/480)
  ([c82e8c5](https://github.com/proofit404/dependencies/commit/c82e8c5af0d4deafab723886d800b53c3aadd059))

### BREAKING CHANGES

- Scalar dependencies are basically data types. They are allowed to be used as
  dependencies for other more complicated data types, like classes. If you need
  to take scalar dependency from Injector subclass, use constant value instead.
  You don't need Injector for this.

## [6.0.1](https://github.com/proofit404/dependencies/compare/6.0.0...6.0.1) (2021-02-20)

### Bug Fixes

- custom error message for enumerations
  [#121](https://github.com/proofit404/dependencies/issues/121)
  ([30cf46e](https://github.com/proofit404/dependencies/commit/30cf46e7b2a6724c17ae928d24641c1490e363b0))

# [6.0.0](https://github.com/proofit404/dependencies/compare/5.2.0...6.0.0) (2021-02-12)

### Features

- deprecate [@operation](https://github.com/operation) object
  [#457](https://github.com/proofit404/dependencies/issues/457)
  ([917b62f](https://github.com/proofit404/dependencies/commit/917b62fae0e76aec2ca1fe7f6178d484820cce97))

### BREAKING CHANGES

- @operation object was removed. You could replace it with @value object
  returning inner function. This inner function would use it's closure to
  resolve injected dependencies.

# [5.2.0](https://github.com/proofit404/dependencies/compare/5.1.0...5.2.0) (2020-11-21)

### Features

- support descriptor protocol
  [#25](https://github.com/proofit404/dependencies/issues/25)
  ([66111b5](https://github.com/proofit404/dependencies/commit/66111b5c4ef257c114c39984585239277fe067ca))

# [5.1.0](https://github.com/proofit404/dependencies/compare/5.0.0...5.1.0) (2020-11-20)

### Features

- support pypy interpreter
  [#42](https://github.com/proofit404/dependencies/issues/42)
  ([bb454e7](https://github.com/proofit404/dependencies/commit/bb454e7038f9d180342bd6e4ccfb43ce33b6452a))

# [5.0.0](https://github.com/proofit404/dependencies/compare/4.1.0...5.0.0) (2020-11-12)

### Build System

- add python 3.9 support
  [#410](https://github.com/proofit404/dependencies/issues/410)
  ([a9526bb](https://github.com/proofit404/dependencies/commit/a9526bbb237a6a143a18e47ed4dc27e08fa7b049))

### BREAKING CHANGES

- drop python 3.6 support.

# [4.1.0](https://github.com/proofit404/dependencies/compare/4.0.1...4.1.0) (2020-10-23)

### Features

- deny to use empty extension scope
  [#398](https://github.com/proofit404/dependencies/issues/398)
  ([18fb528](https://github.com/proofit404/dependencies/commit/18fb5286f6ba6343592461629257ed628713c113))

## [4.0.1](https://github.com/proofit404/dependencies/compare/4.0.0...4.0.1) (2020-10-02)

### Bug Fixes

- handle shadowed default arguments
  [#240](https://github.com/proofit404/dependencies/issues/240)
  ([04f795f](https://github.com/proofit404/dependencies/commit/04f795f1cbb3d4820d2ce0ea58f2aed93610e0e3))

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
<p align="center"><i>The <code>dependencies</code> library is part of the SOLID python family.</i></p>
