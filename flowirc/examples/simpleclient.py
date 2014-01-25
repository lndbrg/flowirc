import asyncio
import signal
from flowirc.bot import IRCBot


__author__ = 'Olle Lundberg'

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, loop.stop)
    bot = IRCBot()
    bot.run()
    loop.run_forever()
