__all__ = []

import asyncio
import json
import os
import typing

import dotenv

dotenv.load_dotenv()

HOST = os.getenv('SERVER_HOST', default='localhost')
PORT = os.getenv('SERVER_PORT', default=8080)


class Connection:
    def __init__(self, ui):
        self.reader: typing.Optional[asyncio.StreamReader] = None
        self.writer: typing.Optional[asyncio.StreamWriter] = None
        self.token = None
        self.ui = ui

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(HOST, PORT)
        asyncio.create_task(self.listen())

    async def listen(self):
        while True:
            data = await self.reader.read(1024)

            if data:
                message = json.loads(data.decode())

                match message['type']:
                    case 'connection':
                        if message['valid']:
                            self.token = message['token']
                            self.ui.stackedWidget.setCurrentIndex(1) # TODO: fix the heavy delay

                        else:
                            pass

                    case 'message':
                        username = message['username']
                        msg = message['message']

                        self.ui.chat.insertPlainText(
                            f'{username}: {msg}\n',
                        )

    async def send(self, message):
        data = dict(message)
        data.update({'token': self.token})
        self.writer.write(json.dumps(data).encode())
        await self.writer.drain()
