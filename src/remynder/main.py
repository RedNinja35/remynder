import sys

from config import read_config
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication
from reminder import ReminderService
from ui import GuiService


def main():
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    config = read_config()
    ui = GuiService(config)

    reminder_service = ReminderService(config=config, ui_provider=ui)

    timer = QTimer()
    timer.setInterval(30_000)
    timer.timeout.connect(reminder_service.check)

    timer.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
