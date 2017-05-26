#!/usr/bin/env python3

import json

from whalelinter.app import App


COLORS = {
    'BLUE'  : '\033[94m',
    'GREEN' : '\033[92m',
    'YELLOW': '\033[93m',
    'RED'   : '\033[91m',
    'ENDC'  : '\033[0m',
    'BOLD'  : '\033[1m',
}

class Tools:

    @staticmethod
    def sanitize_list(lst):
        lst = [i for i in lst if i != '']
        return lst

    @staticmethod
    def merge_odd_strings(lst):
        bad_splitted_string = False
        for s in lst:
            if '=' not in s:
                bad_splitted_string = True

        if bad_splitted_string:
            indexes = []
            for string in lst:
                if '=' not in string:
                    if not string.startswith('"'):
                        indexes.append(lst.index(string))

            for idx in reversed(indexes):
                lst[idx - 1] = str(lst[idx - 1]) + ' ' + str(lst[idx])
                lst[idx] = ''

        return Tools.sanitize_list(lst)


class DockerfileCommand:
    def __init__(self):
        self.instruction = None
        self.arguments = None
        self.line = None
        self._raw = None

    def __repr__(self):
        return self.instruction + ' ' + ' '.join(self.arguments)


class Log:
    def __init__(self, rule, line, message):
        self.rule     = rule
        self.category = rule.get('category')
        self.message  = message

        if line is None:
            line = 0

        self.line = line

    def display(self, color, category_right_padding, line_number_right_padding):
        category_right_padding = category_right_padding * ' '
        line_number_right_padding = line_number_right_padding * ' '

        if self.line:
            print('  {}{}: {}{}{} : {}{}'.format(line_number_right_padding, self.line, COLORS.get(color.upper()), self.category, category_right_padding, COLORS.get('ENDC'), self.message))
        else:
            print('      {}{}{} : {}{}'.format(COLORS.get(color.upper()), self.category, category_right_padding, COLORS.get('ENDC'), self.message))

    def displayLight(self, level):
        print('{}:{}'.format(level, self.message))



class Collecter:
    def __init__(self, rules, ignore=None):
        self.ignore      = ignore
        self.rules       = rules
        self.logs        = []
        self.log_classes = App._config['log_classes']

    def get_level_by_category(self, category):
        for log_class in self.log_classes:
            if category in log_class.get('categories'):
                return log_class.get('level')
        return None

    def get_rule_by_id(self, rule_id):
        for rule in self.rules:
            if rule.get('id') == str(rule_id):
                return rule
        return None

    def throw(self, id, **kwargs):
        if str(id) not in self.ignore:
            rule    = self.get_rule_by_id(id)
            message = rule.get('message')

            if kwargs.get('keys'):
                message = message.format(**(kwargs.get('keys')))

            log = Log(rule, kwargs.get('line'), message)
            self.logs.append(log)

    def find_longest_category_name(self, level):
        length = 0
        for log_class in self.log_classes:
            if level == log_class.get('level'):
                for category in log_class.get('categories'):
                    if len(category) > length:
                        length = len(category)

        return length

    def find_highest_line_number(self):
        length = 0
        for log in self.logs:
            if len(str(log.line)) > length:
                length = len(str(log.line))

        return length

    def display(self):
        if App._args.get('json'):
            if self.logs:
                output = {log_class.get('level'): { c: {} for c in log_class.get('categories') } for log_class in self.log_classes}

                for log in self.logs:
                    output[self.get_level_by_category(log.category)][log.category] = log.__dict__

                print(json.dumps(output))
        else:
            if App._args.get('no_color'):
                if self.logs:
                    self.logs.sort(key=(lambda log: log.line))

                    for log_class in self.log_classes:
                        level      = log_class.get('level')
                        categories = log_class.get('categories')

                        for log in self.logs:
                            if log.category in categories:
                                log.displayLight(level)
                else:
                    print('{}'.format('Everything is good'))
            else:
                if self.logs:
                    self.logs.sort(key=(lambda log: log.line))

                    for log_class in self.log_classes:
                        level      = log_class.get('level')
                        color      = log_class.get('color').upper()
                        categories = log_class.get('categories')

                        print('{}{} :{}'.format(COLORS.get(color), level.upper(), COLORS.get('ENDC')))
                        for log in self.logs:
                            if log.category in categories:
                                category_right_padding = self.find_longest_category_name(level) - len(log.category)
                                line_number_right_padding = self.find_highest_line_number() - len(str(log.line))
                                log.display(color, category_right_padding, line_number_right_padding)
                        print()
                else:
                    print('{}{}{}\n'.format(COLORS.get('GREEN'), 'Everything is good', COLORS.get('ENDC')))
