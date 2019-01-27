# argtype
A typed argument parser for Python 3.6+ scripts.

## Overview
This package enables creation of `argparse.ArgumentParsers` from `NamedTuple` objects. 
Created parsers return parsed arguments as an object of configured type, which empowers the developer with more control 
over the contents and types of their scripts.

## Example
The following example may be found [here](examples/example.py).

1. Define a `NamedTuple` specifying the script's arguments:
    ```python
    from typing import NamedTuple
    
    class Config(NamedTuple):
        """
        A config for this script
     
        Args: 
            number: an integer parameter
               which is very necessary
            param: some fancy string
            floating: a float
        """
        number: int
        param: str = "some string"
        floating: float = 0.7
    ```

2. Create a `TypedArgumentParser` object from the `Config` class:
    ```python
    from argtype import TypedArgumentParser
    parser: TypedArgumentParser[Config] = TypedArgumentParser(Config)
    ```

3. Parse the arguments and enjoy code completion and type information!
    ```python
    config = parser.parse_args()
    for n in range(config.number):
        print(f"{n}: {config.param}")

    print(config.floating * 42)
    ```

Executing this script with `-h` (help) flag:
```bash
python examples/example_script.py -h
```

will yield the following output:
```
usage: example_script.py [-h] --number NUMBER [--param PARAM]
                         [--floating FLOATING]

A config for this script Args:

optional arguments:
  -h, --help           show this help message and exit
  --number NUMBER      an integer parameter which is very necessary
  --param PARAM        some fancy string
  --floating FLOATING  a float

```

## Details

### Why do I need to specify the return type twice?

```python
parser: TypedArgumentParser[Config] = TypedArgumentParser(Config)
```
In the above line, passing the configuring `NamedTuple` type to the constructor (on the right) lets the parser perform it's magic underneath
and return the parsed arguments as the specified type.

Type annotation of the parser (on the left) is not necessary, but it will allow IDEs such [PyCharm](https://www.jetbrains.com/pycharm/) 
infer the type of the `NamedTuple` returned by the parser.


### Type annotation of the arguments 
If a type of a field in configuring `NamedTuple` has been specified, i.e:
```python
int_param: int
```
the `TypedArgumentParser` will try to cast the argument with this field's name to that type and raise an error on failure.

### Supported types of arguments
Currently only Python's basic data types, i.e `int`, `float` and `str` are supported.

### Default and required arguments
If a field in the configuring `NamedTuple` has a default value, this value becomes default value of the argument with this name.
If no default value has been specified, this argument is listed as non-optional.

### Documentation (experimental)
`TypedArgumentParser` attempts to parse the configuring `NamedTuple`'s docstring into a description of the script and it's arguments.
The docstring should follow [Google convention](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings).

Everything in the header of the docstring (before the `Args` keyword) will be parsed into the script's description 
(unless the description had been provided in the parser's constructor) and the descriptions of fields of the configuring `NamedTuple` 
will be parsed into descriptions od the script's parameters.

## Installation

```bash
pip install git+https://github.com/mprzewie/argtype
```

## Python version
This library is highly type-oriented, so obviously Python 3.6+ is required.