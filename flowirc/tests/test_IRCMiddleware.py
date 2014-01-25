from flowirc.messages import PingMessage, PongMessage
from flowirc.middleware import IRCMiddleWare

__author__ = 'Olle Lundberg'
from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock

class TestIRCMiddleware(TestCase):

    @patch('asyncio.get_event_loop')
    def test_init_loops(self, gel):
        IRCMiddleWare(__name__)
        self.assertEqual(1, gel.call_count)
        gel.reset_mock()
        IRCMiddleWare(__name__, loop=Mock())
        self.assertEqual(0, gel.call_count)

    def test_init_ssl_and_ports(self):
        SSL_PORT = 6697
        cli = IRCMiddleWare(__name__, port=SSL_PORT, loop=Mock())
        self.assertTrue(cli.ssl)
        cli = IRCMiddleWare(__name__, ssl=True, loop=Mock())
        self.assertEqual(SSL_PORT, cli.port)
        cli = IRCMiddleWare(__name__)
        self.assertFalse(cli.ssl)
        self.assertEqual(6667, cli.port)

    @patch('asyncio.Task')
    def test_run(self, task):
        cli = IRCMiddleWare(loop=Mock())
        test_object = Mock()
        cli.loop.create_connection = MagicMock(return_value = test_object)
        cli.run()
        self.assertEqual(1, cli.loop.create_connection.call_count)

    def test_matches(self):
        cli = IRCMiddleWare()
        pingmsg = PingMessage("PING :irc.example.com")
        pongmsg = PongMessage(pingmsg)
        self.assertTrue(cli.matches(pingmsg, pingmsg))
        self.assertFalse(cli.matches(pingmsg, pongmsg))
