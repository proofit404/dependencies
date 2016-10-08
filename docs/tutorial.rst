Inheritance is hard
===================

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

Customer's delivery department needs more detailed instructions that
ours.  We need a special place in our codebase where we can write this
additional behavior for our customer.  We need to extend ``Processor``
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
orders are processed by our customer.  Yep, we will add more methods
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
