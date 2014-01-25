from unittest import TestCase
from collections import OrderedDict

from flowirc.messages import IRCMessage, PingMessage, JoinMessage


__author__ = 'Olle Lundberg'


class TestIRCMessage(TestCase):
    def test_IRCMessage(self):
        args = OrderedDict(
            (('foo', 'bar'), ('foo1', 'bar1'), ('foo2', 'bar2')))
        foo = IRCMessage(args)
        self.assertEqual("IRC bar bar1 bar2\r\n", str(foo))
        self.assertEqual(b"IRC bar bar1 bar2\r\n", foo.encode())

        def for_test(foo):
            foo.not_a_string_method()

        self.assertRaises(AttributeError, for_test, foo)

    def test_from_str(self):
        self.assertRaises(Exception, IRCMessage.from_str, '')
        ping = "PING :irc.example.net"
        pingmsg = IRCMessage.from_str(ping)
        self.assertIsInstance(pingmsg, PingMessage)
        self.assertEqual("PING irc.example.net\r\n", str(pingmsg))

        prefix = 'flowirc!~flowirc@localhost'
        join = 'JOIN :#foo'
        joinfull = ':{prefix} {join}'.format(prefix=prefix, join=join)
        joinmsg = IRCMessage.from_str(joinfull)
        self.assertIsInstance(joinmsg, JoinMessage)
        self.assertEqual(prefix, joinmsg.prefix)
        self.assertEqual("JOIN #foo\r\n", str(joinmsg))

        crap = 'CRAP foo'
        crapmsg = IRCMessage.from_str(crap)
        self.assertEqual(crapmsg, None)
