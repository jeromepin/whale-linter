#!/usr/bin/env python3

from whalelinter.app import App
from whalelinter.dispatcher import Dispatcher
from whalelinter.commands.apt import Apt


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

    def is_present(self):
        App._collecter.throw(2006, self.line)
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


@Dispatcher.register(token='run')
class Run(Token):
    def __init__(self, payload, line):
        Token.__init__(self, __class__, payload, line)
        self.is_pointless(self.payload[0])

        # if '/var/lib/apt/lists/*' in payload:
        #     # Cache has already been cleaned
        #     self.apt_has_been_used = False

    @Dispatcher.register(token='run', command='cd')
    def cd(self, command):
        App._collecter.throw(2002, self.line)
        return False

    def is_pointless(self, command):
        if command in self.pointless_commands:
            App._collecter.throw(2003, self.line, keys={'command': command})
            return True


@Dispatcher.register(token='from')
class SourceImage(Token):
    def __init__(self, payload, line):
        Token.__init__(self, __class__, payload, line)

        if len(payload) > 1:
            App._collecter.report('CommandTooLong')

        if ':' not in payload[0]:
            App._collecter.throw(2000, self.line, keys={'image': payload[0]})

        if ':latest' in payload[0]:
            App._collecter.throw(2001, self.line)


@Dispatcher.register(token='user')
class User(Token):
    def __init__(self, payload, line):
        Token.__init__(self, __class__, payload, line)
        if payload[0] == 'root':
            App._collecter.throw(2007, self.line)


@Dispatcher.register(token='workdir')
class Workdir(Token):
    def __init__(self, payload, line):
        Token.__init__(self, __class__, payload, line)
        if not payload[0].startswith('/'):
            App._collecter.throw(2004, self.line)
