from collections.abc import Callables
from time import time

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QAction, QFont, QGuiApplication, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QMenu,
    QPushButton,
    QSpinBox,
    QSystemTrayIcon,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from config import Config, save_config

SETTINGS_WINDOW_WIDTH = 1000
SETTINGS_WINDOW_HEIGHT = 400
POPUP_WINDOW_WIDTH = 500
POPUP_WINDOW_HEIGHT = 100
ICON_PATH = "ressources/remynder.png"
DELIMITER = "\n"


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon: QIcon, parent=None):
        super().__init__(icon, parent)

        self.setIcon(icon)
        self.setVisible(True)

        quit_action = QAction("Quit")
        quit_action.triggered.connect(QApplication.quit)

        actions = [quit_action]
        self.actions = actions

    def insert_action(self, index: int, action: QAction) -> None:
        self.actions.insert(index, action)
        self._create_menu()

    def _create_menu(self) -> None:
        self.menu = QMenu()
        [self.menu.addAction(a) for a in self.actions]
        self.setContextMenu(self.menu)


class GuiService:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._icon = QIcon(ICON_PATH)

        self.toggle_action = QAction("Disable")
        self.toggle_action.triggered.connect(self._toggle_active)

        settings_action = QAction("Settings")
        settings_action.triggered.connect(self._open_settings_window)

        tray = SystemTrayIcon(self._icon)
        tray.insert_action(0, self.toggle_action)
        tray.insert_action(1, settings_action)

        self.tray = tray
        self.reminder_window: QMainWindow | None = None
        self.settings_window: QMainWindow | None = None

    @property
    def center(self):
        screen = QGuiApplication.primaryScreen()
        if not screen is None:
            return screen.availableGeometry().center()
        return QPoint(0, 0)

    def show_popup(self, message: str, reset: Callable) -> None:
        reminder_window = PopupWindow(message, reset, self.center)
        reminder_window.setWindowTitle("Remynder")
        reminder_window.setWindowIcon(self._icon)

        reminder_window.show()
        self.reminder_window = reminder_window

    def _open_settings_window(self) -> None:
        settings_window = SettingsWindow(self._icon, self._config, self.center)
        settings_window.show()
        self.settings_window = settings_window

    def _toggle_active(self):
        self._config.disabled = not self._config.disabled
        if self._config.disabled:
            self.toggle_action.setText("Enable")
        else:
            self.toggle_action.setText("Disable")


class SettingsWindow(QMainWindow):
    def __init__(self, icon: QIcon, config: Config, center: QPoint) -> None:
        super().__init__()
        self._build_ui(icon, center)
        self._load_settings(config)
        self._add_button_events()

    def _build_ui(self, icon: QIcon, center: QPoint):
        self.setWindowTitle("Settings")
        self.setWindowIcon(icon)
        self.setGeometry(
            int(center.x() - (SETTINGS_WINDOW_WIDTH / 2)),
            int(center.y() - (SETTINGS_WINDOW_HEIGHT / 2)),
            SETTINGS_WINDOW_WIDTH,
            SETTINGS_WINDOW_HEIGHT,
        )

        edit = QSpinBox()
        self.edit = edit

        text_field = QTextEdit()
        self.text_field = text_field

        self.save_button = QPushButton()
        self.save_button.setText("Save")
        self.save_button.setMaximumWidth(120)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(text="Intervall in minutes"))
        layout.addWidget(edit)
        layout.addWidget(QLabel(text="Messages"))
        layout.addWidget(text_field)
        layout.addWidget(self.save_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def _add_button_events(self):
        self.save_button.clicked.connect(self._save_settings)

    def _load_settings(self, config: Config):
        self._config = config
        self.edit.setValue(config.intervall)
        self.text_field.setText(DELIMITER.join(config.lines))

    def _save_settings(self) -> None:
        intervall = self.edit.value()
        lines = self.text_field.toPlainText().split(DELIMITER)

        self._config.intervall = intervall
        self._config.lines = lines
        save_config(self._config)
        self.close()


class PopupWindow(QMainWindow):
    def __init__(self, message: str, reset: Callable, center: QPoint):
        super().__init__()
        self.reset = reset

        self.setGeometry(
            int(center.x() - POPUP_WINDOW_WIDTH / 2),
            int(center.y() - POPUP_WINDOW_HEIGHT / 2),
            POPUP_WINDOW_WIDTH,
            POPUP_WINDOW_HEIGHT,
        )

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.WindowType.WindowTitleHint)

        layout = QVBoxLayout()

        button = QPushButton("Ok")
        button.setMaximumWidth(120)
        button.clicked.connect(self._close)

        font = QFont()
        font.setBold(True)

        label = QLabel(text=message)
        label.setFont(font)
        label.setMargin(15)

        layout.addWidget(label)
        layout.addWidget(button)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def _close(self):
        self.reset(time())
        self.close()
