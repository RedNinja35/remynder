from PyQt6.QtCore import QTimer

class Timer(QTimer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setInterval(1000)
        self.setSingleShot(True)


