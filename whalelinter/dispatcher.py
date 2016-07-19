#!/usr/bin/env python3
from whalelinter.app import App

FUNCTION_CHAR = '_'


class Dispatcher:
    _callbacks = {}

    def __init__(self):
        self.consecutive_run = {
            'count': 0,
            'line' : 0
        }

    def process_chained_commands(self, command):
        idx, is_newline = self.find_first_command_chaining_symbol(command)

        rest    = command[idx + 1:]
        command = command[:idx]

        if rest[0] == '\n':
            del rest[0]

        if rest[0].startswith('\n'):
            rest[0] = rest[0][1:]

        return (command, rest, is_newline)

    def find_first_command_chaining_symbol(self, command):
        is_newline  = False
        logical_AND = next((x for x in command if x == '&&'), None)
        idx         = command.index(logical_AND) if logical_AND else 0

        if idx and (
            command[idx - 1] == '\n' or \
            command[idx + 1] == '\n' or \
            '\n' in command[idx - 1] or \
            '\n' in command[idx + 1]):

            is_newline = True

        logical_AND = next((x for x in command if x == '\n&&'), None)
        if logical_AND :
            if idx > 0:
                if command.index(logical_AND) < idx:
                    idx        = command.index(logical_AND)
                    is_newline = True
            else:
                idx        = command.index(logical_AND)
                is_newline = True

        return (idx, is_newline)


    def react(self, docker_command, lineno=None):
        """
        When a command is identified, find the corresponding callback and
        let it handle the command.

        self._callbacks = {
            'run' = {
                '_': func(self.caller, args), # represents the 'run' function
                'apt-get' = {
                    '_': func(self.caller, args),
                    'install' = {
                        '_': func(self.caller, args),
                    },
                    'upgrade' = {
                        '_': func(self.caller, args),
                    }
                }
            }
        }

        """
        rest = False
        token, args = docker_command[0].lower(), docker_command[1:]

        if '&&' in args or '\n&&' in args:
            args, rest, is_multiline_command = self.process_chained_commands(args)

        if token in self._callbacks:
            if (self._callbacks[token][FUNCTION_CHAR] is not None):
                self._callbacks[token][FUNCTION_CHAR](args, lineno)

            if token == 'run':
                self.consecutive_run['count'] += 1
                self.consecutive_run['line']   = lineno
            else:
                self.consecutive_run['count'] = 0

            command = args[0]
            args = args[1:]

            if command in self._callbacks[token]:

                if self._callbacks[token][command][FUNCTION_CHAR] is not None:
                    self._callbacks[token][command][FUNCTION_CHAR](token=token, command=command, args=args, lineno=lineno)

        if self.consecutive_run.get('count') > 1:
            App._collecter.throw(2012, self.consecutive_run.get('line'))

        if rest:
            if is_multiline_command:
                lineno += 1

            rest.insert(0, 'RUN')
            self.consecutive_run['count'] = 0
            self.react(rest, lineno)

    @classmethod
    def register(cls, func=None, token=None, command=None):
        """
        Decorator to register a new callback.

        A callback should have the same name as its corresponding command.
        It takes an instance of the calling Dispatcher object as its first
        argument and may accept an arbitrary number of positional arguments.
        If the decorated function contains a 'name' argument, the callback
        will be registered with this name instead of the function one.

        @Dispatcher.register(token='my_command', command='foo', subcommand='bar')
        def my_command_foo_bar(self, args):
        """

        if (not cls._callbacks):
            cls._callbacks = {x.lower(): {FUNCTION_CHAR: None, } for x in App._config.get('all')}

        if hasattr(func, '__call__'):
            token = func.__name__

        if token and command:
            if command not in cls._callbacks[token]:
                cls._callbacks[token][command] = {
                    FUNCTION_CHAR: None,
                }

        if token and command:
            def decorate(func):
                cls._callbacks[token][command][FUNCTION_CHAR] = func

                return func

        if token and not command:

            def decorate(func):
                cls._callbacks[token][FUNCTION_CHAR] = func

                return func

        return decorate
