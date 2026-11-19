from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path

import toml


@dataclass
class Config:
    interval: int
    lines: list[str]
    disabled: bool


CONFIG_FILE = "config.toml"
DEFAULT_CONFIG = Config(
    interval=30,
    lines=[
        "Your chair called - it needs a break from you. Stand up!",
        "Error 404: Movement not found. Please reboot your legs.",
        "Even your code needs to compile - so does your body. Time to stand!",
    ],
    disabled=False,
)


## TODO: Add config file name to path
def load_config(file: Path) -> Config:
    if not file.exists():
        save_config(DEFAULT_CONFIG, file)

    with Path.open(file, mode="r", encoding="utf-8") as f:
        config = toml.load(f)

    return Config(
        interval=config["Settings"]["interval"],
        lines=config["Settings"]["lines"],
        disabled=config["Settings"]["disabled"],
    )


def save_config(config: Config, path: Path) -> None:

    settings = {
        "settings": {
            "interval": config.interval,
            "lines": config.lines,
            "disabled": config.disabled,
        }
    }

    with Path.open(path, mode="w", encoding="utf-8") as f:
        toml.dump(settings, f)
