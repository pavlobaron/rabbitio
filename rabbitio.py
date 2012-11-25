from pika import BlockingConnection
from pika.callback import CallbackManager

#<- stupid hack
def sanitize(self, key):
    if hasattr(key, 'method') and hasattr(key.method, 'NAME'):
        return key.method.NAME

    if hasattr(key, 'NAME'):
        return key.NAME

    if hasattr(key, '__dict__') and 'NAME' in key.__dict__:
        return key.__dict__['NAME']

    return str(key)

CallbackManager.sanitize = sanitize
#stupid hack ->

BACKPRESSURE = 100
SLEEP = 1
DUMMYSIZE = 9999

class RabbitIO(object):

    def __init__(self, queue, sze=DUMMYSIZE):
        self.connection = BlockingConnection()
        self.connection.set_backpressure_multiplier(BACKPRESSURE)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue,
                                   durable=True, exclusive=False, auto_delete=False)
        self.i = 0
        self.sze = sze
        self.queue = queue

    def __iter__(self):
        data = self.read()
        while data and data != '':
            yield data
            data = self.read()

    def __len__(self):
        return self.sze # clear mismatch: the number of messages is dynamic...
        # probably would make sense to configure through the constructor if
        # the number of expected messages is known. Wouldn't work though if
        # trying to work with dynamic streams. Could make sense to close the connection
        # if no messages are in the queue, and expect the client side to catch the
        # corresponding exception

    def close(self):
        self.connection.close()

    def read(self):
        method_frame, header_frame, body = self.channel.basic_get(self.queue, no_ack=True)

        # try only twice after 1s sleep, then give up assuming there are no messages
        # anymore
        if not body:
            self.connection.sleep(SLEEP)
            method_frame, header_frame, body = self.channel.basic_get(self.queue, no_ack=True)

        if not body:
            body = ''

        self.i += len(body)

        return body

    def tell(self):
        return self.i

    def seek(self, pos):
        # there is no matching for modes, it can only be walked forward
        i = pos
        while i > 0:
            self.channel.basic_get(self.queue, no_ack=True) # consume, don't reject
            i -= 1
