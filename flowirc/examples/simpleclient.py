import asyncio
import signal
from flowirc.client import IRCClient


__author__ = 'Olle Lundberg'

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, loop.stop)
    bot = IRCClient(__name__)
    bot.run()
    loop.run_forever()
