from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path

CONFIG_FILE = "config.ini"

path = Path(CONFIG_FILE)
if not path.exists():
    with open(CONFIG_FILE, "w") as f:
        f.write("[DEFAULT]\nintervall=30\nlines=\ndisabled=False")

parser = ConfigParser()
with open(CONFIG_FILE) as f:
    parser.read_file(f)


@dataclass
class Config:
    intervall: int
    lines: list[str]
    disabled: bool


def read_config() -> Config:
    return Config(
        intervall=parser.getint("DEFAULT", "intervall"),
        lines=parser.get("DEFAULT", "lines").split(","),
        disabled=parser.getboolean("DEFAULT", "disabled"),
    )


def save_config(config: Config) -> None:
    parser["DEFAULT"].update(
        {
            "intervall": str(config.intervall),
            "lines": ",".join(config.lines),
            "disabled": str(config.disabled),
        }
    )
    with open(CONFIG_FILE, mode="w", encoding="utf-8") as f:
        parser.write(f)


if __name__ == "__main__":
    config = Config(
        intervall=5000, lines=["Hello my friend", "See you later"], disabled=False
    )
    save_config(config)
    conf = read_config()
    print(conf)
