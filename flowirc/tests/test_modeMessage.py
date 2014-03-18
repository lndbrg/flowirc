from unittest import TestCase

__author__ = 'Olle Lundberg'


class TestModeMessage(TestCase):
    def test_modemessage(self):
        from flowirc.message import ModeMessage

        self.assertEqual("MODE channel bla\r\n",
                         str(ModeMessage("channel", "bla")))
