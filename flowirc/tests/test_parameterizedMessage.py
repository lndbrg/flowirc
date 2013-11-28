from unittest import TestCase

__author__ = 'olle.lundberg'


class TestParameterizedMessage(TestCase):
    def test_parameterizedmessage(self):
        from flowirc.messages import ParameterizedMessage
        self.assertEqual("PARAMETERIZED prefix infix suffix\r\n",
                         str(ParameterizedMessage("prefix","infix","suffix")))