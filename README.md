# whale-linter

**whale-linter** is a cross-platform *Dockerfile* linter.

![alt text](whale-linter.png)

## Requirements

* Python3.4+


## Installation

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

Jerome Pin (@jerome_pin)


## Licence

MIT. See `LICENCE` file.
