import sys
from pathlib import Path

from PyQt6.QtCore import QStandardPaths, QTimer
from PyQt6.QtWidgets import QApplication

from .config import CONFIG_FILE, load_config, save_config
from .reminder import ReminderService
from .ui import GuiService

CHECK_INTERVAL_MS = 30_000


def get_config_path() -> Path:
    config_dir = Path(
        QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppConfigLocation
        )
    )
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / CONFIG_FILE


def main() -> None:
    app = QApplication([])
    app.setApplicationName("Remynder")
    app.setQuitOnLastWindowClosed(False)

    config_path = get_config_path()
    disabled = False

    config = load_config(config_path)
    ui = GuiService(
        config, disabled=disabled, on_save=lambda c: save_config(c, config_path)
    )

    reminder_service = ReminderService(config, ui_provider=ui, disabled=disabled)

    timer = QTimer()
    timer.setInterval(CHECK_INTERVAL_MS)
    timer.timeout.connect(reminder_service.check)

    timer.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
