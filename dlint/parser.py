#!/usr/bin/env python3
import shlex
from dlint.app import App


class Parser(object):
    def __init__(self, filename):
        self.file   = open(filename, encoding='utf-8').read()
        self.TOKENS = App._config['all']

    def shlex_to_dictionnary(self):
        self.lexer                  = shlex.shlex(instream=self.file, posix=True)
        self.lexer.quotes           = '"'
        self.lexer.commenters       = '#'
        self.lexer.whitespace_split = True

        accumulator = []
        commands    = {}
        line        = 0

        for word in self.lexer:
            if word in self.TOKENS:
                if accumulator:
                    commands[line] = accumulator
                    accumulator = []

                line = self.lexer.lineno

            accumulator.append(word)

        commands[line] = accumulator

        return commands
