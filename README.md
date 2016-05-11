# dlint

**Dlint** is a cross-platform *Dockerfile* linter.

![alt text](dlint.png)

## Requirements

* Python3.4+


## Installation

### PyPI : The easy way

```bash
pip install dlint
```

and to upgrade :

```bash
pip install --upgrade dlint
```


## Usage

```bash
usage: dlint [-h] [-i RULE] [-v] DOCKERFILE

A simple non professional Dockerfile linter

positional arguments:
  DOCKERFILE            The Dockerfile to lint

optional arguments:
  -h, --help            Show this help message and exit
  -i, --ignore RULE     Rule to ignore
  -v, --version         Print version
```


## Author

Jerome Pin (@jerome_pin)


## Licence

MIT. See `LICENCE` file.