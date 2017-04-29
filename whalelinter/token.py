#!/usr/bin/env python3

from whalelinter.app import App
from whalelinter.dispatcher import Dispatcher
from whalelinter.commands.command import ShellCommand
# from whalelinter.commands.apt import Apt


class Token:
    def __init__(self, name, payload, line):
        self.name    = name
        self.payload = payload
        self.line    = line

        self.pointless_commands = App._pointless_commands


@Dispatcher.register(token='add')
class Add(Token):
    def __init__(self, payload, line):
        Token.__init__(self, __class__, payload, line)
        self.is_present()
        self.download_from_url()

    def is_present(self):
        App._collecter.throw(2006, self.line)
        return True

    def download_from_url(self):
        if ('http://' in self.payload[0] or 'https://' in self.payload[0]):
            App._collecter.throw(3004, self.line)
            return True
        return False


@Dispatcher.register(token='expose')
class Expose(Token):
    def __init__(self, ports, line):
        Token.__init__(self, __class__, ports, line)
        for port in ports:
            self.is_in_range(port)
            self.is_tcp_or_udp(port)

    def is_in_range(self, port):
        if '/' in port:
            port = port.split('/')[0]

        if int(port) < 1 or int(port) > 65535:
            App._collecter.throw(2005, self.line, keys={'port': port})
            return False
        return True

    def is_tcp_or_udp(self, port):
        if '/' in port:
            if port.split('/')[1] != 'tcp' and port.split('/')[1] != 'udp':
                App._collecter.throw(2009, self.line)
                return False
        return True


@Dispatcher.register(token='maintainer')
class Maintainer(Token):
    def __init__(self, payload, line):
        Token.__init__(self, __class__, payload, line)
        App._collecter.throw(2013, self.line, keys={'instruction': 'maintainer'})


@Dispatcher.register(token='run')
class Run(Token):
    def __init__(self, payload, line):
        payload = list(filter(None, payload))

        Token.__init__(self, __class__, payload, line)
        self.is_pointless()

        shell_command       = self.payload[0]
        shell_arguments     = self.payload[1:]
        next_command_index  = False

        if '&&' in shell_arguments:
            next_command_index  = shell_arguments.index('&&')
            next_command        = shell_arguments[(next_command_index + 1):]
            shell_arguments     = shell_arguments[:next_command_index]

        if shell_command in Dispatcher._callbacks['RUN']:
            if Dispatcher._callbacks['RUN'][shell_command]['self'] is not None:
                Dispatcher._callbacks['RUN'][shell_command]['self'](token='RUN', command=shell_command, args=shell_arguments, lineno=line)

        if next_command_index and next_command:
            self.__init__(next_command, self.line)

        return

    def is_pointless(self):
        if self.payload[0] in self.pointless_commands:
            App._collecter.throw(2003, self.line, keys={'command': self.payload[0]})
            return True
        return False


@Dispatcher.register(token='from')
class SourceImage(Token):
    def __init__(self, payload, line):
        Token.__init__(self, __class__, payload, line)
        self.is_too_long()
        self.has_no_tag()
        self.has_latest_tag()

    def is_too_long(self):
        if len(self.payload) > 1:
            App._collecter.throw(1002, self.line, keys={'command': self.payload})
            return True
        return False

    def has_no_tag(self):
        if ':' not in self.payload[0]:
            App._collecter.throw(2000, self.line, keys={'image': self.payload[0]})
            return True
        return False

    def has_latest_tag(self):
        if ':latest' in self.payload[0]:
            App._collecter.throw(2001, self.line)
            return True
        return False


@Dispatcher.register(token='user')
class User(Token):
    def __init__(self, payload, line):
        Token.__init__(self, __class__, payload, line)

    def is_becoming_root(self):
        if self.payload[0] == 'root':
            App._collecter.throw(2007, self.line)
            return True
        return False


@Dispatcher.register(token='workdir')
class Workdir(Token):
    def __init__(self, payload, line):
        Token.__init__(self, __class__, payload, line)

    def has_relative_path(self):
        if not payload[0].startswith('/'):
            App._collecter.throw(2004, self.line)
            return True
        return False
