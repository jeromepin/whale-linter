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
        logical_AND_index         = 10000
        logical_AND_newline_index = 10000

        if '&&' in command:
            logical_AND_index = command.index('&&')

        if '\n&&' in command:
            logical_AND_newline_index = command.index('\n&&')

        if logical_AND_newline_index < logical_AND_index:
            logical_AND_index = logical_AND_newline_index

        rest    = command[logical_AND_index + 1:]
        command = command[:logical_AND_index]

        return (command, rest)

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
        is_multiline_command = False
        token, args = docker_command[0].lower(), docker_command[1:]

        if '&&' in args or '\n&&' in args:
            is_multiline_command = True
            args, rest = self.process_chained_commands(args)

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

        if is_multiline_command and rest:
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
