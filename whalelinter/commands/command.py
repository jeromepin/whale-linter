#!/usr/bin/env python3

import inspect
from whalelinter.app import App
from abc import ABC


class ShellCommand(ABC):
    _callbacks = {}

    @classmethod
    def register(cls, instance):
        def decorate(func, **kwargs):

            if 'name' not in kwargs:
                name = func.__name__
            else:
                name = kwargs.get('name')

            if (name not in cls._callbacks):
                cls._callbacks[name] = []

            # if 'args' in kwargs and name in .get(args):

            cls._callbacks[name].append({
                'instance': instance,
                'function': func,
                'kwargs'  : kwargs
            })

        return decorate

    def react(self, name):
        if name in self._callbacks:
            for callback in self._callbacks[name]:
                if (self == callback.get('instance')):
                    if callback.get('kwargs'):
                        callback.get('function')(callback.get('instance'), **callback.get('kwargs'))
                    else:
                        callback.get('function')(callback.get('instance'))


class PackageManager(ShellCommand):

    def find_packages(self):
        lst = list(self.rest)
        for arg in self.args:
            lst.remove(arg)

        subcommand = lst[0]
        lst.remove(lst[0])

        return (subcommand, lst)

    def is_parameter_present(self, **kwargs):
        if 'parameter' in kwargs and 'args' in kwargs:
            if kwargs.get('parameter') not in kwargs.get('args'):
                App._collecter.throw(2010, self.lineno, keys={
                    'parameter' : kwargs.get('parameter'),
                    'command'   : self.full_command
                })
                return False

        return True

    def __init__(self, token, command, rest, line_number):
        """
            RUN apt-get install -y name

            RUN             : token
            apt-get         : command
            install -y name  : rest

            install : subcommand
            -y      : args
            name     : packages

        """
        self.token          = token
        self.command        = command
        self.rest           = rest
        self.full_command   = self.command + ' ' + ' '.join(self.rest)

        self.args           = [arg for arg in self.rest if (arg.startswith('-') or arg.startswith('--'))]
        self.lineno         = line_number
        self.methods        = []

        self.subcommand, self.packages = self.find_packages()

        for method in inspect.getmembers(self, predicate=inspect.ismethod):
            if not method[0].startswith('__') \
                and method[0] is not 'register' \
                and method[0] is not 'find_packages' \
                and method[0] is not 'is_parameter_present' \
                and method[0] is not 'react':

                self.methods.append(method[0])
