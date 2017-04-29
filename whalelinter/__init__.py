#!/usr/bin/env python3
import argparse
from pkg_resources import get_distribution, DistributionNotFound

from whalelinter.app       import App
from whalelinter.parser    import Parser
from whalelinter.checker   import Checker
from whalelinter.utils     import Collecter

__all__ = ['run']


def run():
    dist = get_distribution('whale-linter')
    __version__ = dist.version

    parser = argparse.ArgumentParser(description='A simple non professional Dockerfile linter')
    parser.add_argument('-i', '--ignore', default=None, help='Rule to ignore', action='append')
    parser.add_argument('-v', '--version', help='Print version', action='version', version='%(prog)s {}'.format(__version__))
    parser.add_argument('DOCKERFILE', help="The Dockerfile to lint (can be a file, a GitHub repo. or a direct URL)")
    args = parser.parse_args()

    print('\n{}\n'.format(args.DOCKERFILE))

    if args.ignore is None:
        args.ignore = []

    App._collecter = Collecter(App._config.get('rules'), args.ignore)

    parser  = Parser(args.DOCKERFILE)
    checker = Checker(parser.commands)
    checker.check()

    App._collecter.display()

if __name__ == '__main__':
    run()
