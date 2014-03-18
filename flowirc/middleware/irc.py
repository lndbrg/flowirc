import asyncio
from flowirc.message import IRCMessage
from flowirc.middleware.base import MiddleWareBase
from flowirc.log import log


__author__ = 'Olle Lundberg'


class IRCMiddleWare(MiddleWareBase):
    def on(self, message, callback):
        if callable(message):
            message = message()
        log.debug("Registering callback %r for messagetype %s",
                  callback,
                  message.type())
        self.add_listener(message.type(), callback, message)

    def dispatch(self, data):
        if isinstance(data, IRCMessage):
            log.debug("Sending message: %s", data)
            yield self.dispatch_message(data)


    def matches(self, message1, message2):
        return message1 == message2
