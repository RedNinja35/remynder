
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon: QIcon, parent=None):
        super().__init__(icon, parent)

        self.setIcon(icon)
        self.setVisible(True)

        self.menu = QMenu()
        self.settings_action = QAction("Settings")
        self.menu.addAction(self.settings_action)

        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(QApplication.quit)
        self.menu.addAction(self.quit_action)

        self.setContextMenu(self.menu)

class GuiService:
    def __init__(self):
        icon = QIcon('remynder.png')
        self.tray = SystemTrayIcon(icon)
        self.reminder_window = None

    def show_popup(self, message: str) -> None:
        self.reminder_window = QMainWindow()
        self.reminder_window.setWindowTitle("Remynder")
        self.reminder_window.show()
