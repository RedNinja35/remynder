from random import choice
from time import time
from typing import Protocol

from config import Config

disabled = False
last_reminder = time()


class UiProvider(Protocol):
    def show_popup(self, message: str): ...


class ReminderService:
    def __init__(self, config: Config, ui_provider: UiProvider) -> None:
        self.config = config
        self.ui_provider = ui_provider
        self._set_last_reminder(time())

    def _set_last_reminder(self, time: float) -> None:
        self.last_reminder = time

    def check(self) -> None:
        print("Checking...")
        now = time()
        if not self.config.disabled and now >= (
            self.last_reminder + (self.config.intervall * 60)
        ):
            self.ui_provider.show_popup(choice(self.config.lines))
