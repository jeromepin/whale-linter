#!/usr/bin/env python3
from whalelinter.app import App

FUNCTION_CHAR = '_'
from whalelinter.utils import DockerfileCommand


class Dispatcher:
    _callbacks = {}

    def __init__(self):
        self.consecutive_run = {
            'count': 0,
            'line' : 0
        }

    def react(self, docker_command):
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
        if (self._callbacks[docker_command.instruction]['self'] is not None):
            self._callbacks[docker_command.instruction]['self'](docker_command.arguments, docker_command.line)

        if docker_command.instruction == 'RUN':
            self.consecutive_run['count'] += 1
            self.consecutive_run['line']  = docker_command.line
        else:
            self.consecutive_run['count'] = 0

        if self.consecutive_run.get('count') > 1:
            App._collecter.throw(2012, self.consecutive_run.get('line'))



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
