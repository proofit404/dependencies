============
 Why not...
============

Here we will try to collect pros and cons of different approaches to
make your code extendable and reusable.

Let's imagine we have an order processing system.  We want to
implement to implement order purchase feature.  There is a lot of
functionality should be implemented.  We should change our data, we
should send a request to the payment processing system, we should send
notification to user.

Simple functions
================

Let's do it with simple functions

.. code:: python

    def purchase(user, product, shipment_details)

        create_order(user, product)
        final_price = calculate_price(product, shipment_details)
        order_details = request_payment(user, shipment_details)
        notify_user(user, order_details)

    # ...

    def notify_user(user, order_details):

        log_notification(user, order_details)
        subject = get_notification_subject(order_details)
        message = get_notification_text(user, order_details)
        send_notification(user, subject, message)

    def send_notification(user, subject, message):

        email = get_user_email(user)
        send_email(email, subject, message)

It's readable and straightforward solution.   What could possible go
wrong?

It's hard to change and extend this code.

For example you need to add SMS and push notifications in addition to
plain text emails.  There is a lot of different conditions added to
this simple default path.

Push notification to the mobile app should be written in the markdown
format, SMS requires plain text, email needed HTML in addition to the
plain text.  Users should be able to choice  their preferred
notification method.

How we can change this code above to match new requirements?

We have problems on all three layers of your code.  All ``purchase``,
``notify_user`` and ``send_notification`` should be changed in some
way.

1. Add conditions to all parameters to all layers of the code.

   This will end up with messy code which is even harder to extend.
   No one want ``purchase`` function to have 12 arguments.  No one
   want to wonder why ``send_email`` function accepts phone number.
   No one want to read 7 ``if`` statements in the ``notify_user``
   function when they about to add eighth condition.

2. Add context variable instead of another argument.

   This little ``ctx`` argument instead of email address, phone
   number, product price and shipment destination will save us a lot
   of typing between function calls.  But we still have bunch of
   ``if`` statements.

3. Copy-paste this module and reimplement each feature separately.

   Each feature will be readable and simple on it's own, but you will
   regret this decision when usage of the ``request_payment`` or
   ``calculate_price`` changed.

But we still have the same problem.  We can't substitute
implementation details of low level code without changing high level
policies.  Let's try...

Inheritance
===========

Let's rewrite our functions in the single class so we can alter logic
in the subclasses.

.. code:: python

    class Order:

        def __init__(self, user, product, shipment_details):

            self.user = user
            self.product = product
            self.shipment_details = shipment_details
            self.final_price = None  # Set by `calculate_price`.
            self.order_details = None  # Set by `request_payment`.
            self.subject = None  # Set by `get_notification_subject`.
            self.message = None  # Set by `get_notification_text`.
            self.email = None  # Set by `get_user_email`.

        def purchase(self):

            self.create_order()
            self.calculate_price()
            self.request_payment()
            self.notify_user()

        # ...

        def notify_user(self):

            self.log_notification()
            self.get_notification_subject()
            self.get_notification_text()
            self.send_notification()

        def send_notification(self):

            self.get_user_email()
            self.send_email()

At first look this class is even better solution.  Indeed, this code
has few pros.

1. At first glance high level methods even more readable.

   There are no nosy arguments or variables.  Only nice named methods.

2. Simple code reuse.

   With inheritance we can simply override any method on any layer of
   abstraction in the system.  We can add any number of methods or
   attributes is the child classes.  Looks like it is very reasonable
   approach.

But this code has much more hidden cons at more precise analysis.

1. God object.

   One class contains methods related to every single layer of
   abstraction in the system.  It's hard to manage two hundred methods
   in the same class.  One will process HTTP request, another one will
   send email, another one will write to the database.  It's hard to
   figure out what *exactly* this class does.

2. Bad state management.

   During life time of the instance different methods change state of
   the class.  When you read short method somewhere inside email
   sender logic you have no idea *from where* attributes came from and
   *when exactly* they were set.  Hello ``print`` statements to
   understand the code...

Let's reduce amount of logic in the class (responsibility of the
class).  Let's try...

Mixins
======

We can split our God object into multiple classes and join it together
later using multiple inheritance.

.. code:: python

    class OrderProcessingMixin:

        def create_order(self):

            # ...

    class PriceCalculationMixin:

        def calculate_price(self):

            # ...

    class NotificationMixin:

        def get_notification_text(self):

            self.notification_text = self.notification_text_template % (
                self.user,
                self.order_details,
            )

    class Order(OrderProcessingMixin,
                PriceCalculationMixin,
                NotificationMixin):

        def before_calculate(self):

            self.create_order()

        def after_commit(self):

            self.send_email()

Someone might say this is an improvement over one huge class.

1. All methods grouped around classes with the same responsibility.

2. Better code reuse.  We can use the same notification mechanism in
   different classes with just one line of code.

But there are a lot of problems too.  Imagine you during debugging
session of the ``Order`` class.

1. In the ``get_notification_text`` you have no idea who set up
   ``order_details``.

2. In the ``Order`` class itself you see bunch of low level methods
   which are deep implementation details.  What public method I should
   call?   When notification will be sent exactly?

This code is much harder to understand than it should be.  Even if it
reusable, this complexity in too big for my head.  Let's try...

Composition
===========

Composition is a powerful pattern of organizing code with proper
code boundaries and clear dependency relationship.

.. code:: python

    class OrderProcessor:

        def create(self, user, product):

            # ...

    class PriceCalculator:

        def calculate(self, product, shipment_details):

            # ...

    class Notification:

        def __init__(self, logger):

            self.logger = logger

        def notify(self, user, order_details):

            self.logger.record(user, order_details)
            subject = self.get_notification_subject(order_details)
            message = self.get_notification_text(user, order_details)
            self.send_notification(user, subject, message)

    class Order:

        def __init__(self, order_processor, price_calculator,
                     payment_processor, notification):

            self.order_processor = order_processor
            self.price_calculator = price_calculator
            self.payment_processor = payment_processor
            self.notification = notification

        def purchase(self, user, product, shipment_details)

            self.order_processor.create(user, product)
            final_price = self.price_calculator.calculate(product, shipment_details)
            order_details = self.payment_processor.request(user, shipment_details)
            self.notification.notify(user, order_details)

    Order(
        OrderProcessor(),
        PriceCalculator(),
        PaymentProcessor(),
        Notification(Logger()),
    ).purchase(user, product, shipment_details)

This code has few really good characteristics.

1. It's clean where things were defined.  If you try to understand
   what's wrong with your system, you can just use traceback.  No
   nasty code execution paths.

2. You system became really configurable, you can **inject** pretty
   much any implementation without changing high-level code.

But there one unfortunate consequence of this style

1. There are to much boilerplate on the initiation stage.

Let's try...

Dependencies
============

Here where ``dependencies`` library comes in.

.. code:: python

    from dependencies import Injector

    class OrderContainer(Injector):

        order = Order
        order_processor = OrderProcessor
        price_calculator = PriceCalculator
        payment_processor = PaymentProcessor
        notification = Notification
        logger = Logger

    OrderContainer.order.purchase(user, product, shipment_details)

It helps you to reduce the boilerplate of the initiation stage.  It
doesn't require you to change your code.  You still can to instantiate
your classes your self if you don't like this library.
