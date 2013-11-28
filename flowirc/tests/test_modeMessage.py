from unittest import TestCase

__author__ = 'olle.lundberg'


class TestModeMessage(TestCase):
    def test_modemessage(self):
        from flowirc.messages import ModeMessage
        self.assertEqual("MODE channel bla\r\n",
                     str(ModeMessage("channel", "bla")))
