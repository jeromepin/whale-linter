# whale-linter

[![PyPI](https://img.shields.io/pypi/v/whalelinter.svg?maxAge=2592000?style=flat-square)]()
[![PyPI](https://img.shields.io/pypi/dm/whalelinter.svg?maxAge=2592000?style=flat-square)]()
[![PyPI](https://img.shields.io/pypi/l/whalelinter.svg?maxAge=2592000?style=flat-square)]()


**whale-linter** is a cross-platform *Dockerfile* linter.

![alt text](https://raw.githubusercontent.com/jeromepin/whale-linter/master/whale-linter.png)


## Installation

#### Tested on

* Python 3.2, 3.4, 3.5
* Debian wheezy, jessie, stretch

### PyPI : The easy way

```bash
pip install whalelinter
```

and to upgrade :

```bash
pip install --upgrade whalelinter
```


## Usage

```bash
usage: whale-linter [-h] [-i RULE] [-v] DOCKERFILE

A simple non professional Dockerfile linter

positional arguments:
  DOCKERFILE            The Dockerfile to lint

optional arguments:
  -h, --help            Show this help message and exit
  -i, --ignore RULE     Rule to ignore
  -v, --version         Print version
```


## Author

Jerome Pin ([@jerome_pin](https://twitter.com/jerome_pin)) <<jerome@jeromepin.fr>>


## Licence

MIT. See [LICENCE](https://raw.githubusercontent.com/jeromepin/whale-linter/master/LICENSE) file.
