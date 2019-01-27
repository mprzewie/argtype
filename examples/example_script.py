from typing import NamedTuple

from argtype import TypedArgumentParser


class Config(NamedTuple):
    """
    A config for this script

    Args:
        number: an integer parameter
            which is very fancy
        param: some fancy string
        floating: a float
    """

    number: int
    param: str = "some string"
    floating: float = 0.7


if __name__ == "__main__":
    parser: TypedArgumentParser[Config] = TypedArgumentParser(Config)
    config = parser.parse_args()
    for n in range(config.number):
        print(f"{n}: {config.param}")

    print(config.floating * 42)
