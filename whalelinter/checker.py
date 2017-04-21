#!/usr/bin/env python3
from whalelinter.app          import App
from whalelinter.dispatcher   import Dispatcher
from whalelinter.token        import Maintainer
from whalelinter.commands.apt import Apt

import whalelinter.commands.common


class Checker(object):
    def __init__(self, lst):
        self.lines              = lst
        self.line_number        = 0
        self.consecutive_run    = 0

    def check(self):
        dispatcher = Dispatcher()

        for line in self.lines:
            dispatcher.react(line)
            self.must_be_present(line.instruction)
            self.must_be_unique(line.instruction)
            self.should_be_present(line.instruction)

        if Apt._has_been_used:
            App._collecter.throw(3000, keys={'line': Apt._has_been_used})

        for mandatory_token in App._mandatory_tokens:
            App._collecter.throw(1000, keys={'token': mandatory_token})

        for recommended_token in App._recommended_tokens:
            App._collecter.throw(3001, keys={'token': recommended_token})

    def must_be_present(self, instruction):
        if instruction in App._mandatory_tokens:
            App._mandatory_tokens.remove(instruction)

    def should_be_present(self, instruction):
        if instruction in App._recommended_tokens:
            App._recommended_tokens.remove(instruction)

    def must_be_unique(self, instruction):
        if instruction in App._unique_tokens:
            App._unique_tokens[instruction] += 1
            if App._unique_tokens[instruction] > 1:
                App._collecter.throw(1001, self.line_number, keys={'token': instruction})
