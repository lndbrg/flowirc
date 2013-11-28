import signal
import functools
from collections import defaultdict

import asyncio

from flowirc.messages import *


__author__ = 'Olle Lundberg'


class IRCClientProtocol(asyncio.Protocol):
    """
    IRC Protocol implementation.

    ::

        self.loop = asyncio.get_event_loop()
        transport, protocol = yield from loop.create_connection(
        IRCClientProtocol, 'localhost', 6667)
    """

    def connection_made(self, transport):
        self._transport = transport
        self.after_connection_made()

    def _encode(self, data):
        return str(data).encode()

    def send(self, line):
        data = self._encode(line)
        print(data)
        self._transport.write(data)

    def data_received(self, data):
        lines = data.decode().split("\r\n")
        for line in lines:
            print(line)
            if len(line) <= 2:
                # This is a blank line, at best.
                continue
            msg = MessageBase.from_str(line)
            if msg is not None:
                asyncio.Task(self.message_received(msg))


_listeners = defaultdict(list)


def listen_to(message):
    if callable(message):
        message = message()

    def decorator(callback):
        _listeners[message.type()].append((message, asyncio.coroutine(
            callback)))

        @functools.wraps(callback)
        def f(*args):
            return callback(*args)

        return f

    return decorator


class IRCClient(IRCClientProtocol):
    @classmethod
    def connect(cls, host='localhost', port=6667, ircname="flowirc",
                ircnick="flowirc", ssl=None, loop=None):

        if loop is None:
            loop = asyncio.get_event_loop()
        if ssl is None:
            ssl = True if port == 6697 else False

        self = cls()
        self.ircname = ircname
        self.ircnick = ircnick
        asyncio.Task(loop.create_connection(
            lambda: self,
            host=host,
            port=port,
            ssl=ssl))

    def after_connection_made(self):
        self.identify()
        self.join("#foo")

    def identify(self):
        self.nick()
        self.user()

    def nick(self):
        self.send(NickMessage(self.ircnick))

    def join(self, channel):
        self.send(JoinMessage(channel))

    def user(self):
        self.send(UserMessage(self.ircnick, self.ircname))

    @asyncio.coroutine
    def message_received(self, msg):
        listeners = _listeners[msg.type()]
        print("Listeners for messagetype {}: {}".format(msg.type(), listeners))

        coroutines = [callback(msg) for message, callback in
                      listeners if self.matches(message, msg)]
        for future in asyncio.as_completed(coroutines):
            result = yield from future
            if isinstance(result, MessageBase):
                self.send(result)

    def matches(self, message1, message2):
        return True


@listen_to(PingMessage)
def song(msg):
    reply = PongMessage(msg)
    return reply


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, loop.stop)
    IRCClient.connect()
    loop.run_forever()
