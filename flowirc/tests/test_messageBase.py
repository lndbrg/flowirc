from unittest import TestCase

__author__ = 'olle.lundberg'


class TestMessageBase(TestCase):
    def test_messagebase(self):
        from collections import OrderedDict
        from flowirc.messages import MessageBase
        args = OrderedDict((('foo','bar'),('foo1','bar1'),('foo2','bar2')))
        foo = MessageBase(args)
        self.assertEqual("BASE bar bar1 bar2\r\n",str(foo))