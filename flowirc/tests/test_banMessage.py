from unittest import TestCase

__author__ = 'olle.lundberg'


class TestBanMessage(TestCase):
    def test_banmessage(self):
        from flowirc.messages import BanMessage,ModeMessageBase
        self.assertEqual(BanMessage.type(), ModeMessageBase.type())
        self.assertEqual("MODE channel +b *!*@*\r\n",
                         str(BanMessage("channel","*!*@*")))