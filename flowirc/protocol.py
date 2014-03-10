import asyncio
from flowirc.messages import IRCMessage
from flowirc.messages.middleware import ConnectionMessage
from flowirc.log import log
__author__ = 'Olle Lundberg'


class IRCProtocol(asyncio.Protocol):
    """
    IRC Protocol implementation.

    ::

        self.loop = asyncio.get_event_loop()
        transport, protocol = yield from loop.create_connection(
        IRCProtocol, 'localhost', 6667)
    """
    _transport = False
    def connection_made(self, transport):
        log.info("Connected")
        self._transport = transport
        self.message_received(ConnectionMessage)

    def send(self, *lines):
        for line in lines:
            data = line.encode()
            if self._transport:
                log.debug("Sending data: %s", data)
                self._transport.write(data)

    def data_received(self, data):
        lines = data.decode().split("\r\n")
        for line in lines:

            if len(line) <= 2:
                log.debug("Received junk data %s", line)
                continue
            log.debug("Received line %s", line)
            msg = IRCMessage.from_str(line)
            if msg is not None:
                self.message_received(msg)

    def message_received(self, msg):
        raise NotImplementedError("message_received needs to be implemented "
                                  "in a subclass.")
