#!/usr/bin/env python3
import re

from whalelinter.app                import App
from whalelinter.dispatcher         import Dispatcher
from whalelinter.commands.command   import ShellCommand
from whalelinter.commands.apt       import Apt


@Dispatcher.register(token='run', command='cd')
class Cd(ShellCommand):
    def __init__(self, **kwargs):
        App._collecter.throw(2002, self.line)
        return False


@Dispatcher.register(token='run', command='rm')
class Rm(ShellCommand):
    def __init__(self, **kwargs):
        rf_flags_regex    = re.compile("(-.*[rRf].+-?[rRf]|-[rR]f|-f[rR])")
        rf_flags          = True if [i for i in kwargs.get('args') if rf_flags_regex.search(i)] else False
        cache_path_regex  = re.compile("/var/lib/apt/lists(\/\*?)?")
        cache_path        = True if [i for i in kwargs.get('args') if cache_path_regex.search(i)] else False

        if rf_flags and cache_path:
            if (int(Apt._has_been_used) < int(kwargs.get('lineno'))):
                Apt._has_been_used = 0
