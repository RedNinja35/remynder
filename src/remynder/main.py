from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from remynder.reminder import ReminderService

app = QApplication([])
app.setQuitOnLastWindowClosed(False)

reminder_service = ReminderService()

timer = QTimer()
timer.setInterval(30_000)
timer.timeout.connect(lambda: reminder_service.check())

app.exec()