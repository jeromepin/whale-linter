#!/usr/bin/env python3
import shlex
import operator
import re
import urllib.request
import os
from whalelinter.app import App


class Parser(object):
    def __init__(self, filename):
        if self.is_url(filename) is not None:
            response = urllib.request.urlopen(filename)
            if self.is_content_type_plain_text(response):
                self.file = response.read().decode('utf-8')
            else:
                print('ERROR: file format not supported\n')
        elif os.path.isfile(filename):
            self.file = open(filename, encoding='utf-8').read()
        elif self.is_github_repo(filename):
            filename = 'https://raw.githubusercontent.com/' + filename + '/master/Dockerfile'
            self.file = urllib.request.urlopen(filename).read().decode('utf-8')
        else:
            print('ERROR: file format not supported\n')

        self.TOKENS = App._config.get('all')

    def is_github_repo(self, filename):
        regex = re.compile(r'^[-_.0-9a-z]+/[-_.0-9a-z]+$', re.IGNORECASE)

        return True if regex.match(filename) is not None else False

    def is_url(self, filename):
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return regex.match(filename)

    def is_content_type_plain_text(self, response):
        content_type = response.getheader('Content-Type')
        regex        = re.compile(r'text/plain')

        return True if regex.search(content_type) is not None else False

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

        return sorted(commands.items(), key=operator.itemgetter(0))
