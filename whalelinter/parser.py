#!/usr/bin/env python3
import re
import urllib.request
import os

from dockerfile_parse import DockerfileParser

from whalelinter.app import App
from whalelinter.utils import DockerfileCommand


class Parser(DockerfileParser):
    def __init__(self, filename):
        DockerfileParser.__init__(self, cache_content=True)
        self.dockerfile_path = filename

        if self.is_url(filename) is not None:
            response = urllib.request.urlopen(filename)
            if self.is_content_type_plain_text(response):
                self.content = response.read().decode('utf-8')
            else:
                print('ERROR: file format not supported\n')

        elif os.path.isfile(filename):
            self.content = open(filename, encoding='utf-8').read()

        elif self.is_github_repo(filename):
            filename = 'https://raw.githubusercontent.com/' + filename + '/master/Dockerfile'
            self.content = urllib.request.urlopen(filename).read().decode('utf-8')

        else:
            print('ERROR: file format not supported\n')

        self.TOKENS = App._config.get('all')
        self.commands = self.dict_to_command_object(self.structure)

    @property
    def content(self):
        pass

    @content.setter
    def content(self, content):
        pass

    def is_github_repo(self, filename):
        regex = re.compile(r'^[-_.0-9a-z]+/[-_.0-9a-z]+$', re.IGNORECASE)

        return True if regex.match(filename) is not None else False

    def is_url(self, filename):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return regex.match(filename)

    def is_content_type_plain_text(self, response):
        content_type = response.getheader('Content-Type')
        regex        = re.compile(r'text/plain')

        return True if regex.search(content_type) is not None else False

    def dict_to_command_object(self, lst):
        commands = []

        for element in lst:
            command = DockerfileCommand()
            command.instruction = element.get('instruction').upper()
            command.arguments = element.get('value').split(' ')
            command.line = element.get('startline') + 1
            command._raw = element.get('content')
            commands.append(command)

        return commands
