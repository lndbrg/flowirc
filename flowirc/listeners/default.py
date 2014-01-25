__author__ = 'Olle Lundberg'

from ..messages import PingMessage, PongMessage


def register(bot):
    @bot.on(PingMessage)
    def pong(msg):
        print(msg)
        return PongMessage(msg)
