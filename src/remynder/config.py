from configparser import ConfigParser

CONFIG_FILE = "config.ini"

class Config:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read(CONFIG_FILE)

    def get_config(self) -> ConfigParser:
        return self.config

    def get_intervall(self) -> int:
        return self.config.getint("DEFAULT", "intervall", fallback=30)

    def get_lines(self) -> list[str]:
        return self.config.get("DEFAULT", "lines").split(",")

    def set_intervall(self, value: int) -> None:
        self.config.set("DEFAULT", "intervall", str(value))

    def set_lines(self, value: list[str]) -> None:
        self.config.set("DEFAULT", "lines", ",".join(value))