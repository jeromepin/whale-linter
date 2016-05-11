#!/usr/bin/env python3
from dlint.app import App

FUNCTION_CHAR = '_'


class Dispatcher:
    _callbacks = {}

    def __init__(self, caller=None):
        self.caller          = caller
        self.consecutive_run = {
            'count': 0,
            'line' : 0
        }

    def separate_multiline_commands(self, command):
        rest              = None
        chain_idx         = 10000
        newline_chain_idx = 10000

        if '&&' in command:
            chain_idx = command.index('&&')

        if '\n&&' in command:
            newline_chain_idx = command.index('\n&&')

        idx     = chain_idx if chain_idx < newline_chain_idx else newline_chain_idx
        rest    = command[idx + 1:]
        command = command[:idx]

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
            args, rest = self.separate_multiline_commands(args)

        if token in self._callbacks:
            self._callbacks[token][FUNCTION_CHAR](self.caller, args)

            if token == 'run':
                self.consecutive_run['count'] += 1
                self.consecutive_run['line']   = lineno
            else:
                self.consecutive_run['count'] = 0

            command = args[0]
            args = args[1:]

            if command in self._callbacks[token]:

                if self._callbacks[token][command][FUNCTION_CHAR] is not None:
                    self._callbacks[token][command][FUNCTION_CHAR](self.caller, args)

                subcommand = args[0]
                args = args[1:]

                if subcommand in self._callbacks[token][command]:
                    self._callbacks[token][command][subcommand][FUNCTION_CHAR](self.caller, args)

        if self.consecutive_run['count'] > 1:
            App._collecter.throw(2012, self.consecutive_run['line'])

        if is_multiline_command and rest:
            rest.insert(0, 'RUN')
            self.consecutive_run['count'] = 0
            self.react(rest)

    @classmethod
    def register(cls, func=None, token=None, command=None, subcommand=None):
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
        if hasattr(func, '__call__'):
            token = func.__name__

        if token:
            if token not in cls._callbacks:
                cls._callbacks[token] = {
                    FUNCTION_CHAR: None,
                }

            if command:
                if command not in cls._callbacks[token]:
                    cls._callbacks[token][command] = {
                        FUNCTION_CHAR: None,
                    }

                if subcommand:
                    if subcommand not in cls._callbacks[token][command]:
                        cls._callbacks[token][command][subcommand] = {
                            FUNCTION_CHAR: None,
                        }

        if token and command and subcommand:
            def decorate(func):
                cls._callbacks[token][command][subcommand][FUNCTION_CHAR] = func
                return func

        if token and command and not subcommand:
            def decorate(func):
                cls._callbacks[token][command][FUNCTION_CHAR] = func

                return func

        if token and not command and not subcommand:

            def decorate(func):
                cls._callbacks[token][FUNCTION_CHAR] = func

                return func

        return decorate
