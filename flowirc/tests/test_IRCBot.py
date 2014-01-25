from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock

from flowirc.bot import IRCBot
from flowirc.messages import PingMessage


__author__ = 'Olle Lundberg'


class TestIRCBot(TestCase):
    @patch('importlib.import_module')
    def test_run(self, mod_register):
        cli = IRCBot()
        cli.middleware = Mock()
        cli.run()
        mod_register.assert_assert_called_once_with(
            'flowirc.listeners.default')
        self.assertEqual(1, cli.middleware.run.call_count)

    @patch('importlib.import_module')
    @patch('asyncio.Task')
    def test_run_no_default_listeners(self, task, mod_register):
        cli = IRCBot()
        cli.middleware = MagicMock(return_value=None)
        cli.run(False)
        self.assertEqual(0, mod_register.call_count)
        self.assertEqual(1, cli.middleware.call_count)

    def test_run_forever(self):
        cli = IRCBot()
        cli.middleware = MagicMock(return_value=None)
        cli.run = Mock()
        cli.run_forever(False)
        cli.run.assert_called_once_with(False)
        self.assertEqual(1, cli.middleware.run_forever.call_count)

    def test_on(self):
        cli = IRCBot(full_name=__name__)
        cli.middleware = Mock(return_value=None)

        @cli.on(PingMessage)
        def foo(msg):
            return True

        self.assertTrue(foo(PingMessage("PING :irc.example.com")))

        @cli.on(PingMessage())
        def foo(msg):
            return True

        self.assertTrue(foo(PingMessage("PING :irc.example.com")))


