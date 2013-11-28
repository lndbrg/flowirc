from unittest import TestCase

__author__ = 'olle.lundberg'


class TestModeMessageBase(TestCase):
    def test_modemessagebase(self):
        from flowirc.messages import ModeMessageBase
        self.assertEqual("MODE channel +o bla\r\n",
                         str(ModeMessageBase("channel","+o","bla")))