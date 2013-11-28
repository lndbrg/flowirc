from unittest import TestCase

__author__ = 'olle.lundberg'


class TestUserMessage(TestCase):
    def test_usermessage(self):
        from flowirc.messages import UserMessage
        self.assertEqual("USER bar 0 * :baz\r\n",
                         str(UserMessage("bar", "baz")))
