from dataclasses import dataclass
from pathlib import Path

import toml


@dataclass
class Config:
    interval: int
    lines: list[str]


CONFIG_FILE = "config.toml"
DEFAULT_CONFIG = Config(
    interval=30,
    lines=[
        "Your chair has filed a complaint. Please stand up before it calls HR.",
        "Your legs called. They want to know if they're still part of the team.",
        "Fun fact: standing burns more calories than staring at the screen.",
        (
            "Time to stand up and stretch - "
            "your spine has been doing yoga in the wrong direction."
        ),
        "Your butt has requested a short vacation. Please approve it.",
    ],
)


def load_config(file: Path) -> Config:
    if not file.exists():
        save_config(DEFAULT_CONFIG, file)

    with Path.open(file, mode="r", encoding="utf-8") as f:
        config = toml.load(f)

    return Config(
        interval=config["Settings"]["interval"],
        lines=config["Settings"]["lines"],
    )


def save_config(config: Config, path: Path) -> None:

    settings = {
        "settings": {
            "interval": config.interval,
            "lines": config.lines,
        }
    }

    with Path.open(path, mode="w", encoding="utf-8") as f:
        toml.dump(settings, f)
