#!/usr/bin/env python3
from dlint.app        import App
from dlint.dispatcher import Dispatcher


class Apt(object):
    def __init__(self): pass

    @staticmethod
    def remove(lst, element):
        ret = False
        if element in lst:
            lst.remove(element)
            ret = True

        return ret

    @Dispatcher.register(token='run', command='apt-get')
    def this(checker, command):
        checker.apt_has_been_used = True
        # filter global apt-get params
        if ('update' not in command) and Apt.remove(command, '-y'):
            App._collecter.throw(2010, checker.lineno, keys={'command': 'apt-get ' + ' '.join(command)})

    def update(checker):
        pass

    @Dispatcher.register(token='run', command='apt-get', subcommand='upgrade')
    def upgrade(checker, packages):
        App._collecter.throw(2008, checker.lineno)

        for idx, package in enumerate(packages):
            if '=' not in package:
                App._collecter.throw(3003, checker.lineno, keys={'package': package})
            else:
                packages[idx] = package.split('=')[0]

        if packages and sorted(packages) == packages:
            App._collecter.throw(3002)

    @Dispatcher.register(token='run', command='apt-get', subcommand='install')
    def install(checker, packages):
        if Apt.remove(packages, '--no-install-recommends'):
            App._collecter.throw(2009, checker.lineno, keys={'command': ' '.join(command)})

        for idx, package in enumerate(packages):
            if '=' not in package:
                App._collecter.throw(3003, checker.lineno, keys={'package': package})
            else:
                packages[idx] = package.split('=')[0]

        if sorted(packages) != packages:
            App._collecter.throw(3002)

    @Dispatcher.register(token='run', command='apt-get', subcommand='dist-upgrade')
    def dist_upgrade(checker, packages):
        App._collecter.throw(2011, checker.lineno)
