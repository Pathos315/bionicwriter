r"""config contains the dataclass describing
    the overall configurations
    and a method to read the config

    Returns:
        a function that reads the dataclass as a JSON object.
    """

import json
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class BionicConfig:
    """A dataclass containing the overall configurations"""

    target: str
    export_dir: str
    font_regular: str
    font_bold: str
    font_italic: str
    font_bolditalic: str
    log_dir: str


def read_config(config_file: str) -> BionicConfig:
    """read_config takes a .json file and returns a ScrapeConfig object.

    Args:
        config_file (str): the path to the .json file containing the configs.

    Returns:
        ScrapeConfig: A dataclass containing the overall configurations
    """
    with open(config_file, encoding="utf-8") as file:
        data = json.load(file)
        return BionicConfig(**data)
