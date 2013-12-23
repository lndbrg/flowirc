import asyncio
import functools
from collections import defaultdict
from flowirc.protocol import IRCClientProtocol
from flowirc.messages import *


__author__ = 'Olle Lundberg'


class IRCClient(IRCClientProtocol):
    def __init__(self, name=None, host='localhost', port=None,
                 user="flowirc", nick="flowirc", ssl=None, loop=None):
        assert name is not None, "The client needs to be identified by a " \
                                 "name."


        if loop is None:
            loop = asyncio.get_event_loop()

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

    def run_forever(self, use_default_listeners=True):
        self.run(use_default_listeners)
        self.loop.run_forever()

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
