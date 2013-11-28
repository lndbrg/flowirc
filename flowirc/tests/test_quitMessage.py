from unittest import TestCase

__author__ = 'olle.lundberg'


class TestQuitMessage(TestCase):
    def test_quitmessage(self):
        from flowirc.messages import QuitMessage
        self.assertEqual("QUIT :Good bye my friend it's hard to die!\r\n",str(QuitMessage()))