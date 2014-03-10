import functools
import importlib
from flowirc.client import IRCClient
from flowirc.messages import JoinMessage
from flowirc.messages.middleware import ConnectionMessage
from flowirc.middleware import IRCMiddleWare
from flowirc.user import IRCUser
from flowirc.log import log

__author__ = 'Olle Lundberg'


class IRCBot:
    def __init__(self, host='localhost', port=None, full_name=None, *,
                 user="flowirc", nick="flowirc", ssl=None):
        self.client = IRCClient(host, port, ssl)
        self.user = IRCUser(full_name, user, nick)

        self.client.on(ConnectionMessage, lambda x: x)


    def run(self, use_default_listeners=True):
        if use_default_listeners:
            mod = importlib.import_module('flowirc.listeners.default')
            mod.register(self)
            del mod
        self.client.run()


    def on(self, message):
        def decorator(callback):
            self.client.on(message, callback)

            @functools.wraps(callback)
            def f(*args):
                return callback(*args)

            return f

        return decorator

    def run_forever(self, use_default_listeners=True):
        self.run(use_default_listeners)
        self.client.loop.run_forever()

    def send(self, lines):
        self.client.send(lines)

    def join(self, channel):
        self.send(JoinMessage(channel))
