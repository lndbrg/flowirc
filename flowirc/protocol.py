import asyncio
from flowirc.messages import MessageBase

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

