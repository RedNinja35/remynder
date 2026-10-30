from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction, QGuiApplication
from PyQt6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu


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
        self.icon = QIcon('remynder.png')

        self.width = 1000
        self.height = 600

        screen = QGuiApplication.primaryScreen()
        if not screen is None:
            self.center = screen.availableGeometry().center()

        settings_action = QAction("Settings")
        settings_action.triggered.connect(self.open_settings_window)

        tray = SystemTrayIcon(self.icon)
        tray.add_action(settings_action)

        self.tray = tray
        self.reminder_window = None

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
        self.show_popup("Settings")