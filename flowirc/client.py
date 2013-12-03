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

    def send(self, *lines):
        for line in lines:
            data = line.encode()
            self._transport.write(data)

    def data_received(self, data):
        lines = data.decode().split("\r\n")
        for line in lines:

            if len(line) <= 2:
                continue

            msg = MessageBase.from_str(line)

            if msg is not None:
                asyncio.Task(self.message_received(msg))


class IRCClient(IRCClientProtocol):
    def __init__(self, name=None, host='localhost', port=6667,
                 user="flowirc", nick="flowirc", ssl=None, loop=None):

        if loop is None:
            loop = asyncio.get_event_loop()
        if ssl is None:
            ssl = True if port == 6697 else False

        self.__listeners = defaultdict(list)
        self._name = name
        self._nick = nick
        self._user = user
        self.host = host
        self.port = port
        self.ssl = ssl
        self.loop = loop

    def run(self, use_default_listeners=True):
        if use_default_listeners:
            mod = importlib.import_module('flowirc.listeners.default')
            mod.register(self)
            del mod

        asyncio.Task(self.loop.create_connection(
            lambda: self,
            host=self.host,
            port=self.port,
            ssl=self.ssl))

    def after_connection_made(self):
        self.identify()
        self.join("#foo")

    def identify(self):
        self.nick()
        self.user()

    def nick(self, nick=None):
        if nick is not None and nick != self._nick:
            self._nick = nick
        self.send(NickMessage(self._nick))

    def user(self, user=None):
        if user is not None and user != self._user:
            self._user = user
        self.send(UserMessage(self._nick, self._user))

    def join(self, channel):
        self.send(JoinMessage(channel))

    def listen_to(self, message):
        if callable(message):
            message = message()

        def decorator(callback):
            self.__listeners[message.type()]. \
                append((message, asyncio.coroutine(callback)))

            @functools.wraps(callback)
            def f(*args):
                return callback(*args)

            return f

        return decorator

    @asyncio.coroutine
    def message_received(self, msg):
        listeners = self.__listeners[msg.type()]

        coroutines = [callback(msg) for message, callback in
                      listeners if self.matches(message, msg)]
        for future in asyncio.as_completed(coroutines):
            result = yield from future
            if isinstance(result, MessageBase):
                self.send(result)

    def matches(self, message1, message2):
        return True
