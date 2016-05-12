#!/usr/bin/env python3
from whalelinter.app          import App
from whalelinter.dispatcher   import Dispatcher
from whalelinter.commands.apt import Apt


class Checker(object):
    def __init__(self, dictionnary):
        self.lines              = dictionnary
        self.dispatcher         = Dispatcher(self)
        self.consecutive_run    = 0
        self.apt_has_been_used  = False
        self.mandatory_tokens   = App._config['mandatory']
        self.recommended_tokens = App._config['recommended']
        self.pointless_commands = App._config['pointless_commands']
        self.unique_tokens      = {x: 0 for x in App._config['unique']}

    def all(self):
        for lineno, line in self.lines.items():
            self.lineno = lineno
            self.dispatcher.react(line, self.lineno)
            self.must_be_present(line[0])
            self.must_be_unique(line[0])
            self.should_be_present(line[0])

        if self.apt_has_been_used is True:
            App._collecter.throw(3000)

        for mandatory_token in self.mandatory_tokens:
            App._collecter.throw(1000)

        for recommended_token in self.recommended_tokens:
            App._collecter.throw(3001, keys={'token': recommended_token})

    def must_be_present(self, current_token):
        if current_token in self.mandatory_tokens:
            self.mandatory_tokens.remove(current_token)

    def should_be_present(self, current_token):
        if current_token in self.recommended_tokens:
            self.recommended_tokens.remove(current_token)

    def must_be_unique(self, current_token):
        if current_token in self.unique_tokens:
            self.unique_tokens[current_token] += 1
            if self.unique_tokens[current_token] > 1:
                App._collecter.throw(1001, self.lineno, keys={'token': current_token})

    @Dispatcher.register(token='from')
    def source_image(self, command):
        if len(command) > 1:
            App._collecter.report('CommandTooLong')

        if ':' not in command[0]:
            App._collecter.throw(2000, self.lineno, keys={'image': command[0]})

        if ':latest' in command[0]:
            App._collecter.throw(2001, self.lineno)

    @Dispatcher.register(token='run')
    def run(self, command):
        @Dispatcher.register(token='run', command='cd')
        def cd(self, command):
            App._collecter.throw(2002, self.lineno)

        if command[0] == 'apt' or command[0] == 'apt-get':
            apt = Apt()

        if '/var/lib/apt/lists/*' in command:
            # Cache has already been cleaned
            self.apt_has_been_used = False

        if command[0] in self.pointless_commands:
            App._collecter.throw(2003, self.lineno, keys={'command': command[0]})

    @Dispatcher.register(token='workdir')
    def workdir(self, command):
        if not command[0].startswith('/'):
            App._collecter.throw(2004, self.lineno)

    @Dispatcher.register(token='expose')
    def expose(self, ports):
        for port in ports:
            if int(port) < 1 or int(port) > 65535:
                App._collecter.throw(2005, self.lineno, keys={'port': port})

    @Dispatcher.register(token='add')
    def add(self, command):
        App._collecter.throw(2006, self.lineno)

    @Dispatcher.register(token='user')
    def user(self, command):
        if command[0] == 'root':
            App._collecter.throw(2007, self.lineno)
