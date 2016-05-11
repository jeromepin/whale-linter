#!/usr/bin/env python3
import sys
import argparse
import os.path

from pkg_resources import get_distribution, DistributionNotFound

from dlint.app       import App
from dlint.parser    import Parser
from dlint.checker   import Checker
from dlint.collecter import Collecter

__all__ = ['run']

def run():
    try:
        _dist = get_distribution('app')
        dist_loc = os.path.normcase(_dist.location)
        here = os.path.normcase(__file__)
        if not here.startswith(os.path.join(dist_loc, 'app')):
            raise DistributionNotFound
    except DistributionNotFound:
        __version__ = 'Please install this project with setup.py'
    else:
        __version__ = _dist.version

    parser = argparse.ArgumentParser(description='A simple nonprofessional Dockerfile linter')
    parser.add_argument('-i', '--ignore', default=None, help='Rule to ignore', action='append')
    parser.add_argument('-v', '--version', help='Print version', action='version', version='%(prog)s {}'.format(__version__))
    parser.add_argument('dockerfile', help="The Dockerfile to lint")
    args = parser.parse_args()

    print('\n{}\n'.format(args.dockerfile))

    if args.ignore is None:
        args.ignore = []

    App._collecter = Collecter(App._config['rules'], args.ignore)

    checkFor = Checker(Parser(args.dockerfile).shlex_to_dictionnary())
    checkFor.all()

    App._collecter.display()

if __name__ == '__main__':
    run()
