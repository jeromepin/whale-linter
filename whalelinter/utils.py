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
        self.log_classes = App._config['log_classes']

    def get_level_by_category(self, category):
        for log_class, v in self.log_classes.items():
            if category in v.get('categories'):
                return log_class
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

            log   = Log(rule, kwargs.get('line'), message)
            level = self.get_level_by_category(log.category)

            if 'logs' not in self.log_classes[level]:
                self.log_classes[level]['logs'] = []

            self.log_classes[level]['logs'].append(log)

    def find_longest_category_name(self, level):
        length = 0
        for category in self.log_classes[level].get('categories'):
            if len(category) > length:
                length = len(category)

        return length

    def find_highest_line_number(self):
        length = 0
        for log_class, v in self.log_classes.items():
            if 'logs' in v:
                for log in v.get('logs'):
                    if len(str(log.line)) > length:
                        length = len(str(log.line))

        return length

    def display(self):
        logs = {
            'critical': False,
            'warning':  False,
            'enhancement': False
        }

        for log_class, v in self.log_classes.items():
            if 'logs' in v:
                logs[log_class] = True

        if logs['critical'] or logs['warning'] or logs['enhancement']:

            if App._args.get('json'):
                output = {log_class: {c: {} for c in v.get('categories')} for log_class, v in self.log_classes.items()}

                for log_class, v in self.log_classes.items():
                    if logs.get(log_class):
                        for log in v.get('logs'):
                            output[log_class][v.get('category')] = log.__dict__

                print(json.dumps(output))

            elif App._args.get('no_color'):
                for log_class, v in self.log_classes.items():
                    categories = v.get('categories')
                    if logs.get(log_class):
                        for log in v.get('logs'):
                            if log.category in categories:
                                log.displayLight(log_class)
            else:
                for log_class, v in self.log_classes.items():
                    color      = v.get('color').upper()
                    categories = v.get('categories')

                    if logs.get(log_class):
                        print('{}{} :{}'.format(COLORS.get(color), log_class.upper(), COLORS.get('ENDC')))
                        for log in v.get('logs'):
                            if log.category in categories:
                                category_right_padding = self.find_longest_category_name(log_class) - len(log.category)
                                line_number_right_padding = self.find_highest_line_number() - len(str(log.line))
                                log.display(color, category_right_padding, line_number_right_padding)
                        print()

            if logs.get('critical'):
                exit(3)
            elif logs.get('warning'):
                exit(2)
            elif logs.get('enhancement'):
                exit(1)
        else:
            print('{}{}{}\n'.format(COLORS.get('GREEN'), 'Everything is good', COLORS.get('ENDC')))
            exit(0)
