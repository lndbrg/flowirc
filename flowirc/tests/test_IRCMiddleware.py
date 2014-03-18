from flowirc.message import PingMessage, PongMessage
from flowirc.middleware import IRCMiddleWare

__author__ = 'Olle Lundberg'
from unittest import TestCase, expectedFailure
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
        cli.loop.create_connection = MagicMock(return_value=test_object)
        cli.run()
        self.assertEqual(1, cli.loop.create_connection.call_count)

    def test_run_forever(self):
        cli = IRCMiddleWare(loop=Mock())
        cli.run = Mock()
        cli.run_forever()
        self.assertEqual(1, cli.run.call_count)
        self.assertEqual(1, cli.loop.run_forever.call_count)


    @patch('asyncio.coroutine')
    def test_on(self, coro):
        cli = IRCMiddleWare(loop=Mock())
        callback = Mock(side_effect='called')
        cli.on(PingMessage, callback)
        coro.assert_called_once_with(callback)
        coro.reset_mock()
        cli.on(PingMessage(), callback)
        coro.assert_called_once_with(callback)

    @patch('asyncio.Task')
    def test_message_received(self, task):
        cli = IRCMiddleWare(loop=Mock())
        cli.dispatch_message = Mock()
        cli.message_received(False)
        cli.dispatch_message.assert_called_once_with(False)
        self.assertEqual(1, task.call_count)

    @expectedFailure
    def test_matches(self):
        cli = IRCMiddleWare(loop=Mock())
        self.assertTrue(cli.matches(PingMessage("irc.example.com"),
                                    PingMessage("irc.example.com")))
        self.assertFalse(cli.matches(PingMessage("irc.example.com"),
                                    PingMessage("irc2.example.com")))

    def test_dispatch_message(self):
        import asyncio

        loop = asyncio.get_event_loop()
        cli = IRCMiddleWare(loop=loop)
        cli.send = Mock()
        cli.matches = Mock(return_value = True)
        pingmsg = PingMessage("irc.example.com")
        pingmsg2 = PingMessage("irc2.example.com")
        pongmsg2 = PongMessage(pingmsg2)
        callback = Mock(return_value=pongmsg2)
        cli.on(pingmsg, callback=callback)
        loop.run_until_complete(asyncio.Task(cli.dispatch_message(pingmsg2)))
        callback.assert_called_once_with(pingmsg2)
        cli.send.assert_called_once_with(pongmsg2)

    def test_dispatch_message2(self):
        import asyncio

        loop = asyncio.get_event_loop()
        cli = IRCMiddleWare(loop=loop)
        cli.send = Mock()
        cli.matches = Mock(return_value = True)
        pingmsg = PingMessage("irc.example.com")
        pingmsg2 = PingMessage("irc2.example.com")
        pongmsg2 = Mock()
        callback = Mock(return_value=pongmsg2)
        cli.on(pingmsg, callback=callback)
        loop.run_until_complete(asyncio.Task(cli.dispatch_message(pingmsg2)))
        callback.assert_called_once_with(pingmsg2)
        self.assertEqual(0,cli.send.call_count)
