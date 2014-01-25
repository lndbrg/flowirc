import functools
import importlib
from flowirc.messages import JoinMessage
from flowirc.messages.middleware import ConnectionMessage
from flowirc.middleware import IRCMiddleWare
from flowirc.user import IRCUser
from flowirc.log import log

__author__ = 'Olle Lundberg'


class IRCBot(IRCUser):
    def __init__(self, host='localhost', port=None, full_name=None, *,
                 user="flowirc", nick="flowirc", ssl=None):
        self.middleware = IRCMiddleWare(host, port, ssl)
        super().__init__(full_name, user, nick)

        def identify(msg):
            self.nick = nick
            self.user = user
            self.full_name = full_name

        self.middleware.on(ConnectionMessage, identify)


    def run(self, use_default_listeners=True):
        if use_default_listeners:
            mod = importlib.import_module('flowirc.listeners.default')
            mod.register(self)
            del mod
        self.middleware.run()


    def on(self, message):
        if callable(message):
            message = message()

        def decorator(callback):
            self.middleware.on(message, callback)

            @functools.wraps(callback)
            def f(*args):
                return callback(*args)

            return f

        return decorator

    def run_forever(self, use_default_listeners=True):
        self.run(use_default_listeners)
        self.middleware.loop.run_forever()

    def send(self, lines):
        self.middleware.send(lines)

    def join(self, channel):
        self.send(JoinMessage(channel))
