from collections.abc import Callable
from random import choice
from time import monotonic
from typing import Protocol

from remynder.config import Config


class UiProvider(Protocol):
    def show_popup(self, message: str, reset: Callable[[], None]) -> None: ...


class ReminderService:
    def __init__(self, config: Config, ui_provider: UiProvider, disabled: bool) -> None:
        self.config = config
        self._disabled = disabled
        self.ui_provider = ui_provider
        self.reminder_is_reset = True
        self.set_last_reminder()

    def set_last_reminder(self) -> None:
        self.reminder_is_reset = True
        self.last_reminder = monotonic()

    def check(self) -> None:
        now = monotonic()
        interval_minutes = self.config.interval * 60

        if (
            not self._disabled
            and self.reminder_is_reset
            and now >= (self.last_reminder + interval_minutes)
        ):
            self.ui_provider.show_popup(
                choice(self.config.lines), self.set_last_reminder
            )
            self.reminder_is_reset = False
