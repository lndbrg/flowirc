from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock

from flowirc.client import IRCClient
from flowirc.messages import PingMessage


__author__ = 'Olle Lundberg'


class TestIRCClient(TestCase):
    def test_init_no_name(self):
        self.assertRaises(AssertionError, IRCClient)

    @patch('asyncio.get_event_loop')
    def test_init_loops(self, gel):
        IRCClient(__name__)
        self.assertEqual(1, gel.call_count)
        gel.reset_mock()
        IRCClient(__name__, loop=Mock())
        self.assertEqual(0, gel.call_count)

    def test_init_ssl_and_ports(self):
        SSL_PORT = 6697
        cli = IRCClient(__name__, port=SSL_PORT, loop=Mock())
        self.assertTrue(cli.ssl)
        cli = IRCClient(__name__, ssl=True, loop=Mock())
        self.assertEqual(SSL_PORT, cli.port)
        cli = IRCClient(__name__)
        self.assertFalse(cli.ssl)
        self.assertEqual(6667, cli.port)

    @patch('importlib.import_module')
    @patch('asyncio.Task')
    def test_run(self, task, mod_register):
        cli = IRCClient(name=__name__, loop=Mock())
        test_object = Mock()
        cli.loop.create_connection = MagicMock(return_value = test_object)
        cli.run()
        mod_register.assert_assert_called_once_with(
            'flowirc.listeners.default')
        self.assertEqual(1, cli.loop.create_connection.call_count)
        task.assert_called_once_with(test_object)

    @patch('importlib.import_module')
    @patch('asyncio.Task')
    def test_run_no_default_listeners(self, task, mod_register):
        cli = IRCClient(name=__name__, loop = Mock())
        cli.loop.create_connection = MagicMock(return_value = None)
        cli.run(False)
        self.assertEqual(0, mod_register.call_count)
        self.assertEqual(1, cli.loop.create_connection.call_count)

    def test_run_forever(self):
        cli = IRCClient(name=__name__, loop=Mock())
        cli.run = Mock()
        cli.run_forever(False)
        cli.run.assert_called_once_with(False)
        self.assertEqual(1, cli.loop.run_forever.call_count)

    def test_after_connection_made(self):
        cli = IRCClient(name=__name__, loop=Mock())
        cli.identify = Mock()
        cli.join = Mock()
        cli.after_connection_made()
        self.assertEqual(1, cli.identify.call_count)
        cli.join.assert_assert_called_once_with('#foo')

    def test_identify(self):
        cli = IRCClient(name=__name__, loop=Mock())
        cli.user = Mock()
        cli.nick = Mock()
        cli.identify()
        self.assertEqual(1, cli.user.call_count)
        self.assertEqual(1, cli.nick.call_count)

    @patch('flowirc.client.JoinMessage')
    def test_join(self, joinmessage):
        TEST_CHAN = '#FOO'
        cli = IRCClient(name=__name__, loop=Mock())
        cli.send = Mock()
        cli.join(TEST_CHAN)
        joinmessage.assert_called_once_with(TEST_CHAN)
        cli.send.assert_assert_called_once_with(joinmessage)

    @patch('flowirc.client.NickMessage')
    def test_nick_default(self, nickmessage):
        cli = IRCClient(name=__name__, loop=Mock())
        cli.send = Mock()
        cli.nick()
        nickmessage.assert_called_once_with(cli._nick)
        cli.send.assert_assert_called_once_with(nickmessage)
        self.assertEqual(cli._nick, 'flowirc')

    @patch('flowirc.client.NickMessage')
    def test_nick_constructor_nick(self, nickmessage):
        TEST_NICK = 'testnick'
        cli = IRCClient(name=__name__, nick=TEST_NICK, loop=Mock())
        cli.send = Mock()
        cli.nick()
        nickmessage.assert_called_once_with(TEST_NICK)
        cli.send.assert_assert_called_once_with(nickmessage)
        self.assertEqual(cli._nick, TEST_NICK)

    @patch('flowirc.client.NickMessage')
    def test_nick_set_nick(self, usermessage):
        TEST_NICK = 'testnick'
        cli = IRCClient(name=__name__, loop=Mock())
        cli.send = Mock()
        cli.nick(TEST_NICK)
        usermessage.assert_called_once_with(TEST_NICK)
        cli.send.assert_assert_called_once_with(usermessage)
        self.assertEqual(cli._nick, TEST_NICK)

    @patch('flowirc.client.UserMessage')
    def test_user_default(self, usermessage):
        cli = IRCClient(name=__name__, loop=Mock())
        cli.send = Mock()
        cli.user()
        usermessage.assert_called_once_with(cli._nick, cli._user)
        cli.send.assert_assert_called_once_with(usermessage)
        self.assertEqual(cli._user, 'flowirc')

    @patch('flowirc.client.UserMessage')
    def test_user_constructor_user(self, usermessage):
        TEST_USER = 'testuser'
        cli = IRCClient(name=__name__, user=TEST_USER, loop=Mock())
        cli.send = Mock()
        cli.user()
        usermessage.assert_called_once_with(cli._nick, TEST_USER)
        cli.send.assert_assert_called_once_with(usermessage)
        self.assertEqual(cli._user, TEST_USER)

    @patch('flowirc.client.UserMessage')
    def test_user_set_user(self, usermessage):
        TEST_USER = 'testuser'
        cli = IRCClient(name=__name__, loop=Mock())
        cli.send = Mock()
        cli.user(TEST_USER)
        usermessage.assert_called_once_with(cli._nick, TEST_USER)
        cli.send.assert_assert_called_once_with(usermessage)
        self.assertEqual(cli._user, TEST_USER)

    def test_listen_to(self):
        cli = IRCClient(name=__name__, loop=Mock())
        @cli.listen_to(PingMessage)
        def foo(msg):
            pass
        @cli.listen_to(PingMessage())
        def foo(msg):
            pass
