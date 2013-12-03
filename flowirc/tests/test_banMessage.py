from unittest import TestCase
from flowirc.messages import BanMessage, ModeMessageBase

__author__ = 'olle.lundberg'


class TestBanMessage(TestCase):
    def test_banmessage(self):
        self.assertEqual(BanMessage.type(), ModeMessageBase.type())
        self.assertEqual("MODE channel +b *!*@*\r\n",
                         str(BanMessage("channel", "*!*@*")))
