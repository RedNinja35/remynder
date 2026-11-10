from random import choice
from time import time
from typing import Protocol

from config import Config, save_config


class UiProvider(Protocol):
    def show_popup(self, message: str): ...


class ReminderService:
    def __init__(self, config: Config, ui_provider: UiProvider) -> None:
        self.config = config
        self.ui_provider = ui_provider
        self.disabled = False
        self._set_last_reminder(time())

    def set_intervall(self, intervall: int) -> None:
        self.config.intervall = intervall

    def set_lines(self, lines: list[str]) -> None:
        self.config.lines = lines

    def get_intervall(self) -> int:
        return self.config.intervall

    def get_lines(self) -> list[str]:
        return self.config.lines

    def disable(self) -> None:
        self.disabled = True

    def enable(self) -> None:
        self.disabled = False
        self._set_last_reminder(time())

    def _set_last_reminder(self, time: float) -> None:
        self.last_reminder = time

    def check(self) -> None:
        print("Checking...")
        now = time()
        if not self.disabled and now >= (self.last_reminder + self.config.intervall):
            self.ui_provider.show_popup(choice(self.config.lines))
