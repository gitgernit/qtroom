__all__ = []

import asyncio
import sys

from PyQt6.QtWidgets import QMainWindow
from qasync import asyncClose
from qasync import asyncSlot
from qasync import QApplication
from qasync import QEventLoop

from client.client import Connection
from designs.app import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.connection = Connection(self.ui)
        self.username = ''

        self.ui.stackedWidget.setCurrentIndex(0)

        self.ui.connect_button.clicked.connect(self.on_join_button_clicked)
        self.ui.chat.setReadOnly(True)
        self.ui.message_entry.returnPressed.connect(self.send_message)

    @asyncSlot()
    async def send_message(self):
        message = self.ui.message_entry.text()
        self.ui.message_entry.setText('')
        await self.connection.send(
            {
                'type': 'message',
                'message': message,
            },
        )

    @asyncSlot()
    async def on_join_button_clicked(self):
        self.username = self.ui.username_input.text()

        if self.username:
            if not self.connection.writer:
                await self.connection.connect()

            await self.connection.send(
                {
                    'type': 'connection',
                    'username': self.username,
                },
            )

    @asyncClose
    async def closeEvent(self, event):
        print('closing')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    main_window = MainWindow()
    main_window.show()

    with event_loop:
        event_loop.run_until_complete(app_close_event.wait())
