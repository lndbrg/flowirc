from flowirc.message.irc import UserMessage, NickMessage
from flowirc.middleware import MiddleWareBase

__author__ = 'Olle Lundberg'


class _BaseDescriptor:
    def __init__(self, what):
        self._what = what

    def __get__(self, obj, objtype):
        return self._what

    def __set__(self, obj, val):
        if self._should_send(val):
            self._what = val
            message = self._message(
                *[getattr(obj, field) for field in self._fields])
            obj.trigger(message)

    def _should_send(self, val):
        return val is not None


class _Nick(BaseDescriptor):
    _message = NickMessage
    _fields = ['nick']


class _User(BaseDescriptor):
    _message = UserMessage
    _fields = ['user', 'full_name']

_FullName = _User


class IRCUser(MiddleWareBase):
    _full_name_template = "{name} a Flowirc bot"
    nick = _Nick('flowirc')
    user = _User('flowirc')
    full_name = _FullName(None)

    def __init__(self, full_name=None, user="flowirc", nick="flowirc"):

        if full_name is None:
            import inspect

            form = inspect.stack()[1]
            module = inspect.getmodule(form[0])
            full_name = module.__name__
            if full_name == '__main__':
                import os

                full_name = os.path.splitext(
                    os.path.basename(
                        module.__file__))[0]
            else:
                _, _, full_name = full_name.rpartition('.')
            del module
            del form

        self.nick = nick
        self.full_name = self._full_name_template.format(name=full_name)
        self.user = user
