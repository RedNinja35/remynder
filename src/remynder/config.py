from configparser import ConfigParser
from pathlib import Path

CONFIG_FILE = "config.ini"


def create_config() -> None:
    path = Path(CONFIG_FILE)
    if not path.exists():
        path.touch()


class Config:
    def __init__(self):
        create_config()
        self._config = ConfigParser()
        self._config.read(CONFIG_FILE)

    def get_intervall(self) -> int:
        return self._config.getint("DEFAULT", "intervall", fallback=30)

    def get_lines(self) -> list[str]:
        return self._config.get("DEFAULT", "lines").split(",")

    def set_intervall(self, value: int) -> None:
        self._config.set("DEFAULT", "intervall", str(value))

    def set_lines(self, value: list[str]) -> None:
        self._config.set("DEFAULT", "lines", ",".join(value))