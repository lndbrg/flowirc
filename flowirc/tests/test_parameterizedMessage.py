from unittest import TestCase
from flowirc.messages import ParameterizedMessage


__author__ = 'Olle Lundberg'


class TestParameterizedMessage(TestCase):
    def test_parameterizedmessage(self):
        self.assertEqual("PARAMETERIZED foo bar :baz\r\n",
                         str(ParameterizedMessage("foo", "bar", "baz")))
