__author__ = 'Olle Lundberg'

from ..messages import PingMessage, PongMessage


def register(bot):

    @bot.listen_to(PingMessage)
    def pong(msg):
        return PongMessage(msg)
