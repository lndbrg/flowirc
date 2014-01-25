from collections import OrderedDict
import importlib
from flowirc.log import log
from flowirc.messages.base import MessageBase


class IRCMessage(MessageBase):
    prefix = None

    def __init__(self, ordered_args):
        super().__init__()
        self._fields = ordered_args.keys()
        self._asdict = ordered_args

    def __str__(self):
        result_string = ' '.join(['{type}',
                                  ''.join(['{{{f}}}'.format(f=field)
                                           if self._asdict[field].endswith(":")
                                           else '{{{f}}} '.format(f=field)
                                           for field in self._fields
                                           if self._asdict[field]])])

        return ''.join([result_string.rstrip().format(type=self.type(),
                                                      **self._asdict),
                        '\r\n'])

    def __getattr__(self, attr):
        return getattr(str(self), attr)

    @classmethod
    def from_str(cls, string):
        prefix = ''
        trailing = []
        if not string:
            raise Exception("Empty line.")
        if string[0] == ':':
            prefix, string = string[1:].split(' ', 1)
        if string.find(' :') != -1:
            string, trailing = string.split(' :', 1)
            args = string.split()
            args.append(trailing)
        else:
            args = string.split()
        command = args.pop(0)
        module = importlib.import_module(__name__)
        try:
            class_ = getattr(module, '{command}Message'.
            format(command=command.capitalize()))
            del module
            log.debug("Creating %s with args %s", class_, args)
            msg = class_(*args)
            msg.prefix = prefix
            return (msg)
        except AttributeError:
            log.warning("Message creation failed for: %s" % string)
            pass
        return None

class ParameterizedMessage(IRCMessage):
    def __init__(self, *parameters):

        parameters = list(parameters)
        trailing = parameters.pop()
        parameters = [str(param) for param in parameters
                      if param is not None]

        if len(parameters) > 0:
            parameters = " ".join(parameters)
            if trailing is not None:
                trailing = ':{trailing}'.format(trailing=trailing)
        ordered_args = OrderedDict()
        ordered_args['middle'] = parameters
        ordered_args['trailing'] = trailing
        super().__init__(ordered_args)


class ModeMessageBase(ParameterizedMessage):
    _type = 'MODE'

    def __init__(self, channel=None, mode=None, user=None):
        if mode is None:
            mode = self._mode
        super().__init__(channel, mode, user, None)


class ModeMessage(ModeMessageBase):
    _mode = None

    def __init__(self, channel=None, user=None):
        super().__init__(channel=channel, user=user)


class BanMessage(ModeMessage):
    _mode = '+b'


class UserMessage(ParameterizedMessage):
    def __init__(self, user=None, full_name=None, mode=0):
        super().__init__(user, mode, '*', full_name)


class QuitMessage(ParameterizedMessage):
    _message = "Good bye my friend it's hard to die!"

    def __init__(self, message=None):
        if message is None:
            message = self._message
        super().__init__('', message)


class SimpleMessage(ParameterizedMessage):
    def __init__(self, trailing=None):
        super().__init__(trailing)


class NickMessage(SimpleMessage):
    pass


class JoinMessage(SimpleMessage):
    pass


class PartMessage(SimpleMessage):
    pass


class PingMessage(SimpleMessage):
    pass


class PongMessage(SimpleMessage):
    def __init__(self, msg):
        print(msg)
        sender = msg.split()[-1]
        super().__init__(sender)
