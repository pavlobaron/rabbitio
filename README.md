rabbitio
========

Python module to access a RabbitMQ queue as if it were a file.

Similar to the StringIO abstraction, but for consuming from a RabbitMQ queue. Implements minimal methods only right now to fit my Disco fork's needs.

URL has the form "queue://<QUENAME>". No exchanges are possible yet, but would be easy to implement.

I use it in my Disco fork: https://github.com/pavlobaron/disco, so see it for examples.

You need pika to use this tiny class: https://github.com/pika/pika

Feel free to contribute.
