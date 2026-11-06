from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QGuiApplication, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QSystemTrayIcon,
)

SETTINGS_WINDOW_WIDTH = 1000
SETTINGS_WINDOW_HEIGHT = 800
ICON_PATH = "ressources/remynder.png"


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon: QIcon, parent=None):
        super().__init__(icon, parent)

        self.setIcon(icon)
        self.setVisible(True)

        quit_action = QAction("Quit")
        quit_action.triggered.connect(QApplication.quit)

        actions = [quit_action]
        self.actions = actions

        self._create_menu()

    def add_action(self, action: QAction) -> None:
        self.actions.append(action)
        self._create_menu()

    def _create_menu(self) -> None:
        self.menu = QMenu()
        self.actions.sort(key=lambda a: a.text())
        [self.menu.addAction(a) for a in self.actions]
        self.setContextMenu(self.menu)


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
        settings_window = SettingsWindow(self.icon)
        settings_window.show()
        self.settings_window = settings_window


class SettingsWindow(QMainWindow):
    def __init__(self, icon: QIcon) -> None:
        super().__init__()
        self.setWindowTitle("Settings")
        self.setWindowIcon(icon)
        self.setGeometry(0, 0, SETTINGS_WINDOW_WIDTH, SETTINGS_WINDOW_HEIGHT)

        self.label = QLabel(parent=self, text="Interval")
        self.interval_input = QLineEdit(self)
