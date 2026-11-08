from config import Config, read_config, save_config
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QGuiApplication, QIcon, QIntValidator
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QPushButton,
    QSpinBox,
    QSystemTrayIcon,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

SETTINGS_WINDOW_WIDTH = 1000
SETTINGS_WINDOW_HEIGHT = 400
ICON_PATH = "ressources/remynder.png"
DELIMITER = "\n"


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon: QIcon, parent=None):
        super().__init__(icon, parent)

        self.setIcon(icon)
        self.setVisible(True)

        self.toggle_action = QAction("Disable")
        self.toggle_action.triggered.connect(self.toggle_active)

        quit_action = QAction("Quit")
        quit_action.triggered.connect(QApplication.quit)

        actions = [self.toggle_action, quit_action]
        self.actions = actions

    def add_action(self, action: QAction) -> None:
        self.actions.append(action)
        self._create_menu()

    def _create_menu(self) -> None:
        self.menu = QMenu()
        self.actions.sort(key=lambda a: a.text())
        [self.menu.addAction(a) for a in self.actions]
        self.setContextMenu(self.menu)

    def toggle_active(self):
        self.toggle_action.setText("Enable")


class GuiService:
    def __init__(self) -> None:
        self.icon = QIcon(ICON_PATH)

        self.width = 600
        self.height = 400

        screen = QGuiApplication.primaryScreen()
        if not screen is None:
            self.center = screen.availableGeometry().center()

        settings_action = QAction("Settings")
        settings_action.triggered.connect(self.open_settings_window)

        tray = SystemTrayIcon(self.icon)
        tray.add_action(settings_action)

        self.tray = tray
        self.reminder_window: QMainWindow | None = None
        self.settings_window: QMainWindow | None = None

    def show_popup(self, message: str) -> None:
        reminder_window = QMainWindow()
        reminder_window.setWindowTitle("Remynder")
        reminder_window.setWindowIcon(self.icon)
        reminder_window.setGeometry(0, 0, self.width, self.height)
        reminder_window.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        reminder_window.setWindowFlags(Qt.WindowType.WindowTitleHint)
        reminder_window.show()
        self.reminder_window = reminder_window

    def open_settings_window(self) -> None:
        config = read_config()
        settings_window = SettingsWindow(self.icon, config)
        settings_window.show()
        self.settings_window = settings_window


class SettingsWindow(QMainWindow):
    def __init__(self, icon: QIcon, config: Config) -> None:
        super().__init__()
        self._build_ui(icon)
        self._load_settings(config)
        self._add_button_events()

    def _build_ui(self, icon: QIcon):
        self.setWindowTitle("Settings")
        self.setWindowIcon(icon)
        self.setGeometry(0, 0, SETTINGS_WINDOW_WIDTH, SETTINGS_WINDOW_HEIGHT)

        edit = QSpinBox()
        self.edit = edit

        text_field = QTextEdit()
        self.text_field = text_field

        self.save_button = QPushButton()
        self.save_button.setText("Save")

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
        self.edit.setValue(config.intervall)
        self.text_field.setText(DELIMITER.join(config.lines))

    def _save_settings(self) -> None:
        intervall = self.edit.value()
        lines = self.text_field.toPlainText().split(DELIMITER)

        config = Config(intervall, lines)
        save_config(config)
