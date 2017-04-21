#!/usr/bin/env python3
COLORS = {
    'BLUE'  : '\033[94m',
    'GREEN' : '\033[92m',
    'YELLOW': '\033[93m',
    'RED'   : '\033[91m',
    'ENDC'  : '\033[0m',
    'BOLD'  : '\033[1m',
}

class DockerfileCommand:
    def __init__(self):
        self.instruction = None
        self.arguments = None
        self.line = None
        self._raw = None

    def __repr__(self):
        return self.instruction + ' ' + ' '.join(self.arguments)


class Log:
    def __init__(self, rule, line, keys):
        # print(rule)
        self.id       = rule.get('id')
        self.category = rule.get('category')
        self.message  = rule.get('message').format(**keys)

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


class Collecter:
    def __init__(self, rules, ignore=None):
        self.ignore      = ignore
        self.rules       = rules
        self.logs        = []
        self.log_classes = [
            {
                'level'      : 'critical',
                'color'      : 'red',
                'categories' : ['NotFound', 'TooMuch', 'TooLong', 'BadValue']
            },
            {
                'level'      : 'warning',
                'color'      : 'yellow',
                'categories' : ['BadPractice', 'Pointless']
            },
            {
                'level'      : 'enhancement',
                'color'      : 'blue',
                'categories' : ['BestPractice', 'Immutability', 'Maintainability']
            },
        ]

    def throw(self, id, line=None, keys={}):
        # rule = (item for item in self.rules if .get(id) == id)
        if str(id) not in self.ignore:
            for rule in self.rules:
                if rule.get('id') == str(id):
                    break

            log = Log(rule, line, keys)
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
