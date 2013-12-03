from unittest import TestCase, expectedFailure
from collections import OrderedDict

from flowirc.messages import MessageBase, PingMessage, JoinMessage


__author__ = 'olle.lundberg'


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

    @expectedFailure
    def test_from_str(self):
        self.assertRaises(Exception, MessageBase.from_str, '')
        ping = "PING :irc.example.net"
        pingmsg = MessageBase.from_str(ping)
        self.assertIsInstance(pingmsg, PingMessage)
        self.assertEqual(ping,str(pingmsg))

        join = ':flowirc!~flowirc@localhost JOIN :#foo'
        joinmsg = MessageBase.from_str(join)
        self.assertIsInstance(joinmsg, JoinMessage)
        self.assertEqual(join, str(joinmsg))

        crap = 'CRAP foo'
        crapmsg = MessageBase.from_str(crap)
        self.assertEqual(crapmsg, None)
