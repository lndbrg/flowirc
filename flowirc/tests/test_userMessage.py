from unittest import TestCase
from flowirc.message import UserMessage


__author__ = 'Olle Lundberg'


class TestUserMessage(TestCase):
    def test_usermessage(self):
        self.assertEqual("USER bar 0 * :baz\r\n",
                         str(UserMessage("bar", "baz")))
