Tutorial
========

Inheritance is hard
-------------------

Inheritance is a rigid relation between code blocks, which is hard to
control.  If you add behavior inside child classes, result class at
the end of inheritance chain will collect lots of different methods.
As a consequence of this effect, resulting class collect different
responsibilities in your system.  It becomes hard to understand what
exactly this class serves for.

Lets consider long inheritance chain.  For example, we're writing
order processing system.  An awesome framework, we use, requires to
subclass its ``OrderProcessor`` base class.  It's very common
technique, which is easy to implement.

Everything we need to do on this stage is to validate order and create
instructions for our executives, as a database records for example.

.. code:: python

    class Processor(OrderProcessor):

        def process(self, order):

            assert 'some field' in order
            for params in order.items:
                record = Instruction(**params)
                record.save()

    processors.add(Processor)

Thanks to our sales department, our service becomes popular and new
customers asks for new features.  Now we have a partner company, which
can process some orders with less cost that we do ourselves.  We need
to provide instructions to their executives.  And we do not want to
give them access to our database.  It's a nightmare when several
projects use same database to interact with each other.

As a good engineers we decide to create order instructions in partners
own order processing system through its public API.  But there is no
possibility to do that in our code base with out significant change.
We need to move instructions' save part of the process into separate
method.  ``Processor`` class now looks like this:

.. code:: python

    class Processor(OrderProcessor):

        def process(self, order):

            assert 'some field' in order
            self.store(order)

        def store(self, order):

            for params in order.items:
                record = Instruction(**params)
                record.save()

Now we are able to write integration part for our partner's system:

.. code:: python

    class PartnerProcessor(Processor):

        api_endpoint = 'https://.../api/v1/instructions'

        def store(self, order):

            for params in order.items:
                requests.post(self.api_endpoint, **params)

Partner's delivery department needs more detailed instructions that
ours.  We need a special place in our codebase where we can write this
additional behavior for our partner.  We need to extend ``Processor``
class API one more time.  Also we need to change some methods
signatures so they can work with this new data flow.

.. code:: python

    class Processor(OrderProcessor):

        def process(self, order):

            assert 'some field' in order
            instructions = self.order_instructions(order)
            self.store(instructions)

        def order_instructions(self, order):

            return order.items

        ...

Now we can add additional instructions in the ``Processor``
subclasses:

.. code:: python

    class PartnerProcessor(Processor):

        def order_instructions(self, order):

            instructions = super().order_instructions(order)
            instructions.add(...)
            return instructions

        ...

Now we need to figure out what orders are processed ourselves and what
orders are processed by our partner.  Yep, we will add more methods
to your classes.  Lets say we will look at the order content.  Then we
send a signal to our frame work if we want to skip this processor and
try another one.  This logic make sense only for ``PartnerProcessor``
class.  We can't simply override ``process`` method and call its
parent method.  Logic we want to add kinda in between of it.  So we
add meaningless ``appropriate_order`` method to the ``Processor``
class to have this ability.  Our classes becomes to look like that:

.. code:: python

    class Processor(OrderProcessor):

        def process(self, order):

            assert 'some field' in order
            self.appropriate_order(order)
            instructions = self.order_instructions(order)
            self.store(instructions)

        def appropriate_order(self, order):

            pass

        ...

    class PartnerProcessor(Processor):

        def appropriate_order(self, order):

            if 'partner_flag' not in order:
                raise SkipThisProcessor

        ...

    # Finally we can use our subclass.
    processors.add(PartnerProcessor)

Now we have two classes defining different parts of system behavior.
Thanks to our tireless refactoring our service now have even more
customers.  One customer was so happy by using our product, that he
decide to become our partner.  He wants process some of his orders by
our executives because it's chipper to him.  And some of this orders
are perfect candidates to be processed by our first partner in his
order processing system.  You get it.

We need add more behavior to our system.  One class for regular orders,
which comes from second partner.  One class for orders from second
partner that we want to pass to the first partner.

.. code:: python

    class SecondPartnerProcessor(Processor):

        def appropriate_order(self, order):

            if 'second_partner_flag' not in order:
                raise SkipThisProcessor

    processors.add(SecondPartnerProcessor)

    class SecondToFirstPartnerProcessor(SecondPartnerProcessor, PartnerProcessor):

        def appropriate_order(self, order):

            super().appropriate_order(order)
            super(SecondPartnerProcessor, self).appropriate_order(order)

    processors.add(SecondToFirstPartnerProcessor)

We end up with lots of classes which depends on each other in all
possible combinations.  It is difficult to read and modify this
structure.  Imagine we need to add some additional hooks in between of
process method of our second partner.  This will lead us to each
class modification where we will stub things for the first partner.
Some one can say "Mixins are good for this!"

To mix or not to mix
--------------------

In my opinion mixins are great in this cases:

- mixin class is self containing (no overlapping with another mixins)
- it add functionality based on your own class characteristics

They not so great where you define concrete behavior in mixins and
then try to build concrete units from this separate behavior by using
multiple inheritance and writing adapter methods.  If you saw Django
class based views implementation, you know what I'm talking about.

We will end up with something like this, if we will use this
technique:

.. code:: python

    class SecondToFirstPartnerProcessor(
            AppropriateSecondToFirstPartnerMixin,
            APIStorageMixin,
            DeliveryInstructionsMixin,
            ProcessMixin,
            OrderProcessor):
        pass

    processors.add(SecondToFirstPartnerProcessor)

If I see this class first time, I'll have no idea what he's doing.
It's hard to figure out execution chain because of many overlapping
methods.  ``APIStorageMixin`` define methods used in ``ProcessMixin``.
When you read ``ProcessMixin`` code it looks like ``self.something(``
comes from nowhere.  ``DeliveryInstructionsMixin`` override
``ProcessMixin`` methods.  When you read ``ProcessMixin`` code it
looks like it do something else until you realize it was overwritten
in the upper class.  Your awesome IDE can't get you this information
since ``DeliveryInstructionsMixin`` method usage is outside of
``SecondToFirstPartnerProcessor`` context.  It's hard to work with
this code.
