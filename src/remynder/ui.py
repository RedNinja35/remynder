from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu


def create_tray_icon() -> QSystemTrayIcon:
    icon = QIcon('icon.png')

    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    menu = QMenu()
    action = QAction("Item")
    menu.addAction(action)

    quit_action = QAction("Quit")
    quit_action.triggered.connect(QApplication.quit)
    menu.addAction(quit_action)

    tray.setContextMenu(menu)

    return tray


class MainUi:
    def __init__(self):
        self.tray = create_tray_icon()

    def show_popup(self, message: str) -> None:
        ...
