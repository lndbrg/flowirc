from unittest import TestCase
from flowirc.messages import ParameterizedMessage


__author__ = 'Olle Lundberg'


class TestParameterizedMessage(TestCase):
    def test_parameterizedmessage(self):
        self.assertEqual("PARAMETERIZED prefix infix suffix\r\n",
                         str(ParameterizedMessage("prefix", "infix",
                                                  "suffix")))
