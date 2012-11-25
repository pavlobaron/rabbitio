rabbitio
========

Python module to access a RabbitMQ queue as if it were a file.

Similar to the StringIO abstraction, but for consuming from a RabbitMQ queue. Implements minimal methods only right now to fit my Disco fork's needs.

URL as the only constructor argument is simply the name of the queue. No exchanges are possible yet, but would be easy to implement. Also, the module yet expects all default RabbitMQ connection settings. In the future, if necessary, an AMQP url can be added as parameter for non-default connection settings.

I use it in my Disco fork: https://github.com/pavlobaron/disco, so see it for examples.

You need pika to use this tiny class: https://github.com/pika/pika

Feel free to contribute.
