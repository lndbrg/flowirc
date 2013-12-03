from unittest import TestCase
from flowirc.messages import BanMessage, ModeMessageBase

__author__ = 'Olle Lundberg'


class TestBanMessage(TestCase):
    def test_banmessage(self):
        self.assertEqual(BanMessage.type(), ModeMessageBase.type())
        self.assertEqual("MODE channel +b *!*@*\r\n",
                         str(BanMessage("channel", "*!*@*")))
