import asyncio
from flowirc.log import log
from flowirc.middleware import IRCMiddleWare
from flowirc.protocol import IRCProtocol

__author__ = 'Olle Lundberg'


class IRCClient(IRCProtocol, IRCMiddleWare):
    def __init__(self, host='localhost', port=None, ssl=None, loop=None):
        if port is None:
            if ssl:
                port = 6697
            else:
                port = 6667

        if ssl is None:
            if port == 6697:
                ssl = True
            else:
                ssl = False
        if loop is None:
            loop = asyncio.get_event_loop()

        self.host = host
        self.port = port
        self.ssl = ssl
        self.loop = loop


    def run(self):
        log.info("Connecting to: %s:%s (ssl: %s)",
                 self.host,
                 self.port,
                 self.ssl)
        asyncio.Task(self.loop.create_connection(
            lambda: self,
            host=self.host,
            port=self.port,
            ssl=self.ssl))

    def run_forever(self):
        self.run()
        self.loop.run_forever()

    def message_received(self, message):
        asyncio.Task(self.trigger(message))

    @asyncio.coroutine
    def dispatch_message(self, message):
        self.send(message)
