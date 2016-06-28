#!/usr/bin/env python3
from whalelinter.app                import App
from whalelinter.dispatcher         import Dispatcher
from whalelinter.commands.command   import Command
from whalelinter.commands.apt       import Apt


@Dispatcher.register(token='run', command='cd')
class Cd(Command):
    def __init__(self, **kwargs):
        App._collecter.throw(2002, self.line)
        return False


@Dispatcher.register(token='run', command='rm')
class Rm(Command):
    def __init__(self, **kwargs):
        if (
            '-rf' in kwargs.get('args') or
            '-fr' in kwargs.get('args') or
            ('-r' in kwargs.get('args') and '-f' in kwargs.get('args'))
            ) and ('/var/lib/apt/lists' in kwargs.get('args')):

            if (int(Apt._has_been_used) < int(kwargs.get('lineno'))):
                Apt._has_been_used = 0
