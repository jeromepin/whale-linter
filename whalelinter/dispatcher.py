#!/usr/bin/env python3
from whalelinter.app import App
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
                'self': func(self.caller, args), # represents the 'run' function
                'apt-get' = {
                    'self': func(self.caller, args),
                    'install' = {
                        'self': func(self.caller, args),
                    },
                    'upgrade' = {
                        'self': func(self.caller, args),
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
            cls._callbacks = {x.upper(): {'self': None, } for x in App._config.get('all')}

        if hasattr(func, '__call__'):
            token = func.__name__

        token = token.upper()

        if token and command:
            if command not in cls._callbacks[token]:
                cls._callbacks[token][command] = {
                    'self': None,
                }

        if token and command:
            def decorate(func):
                cls._callbacks[token][command]['self'] = func

                return func

        if token and not command:

            def decorate(func):
                cls._callbacks[token]['self'] = func

                return func

        return decorate
