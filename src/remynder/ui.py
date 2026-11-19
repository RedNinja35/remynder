import sys
from collections.abc import Callable
from pathlib import Path
from string import Template

from PyQt6.QtCore import QPoint, QStandardPaths, Qt
from PyQt6.QtGui import QAction, QColor, QFont, QGuiApplication, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
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

from .config import Config, save_config

CONFIG_DIR = Path(
    QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation)
)

THEMES = {
    "light": {
        "bg": "#FFFFFF",
        "border": "#E3E6EA",
        "text": "#1F2328",
        "subtext": "#6B7280",
        "accent": "#2563EB",
        "accent_hover": "#1D4ED8",
        "accent_pressed": "#1E40AF",
        "accent_text": "#FFFFFF",
        "focus": "#93C5FD",
    },
    "dark": {
        "bg": "#1E1F24",
        "border": "#34363D",
        "text": "#E8EAED",
        "subtext": "#9AA0A6",
        "accent": "#4F8CFF",
        "accent_hover": "#6A9DFF",
        "accent_pressed": "#3B78F0",
        "accent_text": "#FFFFFF",
        "focus": "#1E3A8A",
    },
}

SHADOW_COLORS = {
    "light": QColor(0, 0, 0, 60),
    "dark": QColor(0, 0, 0, 170),
}

STYLESHEET = Template("""
#card {
    background-color: $bg;
    border: 1px solid $border;
    border-radius: 18px;
}
QLabel {
    background: transparent;
    font-family: "Segoe UI Variable Text", "Segoe UI", "Inter", sans-serif;
}
#title {
    color: $accent;
    font-size: 10pt;
    font-weight: 700;
}
#message {
    color: $text;
    font-size: 15pt;
    font-weight: 500;
}
#hint {
    color: $subtext;
    font-size: 9pt;
}
#okButton {
    background-color: $accent;
    color: $accent_text;
    border: 2px solid transparent;
    border-radius: 10px;
    padding: 9px 36px;
    min-width: 110px;
    font-family: "Segoe UI Variable Text", "Segoe UI", "Inter", sans-serif;
    font-size: 11pt;
    font-weight: 600;
}
#okButton:hover   { background-color: $accent_hover; }
#okButton:pressed { background-color: $accent_pressed; }
#okButton:focus   { border: 2px solid $focus; }
""")

SETTINGS_WINDOW_WIDTH = 1000
SETTINGS_WINDOW_HEIGHT = 400
POPUP_WINDOW_WIDTH = 500
POPUP_WINDOW_HEIGHT = 100
ICON_PATH = "resources/remynder.png"
DELIMITER = "\n"
DAY_IN_MINUTES = 24 * 60


def resource_path(relative_path: str) -> str:
    """Return absolute path to a resource, working for dev and PyInstaller builds."""
    if hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)  # bundle root in the exe
    else:
        base_path = Path(__file__).resolve().parent.parent  # src/ -> project root
    return str(base_path / relative_path)


def is_dark_mode() -> bool:
    hints = QGuiApplication.styleHints()
    if hints is not None:
        scheme = hints.colorScheme()
        if scheme != Qt.ColorScheme.Unknown:
            return scheme == Qt.ColorScheme.Dark
    return QGuiApplication.palette().window().color().lightness() < 128


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon: QIcon, parent: QWidget | None = None):
        super().__init__(icon, parent)

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
        self.menu.addActions(self.actions)
        self.setContextMenu(self.menu)


class GuiService:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._icon = QIcon(resource_path(ICON_PATH))

        self.toggle_action = QAction("Disable")
        self.toggle_action.triggered.connect(self._toggle_active)

        settings_action = QAction("Settings")
        settings_action.triggered.connect(self._open_settings_window)

        tray = SystemTrayIcon(self._icon)
        tray.insert_action(0, self.toggle_action)
        tray.insert_action(1, settings_action)

        self.tray = tray
        self.reminder_window: PopupWindow | None = None
        self.settings_window: QMainWindow | None = None

    @property
    def center(self) -> QPoint:
        screen = QGuiApplication.primaryScreen()
        if screen is not None:
            return screen.availableGeometry().center()
        return QPoint(0, 0)

    def show_popup(self, message: str, reset: Callable[[], None]) -> None:
        reminder_window = PopupWindow(message, reset)
        reminder_window.setWindowTitle("Remynder")
        reminder_window.setWindowIcon(self._icon)

        reminder_window.show()
        self.reminder_window = reminder_window

    def _open_settings_window(self) -> None:
        if self.settings_window is None:
            self.settings_window = SettingsWindow(self._icon, self._config, self.center)
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def _toggle_active(self) -> None:
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

    def _build_ui(self, icon: QIcon, center: QPoint) -> None:
        self.setWindowTitle("Settings")
        self.setWindowIcon(icon)
        self.setGeometry(
            int(center.x() - (SETTINGS_WINDOW_WIDTH / 2)),
            int(center.y() - (SETTINGS_WINDOW_HEIGHT / 2)),
            SETTINGS_WINDOW_WIDTH,
            SETTINGS_WINDOW_HEIGHT,
        )

        spin_box = QSpinBox()
        spin_box.setRange(1, DAY_IN_MINUTES)
        self.spin_box = spin_box

        text_field = QTextEdit()
        self.text_field = text_field

        self.save_button = QPushButton()
        self.save_button.setText("Save")
        self.save_button.setMaximumWidth(120)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(text="Interval in minutes"))
        layout.addWidget(spin_box)
        layout.addWidget(QLabel(text="Messages"))
        layout.addWidget(text_field)
        layout.addWidget(self.save_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def _add_button_events(self) -> None:
        self.save_button.clicked.connect(self._save_settings)

    def _load_settings(self, config: Config) -> None:
        self._config = config
        self.spin_box.setValue(config.interval)
        self.text_field.setText(DELIMITER.join(config.lines))

    def _save_settings(self) -> None:
        interval = self.spin_box.value()
        text = self.text_field.toPlainText()

        lines = [line.strip() for line in text.splitlines() if line.strip()]

        self._config.interval = interval
        self._config.lines = lines
        save_config(self._config, CONFIG_DIR)
        self.close()


class PopupWindow(QDialog):
    def __init__(self, message: str, reset: Callable[[], None]):
        super().__init__()
        self.reset = reset

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Dialog
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(28, 28, 28, 28)

        self.card = QFrame()
        self.card.setObjectName("card")
        outer_layout.addWidget(self.card)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(36, 28, 36, 26)
        layout.setSpacing(14)

        title = QLabel("Remynder")
        title.setObjectName("title")
        f = title.font()

        f.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1.5)
        title.setFont(f)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text = QLabel(message)
        text.setObjectName("message")
        text.setWordWrap(True)

        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text.setMinimumWidth(360)
        text.setMaximumWidth(520)

        self.button = QPushButton("OK")
        self.button.setObjectName("okButton")
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.setDefault(True)

        self.button.clicked.connect(self.on_close)
        self.finished.connect(self.on_close)

        button_column = QHBoxLayout()
        button_column.addStretch()
        button_column.addWidget(self.button)
        button_column.addStretch()

        layout.addWidget(title)
        layout.addWidget(text)
        layout.addSpacing(6)
        layout.addLayout(button_column)

        self._set_shadow()
        self._set_theme()
        self._show_window()

    def on_close(self) -> None:
        self.reset()
        self.close()

    def _set_shadow(self) -> None:
        self.shadow = QGraphicsDropShadowEffect(self.card)
        self.shadow.setBlurRadius(40)
        self.shadow.setOffset(0, 8)
        self.card.setGraphicsEffect(self.shadow)

    def _set_theme(self) -> None:
        mode = "dark" if is_dark_mode() else "light"
        self.setStyleSheet(STYLESHEET.substitute(THEMES[mode]))
        self.shadow.setColor(SHADOW_COLORS[mode])

    def _show_window(self) -> None:
        self.adjustSize()
        screen = self.screen()
        if screen is not None:
            area = screen.availableGeometry()
            self.move(area.center() - self.rect().center())
        self.raise_()
        self.activateWindow()
        self.button.setFocus()
