from collections import defaultdict

import asyncio
from flowirc.messages import IRCMessage
from flowirc.log import log
from flowirc.protocol import IRCClientProtocol


class IRCMiddleWare(IRCClientProtocol):
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

        self.__listeners = defaultdict(list)
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
        asyncio.Task(self.dispatch_message(message))

    def on(self, message, callback):
        if callable(message):
            message = message()
        log.debug("Registering callback %s for messagetype %s",
                  callback,
                  message.type())
        self.__listeners[message.type()]. \
            append((message, asyncio.coroutine(callback)))


    @asyncio.coroutine
    def dispatch_message(self, message):
        log.debug("Received message: %s", message)
        listeners = self.__listeners[message.type()]

        coroutines = [callback(message) for message_type, callback in
                      listeners if self.matches(message, message_type)]
        for future in asyncio.as_completed(coroutines):
            result = yield from future
            if isinstance(result, IRCMessage):
                log.debug("Sending message: %s", result)
                self.send(result)


    def matches(self, message1, message2):
        return True
