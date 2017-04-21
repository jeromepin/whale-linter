#!/usr/bin/env python3
from whalelinter.app              import App
from whalelinter.dispatcher       import Dispatcher
from whalelinter.commands.command import PackageManager


@Dispatcher.register(token='run', command='apt-get')
@Dispatcher.register(token='run', command='apt')
class Apt(PackageManager):

    _callbacks      = {}
    _has_been_used  = 0

    def __init__(self, **kwargs):
        PackageManager.__init__(self, kwargs.get('token'), kwargs.get('command'), kwargs.get('args'), kwargs.get('lineno'))

        Apt.register(self)(type(self).install)
        Apt.register(self)(type(self).is_parameter_present, name='install', parameter='-y', args=kwargs.get('args'))
        Apt.register(self)(type(self).is_parameter_present, name='install', parameter='--no-install-recommends', args=kwargs.get('args'))
        Apt.register(self)(type(self).upgrade)
        Apt.register(self)(type(self).dist_upgrade, name='dist-upgrade')

        Apt._has_been_used = self.lineno

        for method in self.methods:
            if self.subcommand == method:
                self.react(method)

    def install(self):
        for idx, package in enumerate(self.packages):
            if '=' not in package:
                App._collecter.throw(3003, self.lineno, keys={'package': package})
            else:
                self.packages[idx] = package.split('=')[0]

        packages_without_versions = []
        for package in self.packages:
            if '=' in package:
                packages_without_versions.append(package.split('=')[0])
            else:
                packages_without_versions.append(package)

        if sorted(packages_without_versions) != packages_without_versions:
            App._collecter.throw(3002, self.lineno)

    def upgrade(self):
        App._collecter.throw(2008, self.lineno)

        for idx, package in enumerate(self.packages):
            if '=' not in package:
                App._collecter.throw(3003, self.lineno, keys={'package': package})
            else:
                packages[idx] = package.split('=')[0]

        if self.packages and sorted(self.packages) == self.packages:
            App._collecter.throw(3002, self.lineno)

    def dist_upgrade(self):
        App._collecter.throw(2011, self.lineno)
