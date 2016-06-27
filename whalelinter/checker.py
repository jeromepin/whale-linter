#!/usr/bin/env python3
from whalelinter.app          import App
from whalelinter.dispatcher   import Dispatcher

class Checker(object):
    def __init__(self, dictionnary):
        self.lines              = dictionnary
        self.dispatcher         = Dispatcher(self)
        self.consecutive_run    = 0
        self.apt_has_been_used  = False

    def all(self):
        for lineno, line in self.lines.items():
            self.lineno = lineno
            self.dispatcher.react(line, self.lineno)
            self.must_be_present(line[0])
            self.must_be_unique(line[0])
            self.should_be_present(line[0])

        if self.apt_has_been_used is True:
            App._collecter.throw(3000)

        for mandatory_token in App._mandatory_tokens:
            App._collecter.throw(1000)

        for recommended_token in App._recommended_tokens:
            App._collecter.throw(3001, keys={'token': recommended_token})

    def must_be_present(self, current_token):
        if current_token in App._mandatory_tokens:
            App._mandatory_tokens.remove(current_token)

    def should_be_present(self, current_token):
        if current_token in App._recommended_tokens:
            App._recommended_tokens.remove(current_token)

    def must_be_unique(self, current_token):
        if current_token in App._unique_tokens:
            App._unique_tokens[current_token] += 1
            if App._unique_tokens[current_token] > 1:
                App._collecter.throw(1001, self.line_number, keys={'token': current_token})
