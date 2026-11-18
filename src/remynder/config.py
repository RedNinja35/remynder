from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path

CONFIG_FILE = Path("config.ini")
LINES_DELIMITER = ";"

DEFAULT_CONFIG = f"""
[DEFAULT]
intervall = 30
lines = Your chair called - it needs a break from you. Stand up!{LINES_DELIMITER}Error 404: Movement not found. Please reboot your legs.{LINES_DELIMITER}Even your code needs to compile - so does your body. Time to stand!
disabled = False
"""


def create_config_file() -> None:
    if not CONFIG_FILE.exists():
        with Path.open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(DEFAULT_CONFIG)


def create_parser(path: Path) -> ConfigParser:
    create_config_file()
    parser = ConfigParser()
    with Path.open(path, "r", encoding="utf-8") as f:
        parser.read_file(f)
    return parser


@dataclass
class Config:
    interval: int
    lines: list[str]
    disabled: bool


def read_config() -> Config:
    parser = create_parser(CONFIG_FILE)
    return Config(
        interval=parser.getint("DEFAULT", "interval"),
        lines=parser.get("DEFAULT", "lines").split(LINES_DELIMITER),
        disabled=parser.getboolean("DEFAULT", "disabled"),
    )


def save_config(config: Config) -> None:
    parser = create_parser(CONFIG_FILE)
    parser["DEFAULT"].update(
        {
            "interval": str(config.interval),
            "lines": LINES_DELIMITER.join(config.lines),
            "disabled": str(config.disabled),
        }
    )
    with Path.open(CONFIG_FILE, mode="w", encoding="utf-8") as f:
        parser.write(f)
