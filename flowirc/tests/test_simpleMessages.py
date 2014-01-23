from unittest import TestCase

from flowirc.messages import *

__author__ = 'Olle Lundberg'


class TestSimpleMessages(TestCase):
    def test_nickmessage(self):
        self.assertEqual("NICK bar\r\n", str(NickMessage("bar")))

    def test_joinmessage(self):
        self.assertEqual("JOIN bar\r\n", str(JoinMessage("bar")))

    def test_partmessage(self):
        self.assertEqual("PART bar\r\n", str(PartMessage("bar")))

    def test_pingmessage(self):
        self.assertEqual("PING irc.example.net\r\n",
                         str(PingMessage("irc.example.net")))

    def test_pongmessage(self):
        ping = PingMessage("irc.example.net")
        self.assertEqual("PONG irc.example.net\r\n",
                         str(PongMessage(ping)))
