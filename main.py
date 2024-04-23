__all__ = []

import sys
import os
import asyncio

from qasync import QEventLoop, QApplication, asyncClose, asyncSlot
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMainWindow

from designs.app import Ui_MainWindow
from client.client import Connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.connection = Connection(self.ui)
        self.username = 'dummy'


        self.ui.stackedWidget.setCurrentIndex(0)

        self.ui.pushButton.clicked.connect(self.on_join_button_clicked)
        self.ui.textEdit.setReadOnly(True)
        self.ui.lineEdit.returnPressed.connect(self.send_message)

    @asyncSlot()
    async def send_message(self):
        message = self.ui.lineEdit.text()
        self.ui.lineEdit.setText('')
        await self.connection.send(f'{self.username}: {message}')

    @asyncSlot()
    async def on_join_button_clicked(self):
        await self.connection.connect()

        self.username = self.ui.lineEdit_2.text()

        await self.connection.send(f'NEWUSER {self.username}')
        self.ui.stackedWidget.setCurrentIndex(1)

    @asyncClose
    async def closeEvent(self, event):
        print('closing')


if __name__ == "__main__":
    app = QApplication(sys.argv)

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    main_window = MainWindow()
    main_window.show()

    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())
