from unittest import TestCase
from collections import OrderedDict

from flowirc.messages import MessageBase, PingMessage, JoinMessage


__author__ = 'Olle Lundberg'


class TestMessageBase(TestCase):
    def test_messagebase(self):
        args = OrderedDict(
            (('foo', 'bar'), ('foo1', 'bar1'), ('foo2', 'bar2')))
        foo = MessageBase(args)
        self.assertEqual("BASE bar bar1 bar2\r\n", str(foo))
        self.assertEqual(b"BASE bar bar1 bar2\r\n", foo.encode())

        def for_test(foo):
            foo.not_a_string_method()

        self.assertRaises(AttributeError, for_test, foo)

    def test_from_str(self):
        self.assertRaises(Exception, MessageBase.from_str, '')
        ping = "PING :irc.example.net"
        pingmsg = MessageBase.from_str(ping)
        self.assertIsInstance(pingmsg, PingMessage)
        self.assertEqual("PING irc.example.net\r\n", str(pingmsg))

        prefix = 'flowirc!~flowirc@localhost'
        join = 'JOIN :#foo'
        joinfull = ':{prefix} {join}'.format(prefix=prefix, join=join)
        joinmsg = MessageBase.from_str(joinfull)
        self.assertIsInstance(joinmsg, JoinMessage)
        self.assertEqual(prefix, joinmsg.prefix)
        self.assertEqual("JOIN #foo\r\n", str(joinmsg))

        crap = 'CRAP foo'
        crapmsg = MessageBase.from_str(crap)
        self.assertEqual(crapmsg, None)
