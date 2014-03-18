from unittest import TestCase

from flowirc.message import QuitMessage

__author__ = 'Olle Lundberg'


class TestQuitMessage(TestCase):
    def test_quitmessage(self):
        self.assertEqual("QUIT :Good bye my friend it's hard to die!\r\n",
                         str(QuitMessage()))
        self.assertEqual("QUIT :Bye!!\r\n", str(QuitMessage("Bye!!")))
