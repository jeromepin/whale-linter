# whale-linter

[![PyPI](https://img.shields.io/pypi/v/whale-linter.svg)](https://pypi.python.org/pypi/whale-linter)
[![PyPI](https://img.shields.io/pypi/dm/whale-linter.svg)](https://pypi.python.org/pypi/whale-linter)
[![PyPI](https://img.shields.io/pypi/l/whale-linter.svg)](https://raw.githubusercontent.com/jeromepin/whale-linter/master/LICENSE)
[![Docker Stars](https://img.shields.io/docker/stars/jeromepin/whale-linter.svg)](https://hub.docker.com/r/jeromepin/whale-linter/)
[![Docker Pulls](https://img.shields.io/docker/pulls/jeromepin/whale-linter.svg)](https://hub.docker.com/r/jeromepin/whale-linter/)

**whale-linter** is a cross-platform *Dockerfile* linter.

![alt text](https://raw.githubusercontent.com/jeromepin/whale-linter/master/whale-linter.png)


## Installation

#### Tested on

* Python 3.2, 3.4, 3.5
* Debian wheezy, jessie, stretch


### Docker : The cool way :)

**Note** : You should use a specific tag (like `jeromepin/whale-linter:0.0.4`) instead of (implicit) *latest*

```
docker run -it --rm -v /path/to/Dockerfile:/Dockerfile jeromepin/whale-linter
```


### PyPI : The easy way

```bash
pip install whale-linter
```

and to upgrade :

```bash
pip install --upgrade whale-linter
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


## Rules

Here is the list of all rules checked by **whale-linter**.

Do not hesitate to [create a new issue](https://github.com/jeromepin/whale-linter/issues/new) if you have an idea for a new/incomplete rule.


Rules are ordered as follows :

* *WL1xxx* : Critical errors

* *WL2xxx* : Bad practices

* *WL3xxx* : Enhancements


| Rule | Corresponding message (as template given in config.json) |
| ------ | ----------- |
| [WL1000](https://github.com/jeromepin/whale-linter/wiki/WL1000) | '{token}' is mandatory |
| [WL1001](https://github.com/jeromepin/whale-linter/wiki/WL1001) | '{token}' must be present only once |
| [WL2000](https://github.com/jeromepin/whale-linter/wiki/WL2000) | A tag should be specified for the '{image}' image |
| [WL2001](https://github.com/jeromepin/whale-linter/wiki/WL2001) | Using the 'latest' tag isn't wise, as it won't always be a reference to the same version |
| [WL2002](https://github.com/jeromepin/whale-linter/wiki/WL2002) | Use 'WORKDIR' to change directory |
| [WL2003](https://github.com/jeromepin/whale-linter/wiki/WL2003) | Some shell commands like '{command}' are pointless in containers |
| [WL2004](https://github.com/jeromepin/whale-linter/wiki/WL2004) | 'WORKDIR' path should be absolute |
| [WL2005](https://github.com/jeromepin/whale-linter/wiki/WL2005) | 'EXPOSE' port ({port}) must be in 1-65535 range |
| [WL2006](https://github.com/jeromepin/whale-linter/wiki/WL2006) | Prefer 'COPY' over 'ADD' for adding files and directories to a container. 'ADD' sounds to much magic |
| [WL2007](https://github.com/jeromepin/whale-linter/wiki/WL2007) | Be careful changing to root user |
| [WL2008](https://github.com/jeromepin/whale-linter/wiki/WL2008) | Avoid running 'apt-get upgrade' in container. Move to a newer image instead |
| [WL2009](https://github.com/jeromepin/whale-linter/wiki/WL2009) | Missing '--no-install-recommends' in your '{command}' command |
| [WL2010](https://github.com/jeromepin/whale-linter/wiki/WL2010) | Missing '-y' in your '{command}' command |
| [WL2011](https://github.com/jeromepin/whale-linter/wiki/WL2011) | Avoid running 'apt-get dist-upgrade' in container. Move to a newer image instead |
| [WL2012](https://github.com/jeromepin/whale-linter/wiki/WL2012) | There is two consecutive 'RUN'. Consider chaining them with '\' and '&&' |
| [WL3000](https://github.com/jeromepin/whale-linter/wiki/WL3000) | Consider removing APT cache : 'rm -rf /var/lib/apt/lists/*' |
| [WL3001](https://github.com/jeromepin/whale-linter/wiki/WL3001) | Using '{token}' is recommended |
| [WL3002](https://github.com/jeromepin/whale-linter/wiki/WL3002) | Consider sorting APT packages for better reading |
| [WL3003](https://github.com/jeromepin/whale-linter/wiki/WL3003) | A version should be specified for the package '{package}' in order to improve immutability |


## Author

Jerome Pin ([@jerome_pin](https://twitter.com/jerome_pin)) <<jerome@jeromepin.fr>>


## Licence

MIT. See [LICENCE](https://raw.githubusercontent.com/jeromepin/whale-linter/master/LICENSE) file.
