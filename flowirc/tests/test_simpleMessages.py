from unittest import TestCase

__author__ = 'olle.lundberg'


class TestSimpleMessages(TestCase):
    def test_nickmessage(self):
        from flowirc.messages import NickMessage
        self.assertEqual("NICK bar\r\n",str(NickMessage("bar")))

    def test_joinmessage(self):
        from flowirc.messages import JoinMessage
        self.assertEqual("JOIN bar\r\n",str(JoinMessage("bar")))

    def test_partmessage(self):
        from flowirc.messages import PartMessage
        self.assertEqual("PART bar\r\n",str(PartMessage("bar")))

    def test_pingmessage(self):
        from flowirc.messages import PingMessage
        self.assertEqual("PING irc.example.net\r\n",str(PingMessage("irc.example.net")))