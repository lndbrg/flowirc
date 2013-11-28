from collections import OrderedDict
import importlib
import inspect


class MessageBase:
    _type = None

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

    @classmethod
    def type(cls):
        return cls._type if cls._type \
            else cls.__name__.upper().replace('MESSAGE', '')

    def __getattr__(self, attr):
        if hasattr(str, attr):
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
            print(args)
            print("CREATING {} with args {}".format(class_, args))
            msg = class_(*args)
            return (msg)
        except AttributeError:
            pass
        return None


        #return prefix, command, args


class ParameterizedMessage(MessageBase):
    def __init__(self, prefix=None, infix=None, suffix=None):
        frame = inspect.currentframe()
        args, _, _, kwargs = inspect.getargvalues(frame)
        del frame
        ordered_args = OrderedDict(((arg, kwargs[arg]) for arg in args[1:]))
        super().__init__(ordered_args)


class ModeMessageBase(ParameterizedMessage):
    _type = 'MODE'

    def __init__(self, channel=None, mode=None, user=None):
        if mode is None:
            mode = self._mode
        super().__init__(channel, mode, user)


class ModeMessage(ModeMessageBase):
    _mode = None

    def __init__(self, channel=None, user=None):
        super().__init__(channel=channel, user=user)


class BanMessage(ModeMessage):
    _mode = '+b'


class UserMessage(ParameterizedMessage):
    _infix = '0 * :'

    def __init__(self, nick=None, name=None):
        super().__init__(nick, self._infix, name)


class QuitMessage(ParameterizedMessage):
    _infix = ':'
    _message = "Good bye my friend it's hard to die!"

    def __init__(self, message=None):
        if message is None:
            message = self._message
        super().__init__(infix=self._infix, suffix=message)


class SimpleMessage(ParameterizedMessage):
    def __init__(self, param=None):
        super().__init__(param)


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
        sender = msg.split()[1]
        super().__init__(sender)