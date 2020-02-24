# -*- coding: utf-8 -*-
from dependencies import Injector
from dependencies import this


class Container(Injector):

    foo = 1
    bar = (this << 1).baz


class SubContainer(Injector):

    bar = (this << 1).foo


class SubSubContainer(Injector):

    bar = (this << 2).foo


class SubContainer1(Injector):

    bar = (this << 1).SubContainer2.baz


class SubContainer2(Injector):

    baz = (this << 1).SubContainer1.bar
