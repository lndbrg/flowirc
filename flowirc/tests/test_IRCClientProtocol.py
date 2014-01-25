from unittest import TestCase
from unittest.mock import Mock, patch, call, MagicMock
from flowirc.protocol import IRCClientProtocol


__author__ = 'Olle Lundberg'


class TestIRCClientProtocol(TestCase):
    def setUp(self):
        self.proto = IRCClientProtocol()
        self.transport = Mock()
        self.proto.message_received = Mock()

    def tearDown(self):
        self.proto = None
        self.transport = None

    def test_connection_made(self):
        self.proto.after_connection_made = Mock()
        self.proto.connection_made(self.transport)
        self.assertEqual(self.proto._transport, self.transport)
        self.assertEqual(1, self.proto.after_connection_made.call_count)
        self.assertEqual((), self.proto.after_connection_made.call_args)

    def test_send(self):
        self.proto._transport = Mock()
        self.proto.send('foo')
        self.proto._transport.write.assert_called_once_with(b'foo')

        self.proto._transport.reset_mock()

        calls = [call(b'foo'), call(b'bar'), call(b'baz')]
        self.proto.send('foo', 'bar', 'baz')
        self.assertEqual(3, self.proto._transport.write.call_count)
        self.proto._transport.write.assert_has_calls(calls)

        self.proto._transport.reset_mock()
        data = Mock()
        data.encode = Mock(side_effect=AttributeError(
            "'NoneType' object has no attribute 'encode'"))
        self.assertRaises(AttributeError, self.proto.send, data)

    @patch('asyncio.Task')
    @patch('flowirc.protocol.IRCMessage')
    def test_data_received(self, ircmessage, task):
        self.proto.message_received = Mock()
        self.proto.data_received(b'')
        self.proto.data_received(b'f')
        self.assertEqual(0, task.call_count)

        self.proto.data_received(b'foo')
        self.assertEqual(1, ircmessage.from_str.call_count)
        self.assertEqual(1, self.proto.message_received.call_count)

    @patch('asyncio.Task')
    @patch('flowirc.protocol.IRCMessage')
    def test_data_received_2(self, ircmessage, task):
        self.proto.message_received = Mock()
        ping = "PING irc.example.net\r\n"
        mock = MagicMock(return_value=ping)
        ircmessage.from_str = mock
        self.proto.data_received(b' \r\nPING :irc.example.net\r\n')
        self.assertEqual(1, ircmessage.from_str.call_count)
        self.proto.message_received.assert_called_once_with(ping)


    @patch('asyncio.Task')
    @patch('flowirc.protocol.IRCMessage')
    def test_data_received_3(self, ircmessage, task):
        self.proto.message_received = Mock()
        mock = MagicMock(return_value=None)
        ircmessage.from_str = mock
        self.proto.data_received(b' \r\nNOT_A_CMD :irc.example.net\r\n')
        self.assertEqual(1, ircmessage.from_str.call_count)
        self.assertEqual(0, self.proto.message_received.call_count)

