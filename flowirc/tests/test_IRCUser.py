from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock

from flowirc.user import IRCUser


__author__ = 'Olle Lundberg'


class TestIRCUser(TestCase):
    def test_init_no_name(self):
        bot = IRCUser()
        self.assertEqual('test_IRCUser a Flowirc bot', bot.full_name)

    def test_init_no_name_with_main_mod(self):
        inspect_mod = Mock()
        inspect_mod.stack.return_value = MagicMock()
        mocked_module = MagicMock()
        mocked_module.__name__ = '__main__'
        mocked_module.__file__ = 'foo/bar.py'
        inspect_mod.getmodule.return_value = mocked_module
        bot = None
        with patch.dict('sys.modules', inspect=inspect_mod):
            bot = IRCUser()

        self.assertEqual('bar a Flowirc bot', bot.full_name)

    @patch('flowirc.user.NickMessage')
    def test_nick_default(self, nickmessage):
        cli = IRCUser()
        cli.send = Mock()
        nickmessage.assert_called_once_with(cli.nick)
        cli.send.assert_assert_called_once_with(nickmessage)
        self.assertEqual(cli.nick, 'flowirc')

    @patch('flowirc.user.NickMessage')
    def test_nick_constructornick(self, nickmessage):
        TEST_NICK = 'TEST_NICK'
        cli = IRCUser(full_name=__name__, nick=TEST_NICK)
        cli.send = Mock()
        nickmessage.assert_called_once_with(TEST_NICK)
        cli.send.assert_assert_called_once_with(nickmessage)
        self.assertEqual(cli.nick, TEST_NICK)

    @patch('flowirc.user.NickMessage')
    def test_nick_setnick(self, usermessage):
        TEST_NICK = 'TEST_NICK'
        cli = IRCUser()
        cli.send = Mock()
        cli.nick = TEST_NICK
        usermessage.assert_called_once_with(TEST_NICK)
        cli.send.assert_assert_called_once_with(usermessage)
        self.assertEqual(cli.nick, TEST_NICK)


    @patch('flowirc.user.UserMessage')
    def test_user_default(self, usermessage):
        cli = IRCUser()
        cli.send = Mock()
        cli.user
        usermessage.assert_called_once_with(cli.user, cli.full_name)
        cli.send.assert_assert_called_once_with(usermessage)
        self.assertEqual(cli.user, 'flowirc')

    @patch('flowirc.user.UserMessage')
    def test_user_constructoruser(self, usermessage):
        TEST_USER = 'TEST_USER'
        cli = IRCUser(user=TEST_USER)
        cli.send = Mock()
        cli.user
        usermessage.assert_called_once_with(TEST_USER, cli.full_name)
        cli.send.assert_assert_called_once_with(usermessage)
        self.assertEqual(cli.user, TEST_USER)

    @patch('flowirc.user.UserMessage')
    def test_user_setuser(self, usermessage):
        TEST_USER = 'TEST_USER'
        cli = IRCUser(full_name=__name__)
        cli.send = Mock()
        cli.user = TEST_USER
        usermessage.assert_called_once_with(TEST_USER, cli.full_name)
        cli.send.assert_assert_called_once_with(usermessage)
        self.assertEqual(cli.user, TEST_USER)
