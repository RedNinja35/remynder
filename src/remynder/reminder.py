from collections.abc import Callable
from random import choice
from time import time
from typing import Protocol

from .config import Config

disabled = False
last_reminder = time()


class UiProvider(Protocol):
    def show_popup(self, message: str, reset: Callable[[], None]) -> None: ...


class ReminderService:
    def __init__(self, config: Config, ui_provider: UiProvider, disabled: bool) -> None:
        self.config = config
        self.ui_provider = ui_provider
        self.reminder_is_reset = True
        self.set_last_reminder()

    def set_last_reminder(self) -> None:
        self.reminder_is_reset = True
        self.last_reminder = time()

    def check(self) -> None:
        print("Checking...")
        now = time()
        if (
            not self.config.disabled
            and self.reminder_is_reset
            and now >= (self.last_reminder + (self.config.interval * 60))
        ):
            self.ui_provider.show_popup(
                choice(self.config.lines), self.set_last_reminder
            )
            self.reminder_is_reset = False
